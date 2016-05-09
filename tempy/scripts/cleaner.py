import os
import shutil
from tempy.scripts import analyzer
from tempy.scripts import converter

# Copy of the dir to be deleted used later for comparison
dir_before_delete = {}

# Files deleted, clean up size, date, hour, errors, etc
cleanup_data = {}

errors = []


def delete_dir_content(dir_path=analyzer.TEMP_DIR):
    global errors
    gather_data_before_delete(dir_path)

    dir_content = analyzer.get_dir_content(dir_path)

    for item in dir_content.keys():
        item_path = os.path.join(dir_path, item)

        try:
            if os.path.isfile(item_path):
                print("Deleting file:", item)
                os.remove(item_path)

            else:
                print("Deleting dir:", item)
                shutil.rmtree(item_path)

        except(os.error, shutil.Error) as error:
            errors.append(str(error))
            print("Unable to delete")

    gather_cleanup_data(dir_path)


def gather_data_before_delete(dir_path):
    global dir_before_delete
    dir_before_delete["content"] = analyzer.get_dir_content(dir_path).copy()
    dir_before_delete["size"] = analyzer.get_dir_size(dir_path, False)
    dir_before_delete["entries_count"] = analyzer.get_entries_count(dir_path)
    dir_before_delete["dirs_count"] = analyzer.get_dirs_count(dir_path)
    dir_before_delete["files_count"] = analyzer.get_files_count(dir_path)
    dir_before_delete["datetime"] = converter.get_datetime()


def gather_cleanup_data(dir_path):
    global cleanup_data
    cleanup_data["deleted"] = get_dir_difference(analyzer.get_dir_content(dir_path))
    cleanup_data["deletions"] = dir_before_delete["entries_count"] - analyzer.get_entries_count(dir_path)
    cleanup_data["size"] = dir_before_delete["size"] - analyzer.get_dir_size(dir_path, False)
    cleanup_data["errors"] = errors
    cleanup_data["error_count"] = len(errors)
    cleanup_data["datetime"] = converter.get_datetime()


def get_dir_difference(current_content, contents_before=None):
    if not contents_before:
        contents_before = dir_before_delete["content"]

    before_delete_content = set(contents_before.items())
    current_dir_content = set(current_content.items())

    return dict(before_delete_content.difference(current_dir_content))
