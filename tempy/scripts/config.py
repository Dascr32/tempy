import tempfile
import os
from tempy.scripts import filemanager


class Config(object):
    def __init__(self):
        self.app_dir = os.path.join(os.path.expanduser("~"), ".tempy")

        if not os.path.exists(self.app_dir):
            os.makedirs(self.app_dir)

        if not filemanager.config_file_exist():
            filemanager.create_config_file(self.app_dir)

        config_data = filemanager.get_config_data()

        # Check if dir_to_use is a subdir of the temp directory, to prevent deletion of important dirs.
        if config_data["dir_to_use"] != "default" and config_data["dir_to_use"].startswith(
                os.path.abspath(tempfile.gettempdir() + "/")):
            self.dir_to_use = config_data["dir_to_use"]

        else:
            self.dir_to_use = tempfile.gettempdir()

        self.log_name = config_data["log_file_name"]
