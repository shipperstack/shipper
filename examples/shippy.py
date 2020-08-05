import configparser
import sys
from pathlib import Path

# Get user home directory
home_dir = str(Path.home())

# Define constants
SERVER_URL = "http://127.0.0.1:8000"
CONFIGURATION_FILE = "{}/.shippy.ini".format(home_dir)
TOKEN = ""
DEBUG = False


def exception_handler(exception_type, exception, traceback, debug_hook=sys.excepthook):
    if DEBUG:
        debug_hook(exception_type, exception, traceback)
    else:
        print("%s: %s" % (exception_type.__name__, exception))


sys.excepthook = exception_handler


# From https://stackoverflow.com/a/3041990, adapted for use in this script
def input_yn(question, default=True):
    global TOKEN
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default:
        prompt = " [Y/n] "
    else:
        prompt = " [y/N] "

    while True:
        print(question + prompt, end='')
        choice = input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")


def login_to_server(username, password):
    import requests
    """ Logs in to server and returns authorization token """
    LOGIN_URL = "{}/maintainers/api/login/".format(SERVER_URL)
    r = requests.post(LOGIN_URL, data={'username': username, 'password': password})

    if r.status_code == 200:
        data = r.json()
        return data['token']
    elif r.status_code == 400:
        raise Exception("Username or password must not be blank.")
    elif r.status_code == 404:
        raise Exception("Invalid credentials!")
    else:
        raise Exception("An unknown error occurred.")


def upload_to_server(build_file, checksum_file, gapps, release):
    import os.path
    # Get codename from build_file
    build_file_name, build_file_ext = os.path.splitext(build_file)
    try:
        _, version, codename, type, date = build_file_name.split('-')
    except:
        raise Exception("The file name is mangled!")

    import requests
    # Get device ID from server
    DEVICE_ID_URL = "{}/maintainers/api/device/id/".format(SERVER_URL)
    print("Fetching device ID for device {}...".format(codename))
    r = requests.get(DEVICE_ID_URL, headers={"Authorization": "Token {}".format(TOKEN)}, data={"codename": codename})

    if r.status_code == 200:
        data = r.json()
        device_id = data['id']
    elif r.status_code == 400:
        raise Exception("The device with the specified codename does not exist.")
    elif r.status_code == 401:
        raise Exception("You are not authorized to upload with this device.")
    else:
        raise Exception("A problem occurred while querying the device ID.")

    print("Uploading build {}...".format(build_file))

    DEVICE_UPLOAD_URL = "{}/maintainers/api/device/{}/upload/".format(SERVER_URL, device_id)

    files = {
        'build_file': open(build_file, 'rb'),
        'checksum_file': open(checksum_file, 'rb')
    }
    r = requests.post(DEVICE_UPLOAD_URL,
                      headers={"Authorization": "Token {}".format(TOKEN)},
                      data={
                          "gapps": gapps,
                          "release": release
                      },
                      files=files
                      )

    if r.status_code == 200:
        print("Successfully uploaded the build {}!".format(build_file))
    elif r.status_code == 400:
        raise Exception("One of the required fields were missing.")
    elif r.status_code == 401:
        raise Exception("You are not allowed to upload for the device {}!".format(codename))
    elif r.status_code == 500:
        raise Exception("An internal server error occurred. Contact the administrators for help.")
    else:
        raise Exception("A problem occurred while uploading your build.")


def main():
    global TOKEN

    # Load configuration file
    config = configparser.ConfigParser()
    config.read(CONFIGURATION_FILE)

    print("Welcome to shippy!")

    try:
        TOKEN = config['shipper']['token']
    except KeyError:
        print("""
It looks like this is your first time running shippy.
In the next couple of steps, shippy will ask for your username
and password and fetch the authentication token from the shipper server.
This token will be saved in {}. Let's get started!
        """.format(CONFIGURATION_FILE))

        config.add_section('shipper')

        while True:
            from getpass import getpass

            username = input("Enter your username: ")
            password = getpass(prompt="Enter your password: ")

            try:
                config['shipper']['token'] = TOKEN = login_to_server(username, password)

                with open(CONFIGURATION_FILE, 'w+') as config_file:
                    config.write(config_file)
                break
            except Exception as e:
                print("An error occurred logging into the server. Please try again.")

    # Search current directory for files
    import glob

    glob_match = 'Bliss-v*.zip'
    build_count = len(glob.glob(glob_match))
    builds = []

    if build_count == 0:
        print("""
Oops, no files were detected! Are you sure you are in the correct directory?
Please do not rename the build artifacts. This breaks a lot of systems.
If you have a unique case contact maintainer support.
        """)
    else:
        if build_count == 1:
            print("Detected the following build:")
        else:
            print("Detected the following builds:")
        for file in glob.glob(glob_match):
            print("\t{}".format(file))
            builds.append(file)
        if input_yn("Proceed with the upload?"):
            for build in builds:
                # Check if build has md5 file
                import os.path
                if not os.path.isfile("{}.md5".format(build)):
                    print("We couldn't find a valid checksum file for this build! Skipping....")
                else:
                    while True:
                        # Specify build options
                        print("Please specify the options for {}".format(build))
                        gapps = input_yn("Does the build include GApps?")
                        while True:
                            VALID_RELEASE_TYPES = ["Stable", "Beta", "Alpha"]
                            valid_release_type_string = "/".join(VALID_RELEASE_TYPES)
                            release = input("Specify the release type ({}): ".format(valid_release_type_string))
                            if release not in VALID_RELEASE_TYPES:
                                print("Incorrect input! Please try again.")
                            else:
                                break

                        if input_yn("We are uploading the build {} with{} GApps and with release branch {}. Correct?".format(
                            build,
                            "" if gapps else "out",
                            release
                        )):
                            upload_to_server(build, "{}.md5".format(build), gapps, release)
                            break
                        else:
                            print("OK. Let's try again.")


if __name__ == "__main__":
    main()
