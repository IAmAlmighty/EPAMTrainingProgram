import configparser
import os

abspath = os.path.abspath


class Config:
    PROJECT_DIR = abspath(os.path.dirname(__file__) + r"../..")
    CONFIG_INI_FILE = abspath(PROJECT_DIR + "/config.ini")

    def __init__(self):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(self.CONFIG_INI_FILE)

    @property
    def db_items(self):
        return self.cfg._sections["DB"]

    @property
    def df_items(self):
        return self.cfg._sections["DF"]
