import os
import tempfile
import prettytable
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


def table_from_content(dir_content=None, type="string", sort_by="File"):
    table = prettytable.PrettyTable(["File", "Size"])

    if not dir_content:
        dir_content = get_dir_content()

    for file, size in dir_content.items():
        table.add_row([file, human_readable_size(size)])

    return table.get_string(sortby=sort_by) \
        if type == "string" else table.get_html_string(sortby=sort_by)


def get_dir_content(dir_path=TEMP_DIR):
    files = {}

    for file_name in os.listdir(dir_path):
        files[file_name] = os.path.getsize(os.path.join(dir_path, file_name))

    return files


def get_dir_size(root_dir_path=TEMP_DIR, readable=False):
    raw_dir_size = 0

    for dir_path, dir_names, file_names in os.walk(root_dir_path):
        for file in file_names:
            file_path = os.path.join(dir_path, file)
            raw_dir_size += os.path.getsize(file_path)

    return human_readable_size(raw_dir_size) if readable else raw_dir_size


def get_total_files(dir_path=TEMP_DIR):
    return len(os.listdir(dir_path))


def get_all_data(dir_path):
    data = dict()

    data["contents"] = table_from_content()
    data["elements"] = get_total_files(dir_path)
    data["size"] = get_dir_size(dir_path, readable=True)

    return data


def human_readable_size(raw_size):
    return converter.human_readable_size(raw_size)
