import argparse
import re
import glob
import os.path
import signal
import sys
from json import JSONDecodeError
from loguru import logger

import requests
import semver
import sentry_sdk

from rich import print
from rich.console import Console

from .client import (
    get_hash_from_checksum_file,
    get_hash_of_file,
    find_checksum_file,
    Client,
)
from .config import get_config_value, set_config_value, get_optional_true_config_value
from .constants import (
    SENTRY_SDK_URL,
    SERVER_COMPAT_ERROR_MSG,
    SHIPPY_COMPAT_ERROR_MSG,
    SHIPPY_OUTDATED_MSG,
    UNEXPECTED_SERVER_RESPONSE_ERROR_MSG,
    FAILED_TO_LOG_IN_ERROR_MSG,
    CANNOT_CONTACT_SERVER_ERROR_MSG,
    PRERELEASE_WARNING_MSG,
    NO_CONFIGURATION_WARNING_MSG,
)
from .exceptions import LoginException, UploadException
from .helper import input_yn, print_error, print_warning, print_success
from .version import __version__
from .server_compat_version import server_compat_version

sentry_sdk.init(
    dsn=SENTRY_SDK_URL,
    traces_sample_rate=1.0,
    release=f"{__version__}",
    ignore_errors=[ConnectionError],
)

console = Console()


# Handle SIGINT gracefully and don't puke up traceback
def sigint_handler(*_):
    exit(1)


signal.signal(signal.SIGINT, sigint_handler)


def lower_logger_level():
    logger.remove()
    logger.add(sys.stderr, level="INFO")


def server_prechecks(client):
    check_server_compat(client)
    check_token_validity(client)


def check_and_upload_build(client, args, build_path):
    # Check build file validity
    if not check_build(client, build_path):
        print_warning("Invalid build. Skipping...")
        return

    if is_upload_without_prompt_enabled(args) or input_yn(
        f"Uploading build {build_path}. Start?"
    ):
        try:
            uploaded_build_id = client.upload(build_path=build_path)

            if is_build_disabling_enabled():
                client.disable_build(build_id=uploaded_build_id)
        except UploadException as exception:
            logger.exception(exception)
            print_error(exception, newline=True, exit_after=False)


def search_and_upload_builds(client, args):
    # Search current directory for files with regex pattern returned by server
    build_paths = get_builds_in_current_dir(client.get_regex_pattern())

    if len(build_paths) == 0:
        print_error(
            msg="No files matching the submission criteria were detected in the "
            "current directory.",
            newline=True,
            exit_after=False,
        )
    else:
        print(f"Detected {len(build_paths)} build(s):")
        for build_path in build_paths:
            print(f"\t{build_path}")

        if not is_upload_without_prompt_enabled(args) and len(build_paths) > 1:
            print_warning("You seem to be uploading multiple builds. ", newline=False)
            if not input_yn("Are you sure you want to continue?", default=False):
                return

        for build_path in build_paths:
            check_and_upload_build(client, args, build_path)


def is_upload_without_prompt_enabled(args):
    config_value = get_optional_true_config_value("shippy", "UploadWithoutPrompt")

    return config_value or args.yes


def build_client_from_config():
    try:
        url = get_config_value("shippy", "server")
        if not check_server_url_schema(url):
            print_error(
                msg="The configuration file is corrupt. Please delete it and restart "
                "shippy.",
                newline=True,
                exit_after=True,
            )

        token = get_config_value("shippy", "token")
        server = Client(server_url=url, token=token)
    except KeyError:
        print_warning(NO_CONFIGURATION_WARNING_MSG)
        server = Client(server_url=get_server_url())
        prompt_login(server)
    return server


def init_argparse():
    parser = argparse.ArgumentParser(
        description="Client-side tool for interfacing with shipper"
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Upload builds automatically without prompting",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Show version of shippy and exit",
    )
    return parser.parse_args()


def check_server_compat(client):
    with console.status(
        "Please wait while shippy contacts the remote server to check compatibility... "
    ):
        # Check if shipper version is compatible
        if not client.is_server_compatible():
            print_error(
                msg=SERVER_COMPAT_ERROR_MSG.format(
                    client.get_version(), server_compat_version
                ),
                newline=True,
                exit_after=True,
            )

    # Check if shippy version is compatible, but only if running stable builds
    if is_prerelease():
        print_warning(
            "You're running a prerelease build of shippy. Server compatibility checks "
            "are disabled."
        )
    else:
        if not client.is_shippy_compatible():
            print_error(
                msg=SHIPPY_COMPAT_ERROR_MSG.format(
                    client.get_shippy_compat_version(), __version__
                ),
                newline=True,
                exit_after=True,
            )

    print_success("Finished compatibility check. No problems found.")


def check_token_validity(client):
    with console.status(
        "Please wait while shippy contacts the remote server to check if the token is "
        "still valid... "
    ):
        if client.is_token_valid():
            print_success(
                f"Successfully validated token! Hello, {client.get_username()}!"
            )
        else:
            # Token check failed, prompt for login again
            print_warning("The saved token is invalid. Please sign-in again.")
            prompt_login(client)


