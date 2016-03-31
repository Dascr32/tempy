import tempfile
import os
from tempy.scripts import filemanager


class Config (object):

    def __init__(self):

        # The first time the app is used create dir in user home
        self.app_dir = os.path.join(os.path.expanduser("~"), ".tempy")

        if not os.path.exists(self.app_dir):
            os.makedirs(self.app_dir)

        if not filemanager.config_file_exist():
            filemanager.create_config_file()

        config_data = filemanager.get_config_data()

        self.dir_to_use = tempfile.gettempdir() if config_data["dir_to_use"] == "default" else config_data["dir_to_use"]
        self.log_name = config_data["log_file_name"]
        self.app_dir = os.path.join(os.path.expanduser("~"), ".tempy") if config_data["app_dir"] == "default" \
            else config_data["app_dir"]
