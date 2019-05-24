import os
from selenium import webdriver

root_files = os.path.dirname(os.path.abspath(__file__))+'\\'
base_driver = root_files+"drivers/"


class ModelConfig:

    # Attributes
    base_url = ""
    url_login = base_url + "/admin/login/"
    email = ""
    password = ""
    connection = "dbname='' " \
                 "user='' " \
                 "host='' " \
                 "password='' " \
                 "connect_timeout=10 "

    # Screenshot
    base_screenshot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\'

    # Drivers
    def drivers(x):
        global root_driver
        if x == "ch":
            driver = webdriver.Chrome(base_driver+"chromedriver.exe")
            return driver
        elif x == "fi":
            driver = webdriver.Firefox(executable_path=base_driver+"geckodriver.exe")
            return driver
        elif x == "ie":
            driver = webdriver.Ie(base_driver+"IEDriverServer.exe")
            return driver
        elif x == "ed":
            driver = webdriver.Edge(executable_path=base_driver+"MicrosoftWebDriver.exe")
            return driver
        else:
            return None

    driver_web = drivers("ch")
