import os
import pickle
import json
from contextlib import suppress
from tempy.scripts import cleaner
from tempy.scripts import analyzer
from tempy.scripts import converter

DEFAULT_APP_DIR = os.path.join(os.path.expanduser("~"), ".tempy")

LOG_FILE_NAME = "tempy-log.txt"

CONFIG_FILE_NAME = "config.json"

TEXT_SPACER = "\n\n\n\n"


def write_cleanup_report(cleanup_data, file_path=DEFAULT_APP_DIR, file_name=LOG_FILE_NAME):
    log_file = open(os.path.join(file_path, file_name), "a")

    if not cleanup_data:
        log_file.write("\n\nNo clean up data available at: " + converter.get_datetime())

    else:
        log_file.write(format_report_head(cleaner.dir_before_delete))
        log_file.write(format_report_body(cleanup_data))

    log_file.close()


def format_report_head(data):
    output = "\n\n##### Clean up performed at: " + data["datetime"] + "#####\n\n"
    output += "\n==== Directory contents on delete ====\n\n"
    output += analyzer.table_from_content(data["content"]) + "\n\n"
    output += "=> Files: " + str(data["files_count"]) + " / Dirs: " + str(data["dirs_count"]) + "\n"
    output += "=> Size: " + converter.human_readable_size(data["size"]) + "\n"

    return output


def format_report_body(data):
    output = "\n"

    if data["deletions"] != 0:
        output += "==== Deleted Files/Dirs ====\n\n"
        output += analyzer.table_from_content(data["deleted"]) + "\n\n"
        output += "=> Clean up size: " + converter.human_readable_size(data["size"]) + "\n"
        output += "=> Deletions: " + str(data["deletions"]) + "\n"
        output += "\n"
        output += "=> Errors: " + str(data["error_count"])

    else:
        output += "=> No files or directories where deleted"

    output += TEXT_SPACER

    return output


def create_config_file(dir_path=DEFAULT_APP_DIR):
    config = dict()
    config["dir_to_use"] = "default"
    config["log_file_name"] = LOG_FILE_NAME

    with open(os.path.join(dir_path, CONFIG_FILE_NAME), "w") as outfile:
        json.dump(config, outfile)

    return config


def get_config_data(dir_path=DEFAULT_APP_DIR):
    data = None

    if not config_file_exist(dir_path):
        create_config_file(dir_path)

    with open(os.path.join(dir_path, CONFIG_FILE_NAME)) as data_file:
            data = json.load(data_file)

    return data


def modify_config(parameter, value, dir_path=DEFAULT_APP_DIR):

    if not config_file_exist(dir_path):
        create_config_file(dir_path)

    config = get_config_data(dir_path)
    config[parameter] = value

    with open(os.path.join(dir_path, CONFIG_FILE_NAME), "w") as outfile:
        json.dump(config, outfile)


def config_file_exist(dir_path=DEFAULT_APP_DIR):
    return os.path.exists(os.path.join(dir_path, CONFIG_FILE_NAME))


def pickle_data(file_name, data, dir_path=DEFAULT_APP_DIR):
    with open(os.path.join(dir_path, file_name + ".pickle"), "wb") as file:
        pickle.dump(data, file)


def unpickle_data(file_name, dir_path=DEFAULT_APP_DIR):
    data = None
    with open(os.path.join(dir_path, file_name + ".pickle"), "rb") as file:
        data = pickle.load(file)

    return data
