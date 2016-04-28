import os
import tempfile
import prettytable
from contextlib import suppress
from collections import OrderedDict
from tempy.scripts import converter

TEMP_DIR = tempfile.gettempdir()


def dir_tree(root_dir_path=TEMP_DIR):
    root_dirs_detail = "."
    root_files = ""

    for element in os.listdir(root_dir_path):
        if os.path.isdir(os.path.join(root_dir_path, element)):
            root_dirs_detail += "\n+-- " + element

            for files in os.listdir(os.path.join(root_dir_path, element)):
                root_dirs_detail += "\n|\t+-- " + files

                if os.path.isdir(os.path.join(root_dir_path, element, files)):
                    root_dirs_detail += " (DIR)"

        else:
            root_files += "\n+-- " + element

    return root_dirs_detail + root_files


def table_from_content(dir_content=None, sort_by="Size"):
    table = prettytable.PrettyTable(["File", "Size"])

    if not dir_content:
        table.add_row(["Directory is empty", "--"])

    if sort_by == "Size":
        dir_content = OrderedDict(sorted(dir_content.items(), key=lambda t: t[1]))

    for file, size in dir_content.items():
        table.add_row([file, human_readable_size(size)])

    return table.get_string(sortby="File") if sort_by == "File" else table.get_string()


def get_dir_content(dir_path=TEMP_DIR):
    files = {}

    for entry in os.listdir(dir_path):
        entry_path = os.path.join(dir_path, entry)

        if os.path.isdir(entry_path):
            files[entry] = get_dir_size(entry_path)

        else:
            files[entry] = os.path.getsize(entry_path)

    return files


def get_dir_size(root_dir_path=TEMP_DIR, readable=False):
    raw_dir_size = 0

    with suppress(os.error):
        for dir_path, dir_names, file_names in os.walk(root_dir_path):
            for file in file_names:
                file_path = os.path.join(dir_path, file)
                raw_dir_size += os.path.getsize(file_path)

    return human_readable_size(raw_dir_size) if readable else raw_dir_size


def get_entries_count(dir_path=TEMP_DIR):
    return len(os.listdir(dir_path))


def get_dirs_count(dir_path=TEMP_DIR):
    count = 0

    for entry in os.listdir(dir_path):
        entry_path = os.path.join(dir_path, entry)
        if os.path.isdir(entry_path):
            count += 1

    return count


def get_files_count(dir_path=TEMP_DIR):
    count = 0

    for entry in os.listdir(dir_path):
        if not os.path.isdir(os.path.join(dir_path, entry)):
            count += 1

    return count


def get_all_data(dir_path):
    data = dict()

    data["contents"] = table_from_content(get_dir_content(dir_path))
    data["entries_count"] = get_entries_count(dir_path)
    data["dirs_count"] = get_dirs_count(dir_path)
    data["files_count"] = get_files_count(dir_path)
    data["size"] = get_dir_size(dir_path, readable=True)

    return data


def human_readable_size(raw_size):
    return converter.human_readable_size(raw_size)
