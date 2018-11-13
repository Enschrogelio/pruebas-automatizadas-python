import os
from selenium import webdriver

root_files = os.path.dirname(os.path.abspath(__file__))+'\\'
base_driver = root_files+"drivers/"

class modelConfig:
    #atributos
    base_url = "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com"
    url_login = base_url+"/admin/login/"
    email = "admin@admin.com"
    password = "admin"
    connection = "dbname='cerebro'" \
                 " user='cerebro'" \
                 " host='cerebro-stage.ct2o8jgma4vs.us-west-2.rds.amazonaws.com' password='N23E4Jz8KLRuSvGb'" \
                 " connect_timeout=10 "

    #Screenshot
    base_screenshot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\'

    #Drivers
    def drivers(x):
        global root_driver
        if x == "ch":
            driver = webdriver.Chrome(base_driver+"chromedriver.exe")
            return driver
        else:
            if x == "fi":
                driver = webdriver.Firefox(executable_path=base_driver+"geckodriver.exe")
                return driver
            else:
                if x == "ie":
                    driver = webdriver.Ie(base_driver+"IEDriverServer.exe")
                    return driver
                else:
                    if x == "ed":
                        driver = webdriver.Edge(executable_path=base_driver+"MicrosoftWebDriver.exe")
                        return driver
                    else:
                        return None

    driver_web = drivers("ch")







