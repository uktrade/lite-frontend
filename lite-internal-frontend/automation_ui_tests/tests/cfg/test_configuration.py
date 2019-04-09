from selenium import webdriver
from sys import platform
import os


class TestConfiguration:
    global env
    env = "staging"

    def get_driver(self):
        if platform == "linux" or platform == "linux2":
            return webdriver.Chrome(
                os.path.join(os.getcwd(),
                             "driver", "executable", "chromedriver"))
        elif platform == "win32":
            return webdriver.Chrome(
                os.path.join(os.getcwd(),
                             "driver", "executable", "chromedriver.exe"))

    @staticmethod
    def get_url():
        base_url = "https://lite-internal-frontend-"+env+".london.cloudapps.digital/"
        return base_url

    @staticmethod
    def get_exporter_url():
        ex_url = "https://lite-exporter-frontend-"+env+".london.cloudapps.digital/"
        return ex_url

