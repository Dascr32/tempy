import tempfile


class Config (object):

    dir_to_use = ""
    log_name = ""
    log_path = ""

    def __init__(self):
        self.dir_to_use = tempfile.gettempdir()
        self.log_name = "tempcl-log.txt"
        self.log_path = "C:\\Users\\Daniel\\Desktop\\tempcl"
