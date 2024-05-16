import hashlib
import os.path
import requests
import re
import time
import urllib.parse

from json.decoder import JSONDecodeError

import semver
from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from loguru import logger

from .constants import (
    BLANK_AUTH_DETAILS_MSG,
    BUILD_DISABLED_MSG,
    GATEWAY_SERVER_UNAVAILABLE_MSG,
    INVALID_CREDENTIALS_MSG,
    LOG_DEBUG_REQUEST_RESPONSE_MSG,
    LOG_DEBUG_REQUEST_SEND_MSG,
    RESPONSE_PARSING_FAILED_MSG,
    SERVER_EMPTY_TOKEN_MSG,
    SERVER_TEMPORARILY_UNAVAILABLE_MSG,
    SERVER_WRONG_SCHEMA_MSG,
    UNHANDLED_EXCEPTION_MSG,
    FAILED_TO_RETRIEVE_SERVER_VERSION_ERROR_MSG,
    RATE_LIMIT_WAIT_STATUS_MSG,
    RATE_LIMIT_MSG,
    UNKNOWN_UPLOAD_ERROR_MSG,
    UNKNOWN_UPLOAD_START_ERROR_MSG,
    UPLOAD_SUCCESSFUL_MSG,
    WAITING_FINALIZATION_MSG,
    CHUNK_SIZE,
    INTERNAL_SERVER_ERROR_MSG,
    FOUND_PREVIOUS_BUILD_ATTEMPT_MSG,
    DISABLE_BUILD_FAILED_MSG,
    SERVER_ERROR_WAITING_MSG,
    SERVER_ERROR_WAIT_STATUS_MSG,
)
from .exceptions import LoginException, UploadException
from .version import __version__
from .server_compat_version import server_compat_version

console = Console()

# Set up progress bar
progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
    transient=True,
)


def log_debug_request_send(request_type, url, headers=None, data=None):
    logger.debug(LOG_DEBUG_REQUEST_SEND_MSG.format(request_type, url, headers, data))


def log_debug_request_response(r):
    try:
        r_content = r.json()
    except ValueError:
        r_content = r.content

    logger.debug(LOG_DEBUG_REQUEST_RESPONSE_MSG.format(r_content))


def wait_rate_limit(seconds):
    with console.status(RATE_LIMIT_WAIT_STATUS_MSG.format(seconds)) as status:
        while seconds:
            time.sleep(1)
            seconds -= 1
            status.update(status=RATE_LIMIT_WAIT_STATUS_MSG.format(seconds))


def wait_temporary_error(seconds):
    with console.status(SERVER_ERROR_WAIT_STATUS_MSG.format(seconds)) as status:
        while seconds:
            time.sleep(1)
            seconds -= 1
            status.update(status=SERVER_ERROR_WAIT_STATUS_MSG.format(seconds))


