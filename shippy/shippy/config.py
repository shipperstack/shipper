import configparser

from pathlib import Path

home_dir = str(Path.home())

# Constants
CONFIGURATION_FILE = f"{home_dir}/.shippy.ini"

# Load configuration
config = configparser.ConfigParser()
config.optionxform = str
config.read(CONFIGURATION_FILE)


def get_config_value(section, key):
    return config[section][key]


def get_optional_true_config_value(section, key):
    try:
        value = config[section][key] == "true"
        return value
    except KeyError:
        # Set default to false so users can change it later
        set_config_value(section, key, "false")
        return False


def set_config_value(section, key, value):
    config_init()
    config[section][key] = value
    config_save()


def delete_deprecated_config():
    if config.has_section("shipper"):
        config.remove_section("shipper")


def config_init():
    if not config.has_section("shippy"):
        config.add_section("shippy")
    delete_deprecated_config()


def config_save():
    with open(CONFIGURATION_FILE, "w+") as config_file:
        config.write(config_file)