def check_shippy_update():
    with console.status("Please wait while shippy checks for updates... "):
        try:
            r = requests.get(
                "https://api.github.com/repos/shipperstack/shipper/releases/latest"
            )
            latest_version = r.json()["name"]
        except KeyError:
            print_error(
                "Failed to contact the GitHub API to check the latest version.",
                newline=True,
                exit_after=False,
            )

    # Check if user is running an alpha/beta build
    if is_prerelease():
        print_warning(PRERELEASE_WARNING_MSG)
    else:
        # User is running a stable build, proceed with update check
        if semver.compare(__version__, latest_version) == -1:
            print(SHIPPY_OUTDATED_MSG.format(__version__, latest_version))
        else:
            print_success("Finished update check. shippy is up-to-date!")


def is_prerelease():
    return "a" in __version__ or "b" in __version__


def get_builds_in_current_dir(regex_pattern):
    with console.status("Detecting builds in current directory..."):
        builds = []
        files = [f for f in glob.glob("*.zip")]
        for file in files:
            if re.search(regex_pattern, file):
                builds.append(file)

        return builds


def check_build(client, filename):
    """Makes sure the build is valid"""
    print(f"Validating build {filename}...")
    # Validate that there is a matching checksum file
    has_checksum_file_type, has_sum_postfix = find_checksum_file(filename=filename)

    if has_checksum_file_type is None:
        print_warning(
            "This build does not have a matching checksum file. ", newline=False
        )
        return False
    else:
        print_success("Matching checksum file exists!")

    # Validate checksum
    with console.status(f"Checking {has_checksum_file_type.upper()} hash..."):
        hash_val = get_hash_of_file(
            filename=filename, checksum_type=has_checksum_file_type
        )
        if not has_sum_postfix:
            actual_hash_val = get_hash_from_checksum_file(
                f"{filename}.{has_checksum_file_type}"
            )
        else:
            actual_hash_val = get_hash_from_checksum_file(
                f"{filename}.{has_checksum_file_type}sum"
            )
        if hash_val != actual_hash_val:
            print_error(
                msg="This build's checksum is invalid. ",
                newline=False,
                exit_after=False,
            )
            return False
        print_success(f"Checksum {has_checksum_file_type.upper()} hash matches!")

    build_slug, _ = os.path.splitext(filename)
    _, _, _, build_type, build_variant, _ = build_slug.split("-")

    # Check build type
    if build_type != "OFFICIAL":
        print_error(msg="This build is not official. ", newline=False, exit_after=False)
        return False
    else:
        print_success("Build type is official!")

    # Check build variant
    if build_variant not in client.get_shippy_upload_variants():
        print_error(
            msg="This build has an unknown variant. ",
            newline=False,
            exit_after=False,
        )
        return False
    else:
        print_success(f"Build variant {build_variant} is supported!")

    print_success(f"Validation of build {filename} complete. No problems found.")
    return True


def get_server_url():
    try:
        while True:
            server_url = input("Enter the server URL: ")
            if not check_server_url_schema(server_url):
                # noinspection HttpUrlsUsage
                print_error(
                    msg="Server URL is missing either http:// or https://.",
                    newline=True,
                    exit_after=False,
                )
            else:
                break

        set_config_value("shippy", "server", server_url)

        return server_url
    except KeyboardInterrupt:
        exit(0)


def check_server_url_schema(url):
    return "http" in url


def prompt_login(client):
    while True:
        from getpass import getpass

        try:
            username = input("Enter your username: ")
            password = getpass(prompt="Enter your password: ")

            try:
                client.login(username=username, password=password)
                set_config_value("shippy", "token", client.token)
                print_success("Successfully logged in!")
                return
            except LoginException as exception:
                print_error(exception, newline=True, exit_after=True)
            except JSONDecodeError:
                print_error(
                    msg=UNEXPECTED_SERVER_RESPONSE_ERROR_MSG
                    + FAILED_TO_LOG_IN_ERROR_MSG,
                    newline=True,
                    exit_after=True,
                )
            except requests.exceptions.RequestException as e:
                logger.error(e)
                print_error(
                    msg=CANNOT_CONTACT_SERVER_ERROR_MSG + FAILED_TO_LOG_IN_ERROR_MSG,
                    newline=True,
                    exit_after=True,
                )
        except KeyboardInterrupt:
            exit(0)


def is_build_disabling_enabled():
    try:
        return get_config_value("shippy", "DisableBuildOnUpload") == "true"
    except KeyError:
        return False


def check_debug_mode(args):
    return args.debug or get_optional_true_config_value("shippy", "debug")


def main():
    # Get commandline arguments
    args = init_argparse()

    lower_logger_level()

    if args.version:
        print(__version__)
        return

    if check_debug_mode(args):
        print_warning("Debug mode has been turned on!")
        logger.add(sink="shippy_{time}.log", level="DEBUG", enqueue=True)

    print(f"Welcome to shippy (v.{__version__})!")

    # Check for updates
    check_shippy_update()

    # Initialize client
    client = build_client_from_config()
    server_prechecks(client)

    # Start uploads
    search_and_upload_builds(client, args)


if __name__ == "__main__":
    main()
