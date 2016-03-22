import tempfile
import os


class Config (object):

    dir_to_use = ""
    log_name = ""
    log_path = ""

    def __init__(self):
        self.dir_to_use = tempfile.gettempdir()
        self.log_name = "tempy-log.txt"
        self.app_dir = os.path.join(os.path.expanduser("~"), "tempy")

        if not os.path.exists(self.app_dir):
            os.makedirs(self.app_dir)