class Client:
    def __init__(self, server_url, token=None):
        self.server_url = server_url
        self.token = token

    def is_url_secure(self):
        return self.server_url[0:5] == "https"

    def is_server_compatible(self):
        server_compat = semver.VersionInfo.parse(server_compat_version)
        return self.get_version() >= server_compat

    def is_shippy_compatible(self):
        shippy_version = semver.VersionInfo.parse(__version__)
        return shippy_version >= self.get_shippy_compat_version()

    def login(self, username, password):
        r = self._post(
            url="/api/v1/maintainers/login/",
            data={"username": username, "password": password},
        )

        match r.status_code:
            case 200:
                token = r.json()["token"]

                if token == b"":
                    raise LoginException(SERVER_EMPTY_TOKEN_MSG)
                else:
                    self.token = token
            case 301:
                if not self.is_url_secure():
                    raise LoginException(SERVER_WRONG_SCHEMA_MSG)
            case 400:
                if r.json()["error"] == "blank_username_or_password":
                    raise LoginException(BLANK_AUTH_DETAILS_MSG)
            case 404:
                if r.json()["error"] == "invalid_credential":
                    raise LoginException(INVALID_CREDENTIALS_MSG)
            case 502:
                raise LoginException(GATEWAY_SERVER_UNAVAILABLE_MSG)
            case 503:
                raise LoginException(SERVER_TEMPORARILY_UNAVAILABLE_MSG)
            case _:
                handle_undefined_response(r)

    def get_version(self):
        return semver.VersionInfo.parse(self._get_info()["version"])

    def get_shippy_compat_version(self):
        return semver.VersionInfo.parse(self._get_info()["shippy_compat_version"])

    def get_shippy_upload_variants(self):
        return self._get_info()["shippy_upload_variants"]

    def duplicate_check(self, file_name):
        r = self._post(
            url="/api/v1/maintainers/build/duplicate_check/",
            headers=self._get_header(),
            data={"file_name": file_name},
        )
        return r.json()["exists"] == "true"

    def _get_info(self):
        r = self._get(url="/api/v2/system/info")
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception(FAILED_TO_RETRIEVE_SERVER_VERSION_ERROR_MSG)

    def get_regex_pattern(self):
        r = self._get(
            url="/api/v1/maintainers/upload_filename_regex_pattern",
            headers=self._get_header(),
        )

        if r.status_code == 200:
            return r.json()["pattern"]

    def _get_checksum_type(self):
        return self._get_info()["shippy_upload_checksum_type"]

    def get_username(self):
        r = self._get(
            url="/api/v1/maintainers/token_check/",
            headers=self._get_header(),
        )

        return r.json()["username"]

    def is_token_valid(self):
        r = self._get(
            url="/api/v1/maintainers/token_check/",
            headers=self._get_header(),
        )

        return r.status_code == 200

    def _get_upload_info(self, build_path):
        current_byte = 0
        upload_id = ""

        # Check for previous attempts
        try:
            previous_attempts = self._get(
                url="/api/v1/maintainers/chunked_upload/", headers=self._get_header()
            ).json()
        except requests.exceptions.RequestException as exc:
            raise UploadException(UNKNOWN_UPLOAD_ERROR_MSG) from exc
        for attempt in previous_attempts:
            if build_path == attempt["filename"]:
                logger.debug(
                    FOUND_PREVIOUS_BUILD_ATTEMPT_MSG.format(
                        build_path, attempt["created_at"]
                    ),
                )
                current_byte = attempt["offset"]
                upload_id = attempt["id"]
        return current_byte, upload_id

    def upload(self, build_path):
        total_file_size = os.path.getsize(build_path)

        with progress:
            upload_progress = progress.add_task(
                "[green]Uploading...", total=total_file_size
            )

            current_byte, upload_id = self._get_upload_info(build_path)

            with open(build_path, "rb") as build_file:
                build_file.seek(current_byte)
                chunk = build_file.read(CHUNK_SIZE)
                while chunk:
                    try:
                        r = self._upload_chunk(
                            build_path=build_path,
                            chunk=chunk,
                            current=current_byte,
                            total=total_file_size,
                            upload_id=upload_id,
                        )

                        if r.status_code == 200:
                            upload_id = r.json()["id"]
                            current_byte += len(chunk)
                            progress.update(upload_progress, completed=current_byte)

                            # Read next chunk and continue
                            chunk = build_file.read(CHUNK_SIZE)
                        elif int(r.status_code / 100) == 4:
                            upload_handle_4xx_response(r)
                        else:
                            raise UploadException(
                                UNKNOWN_UPLOAD_START_ERROR_MSG
                            ) from handle_undefined_response(r)
                    except requests.exceptions.RequestException as exc:
                        raise UploadException(UNKNOWN_UPLOAD_ERROR_MSG) from exc

        # Finalize upload to begin processing
        try:
            with console.status(WAITING_FINALIZATION_MSG):
                checksum = get_hash_of_file(
                    build_path, checksum_type=self._get_checksum_type()
                )
                r = self._upload_finalize(upload_id=upload_id, checksum=checksum)

                upload_exception_check(r, build_path)
        except UploadException as e:
            raise e
        except requests.exceptions.RequestException as exc:
            raise UploadException(UNKNOWN_UPLOAD_ERROR_MSG) from exc

        return r.json()["build_id"]

    def disable_build(self, build_id):
        r = self._post(
            "/api/v1/maintainers/build/enabled_status_modify/",
            headers=self._get_header(),
            data={"build_id": build_id, "enable": False},
        )

        if r.status_code == 200:
            print(BUILD_DISABLED_MSG.format(build_id))
        else:
            raise Exception(DISABLE_BUILD_FAILED_MSG)

    def _upload_chunk(self, build_path, chunk, current, total, upload_id):
        if upload_id:
            url = f"/api/v1/maintainers/chunked_upload/{upload_id}/"
        else:
            url = "/api/v1/maintainers/chunked_upload/"
        result = self._put(
            url=url,
            headers=self._get_header(chunk=chunk, current=current, total=total),
            data={"filename": build_path},
            files={"file": chunk},
        )
        return result

    def _upload_finalize(self, upload_id, checksum):
        return self._post(
            url=f"/api/v1/maintainers/chunked_upload/{upload_id}/",
            headers=self._get_header(),
            data={self._get_checksum_type(): checksum},
        )

    def _get_header(self, chunk=None, current=None, total=None):
        header = {
            "User-Agent": f"shippy {__version__}",
            "Authorization": f"Token {self.token}",
        }

        if chunk is not None and current is not None and total is not None:
            header["Content-Range"] = (
                f"bytes {current}-{current + len(chunk) - 1}/{total}"
            )

        return header

    def _request(self, type, url, headers=None, data=None, files=None):
        request_url = urllib.parse.urljoin(self.server_url, url)
        log_debug_request_send(
            request_type=type,
            url=request_url,
            headers=headers,
            data=data,
        )
        match type:
            case "GET":
                r = requests.get(url=request_url, headers=headers, data=data)
            case "POST":
                r = requests.post(
                    url=request_url,
                    headers=headers,
                    data=data,
                    allow_redirects=False,
                )
            case "PUT":
                r = requests.put(
                    url=request_url,
                    headers=headers,
                    data=data,
                    files=files,
                )
            case _:
                return
        log_debug_request_response(r)

        # Check for rate limit
        if r.status_code == 429:
            print(RATE_LIMIT_MSG)
            wait_rate_limit(int(re.findall(r"\d+", r.json()["detail"])[0]))

            return self._request(
                type=type, url=url, headers=headers, data=data, files=files
            )

        # Check for temporary server-side errors
        if int(r.status_code / 100) == 5:
            print(SERVER_ERROR_WAITING_MSG)
            wait_temporary_error(30)

            return self._request(
                type=type, url=url, headers=headers, data=data, files=files
            )

        return r

    def _post(self, url, headers=None, data=None):
        return self._request("POST", url, headers, data)

    def _get(self, url, headers=None, data=None):
        return self._request("GET", url, headers, data)

    def _put(self, url, headers, data, files):
        return self._request("PUT", url, headers, data, files)


