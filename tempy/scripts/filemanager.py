import os
import pickle
from tempy.scripts import cleaner
from tempy.scripts import analyzer
from tempy.scripts import converter

DEFAULT_APP_DIR = os.path.join(os.path.expanduser("~"), ".tempy")

LOG_FILE_NAME = "tempy-log.txt"

TEXT_SPACER = "\n\n\n\n"


def write_cleanup_report(file_path=DEFAULT_APP_DIR, file_name=LOG_FILE_NAME):
    log_file = open(os.path.join(file_path, file_name), "a")
    cleanup_data = cleaner.cleanup_data

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


def pickle_data(file_name, data, file_path=DEFAULT_APP_DIR):
    file = open(os.path.join(file_path, file_name + ".pickle"), "wb")
    pickle.dump(data, file)


def unpickle_data(file_name, file_path=DEFAULT_APP_DIR):
    data = None
    try:
        file = open(os.path.join(file_path, file_name + ".pickle"), "rb")
        data = pickle.load(file)
    except FileNotFoundError:
        pass

    return data