def handle_undefined_response(request):
    """Handles undefined responses sent back by the server"""
    try:
        raise Exception(
            UNHANDLED_EXCEPTION_MSG.format(
                request.url, request.status_code, request.json()
            )
        )
    except JSONDecodeError:
        raise Exception(
            UNHANDLED_EXCEPTION_MSG.format(
                request.url, request.status_code, request.content
            )
        )


def upload_handle_4xx_response(chunk_request):
    try:
        response_json = chunk_request.json()
        raise UploadException(response_json["message"])
    except (KeyError, JSONDecodeError) as exc:
        raise UploadException(UNKNOWN_UPLOAD_ERROR_MSG) from exc


def get_hash_of_file(filename, checksum_type):
    if checksum_type.lower() == "md5":
        hash_obj = hashlib.md5()
    elif checksum_type.lower() == "sha256":
        hash_obj = hashlib.sha256()
    else:
        # Unsupported checksum type
        return None

    with open(filename, "rb") as file:
        content = file.read()
        hash_obj.update(content)
    return hash_obj.hexdigest()


def get_hash_from_checksum_file(checksum_file):
    with open(checksum_file, "r") as checksum_file_raw:
        line = checksum_file_raw.readline()
        values = line.split(" ")
        return values[0]


def find_checksum_file(filename):
    valid_checksum_types = ["md5", "sha256"]
    has_checksum_file_type = None
    has_sum_postfix = False
    for checksum_type in valid_checksum_types:
        if os.path.isfile(f"{filename}.{checksum_type}"):
            has_checksum_file_type = checksum_type
            has_sum_postfix = False
        elif os.path.isfile(f"{filename}.{checksum_type}sum"):
            has_checksum_file_type = checksum_type
            has_sum_postfix = True
    return has_checksum_file_type, has_sum_postfix


def upload_exception_check(request, build_file):
    if request.status_code == 200:
        print(UPLOAD_SUCCESSFUL_MSG.format(build_file))
        return
    elif int(request.status_code / 100) == 4:
        try:
            response_json = request.json()
            raise UploadException(response_json["message"])
        except (JSONDecodeError, KeyError) as exc:
            raise UploadException(RESPONSE_PARSING_FAILED_MSG) from exc
    elif int(request.status_code / 100) == 5:
        raise UploadException(INTERNAL_SERVER_ERROR_MSG)

    handle_undefined_response(request)
