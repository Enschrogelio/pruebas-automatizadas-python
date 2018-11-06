import string
from selenium import webdriver
import random
import time



class modelConfig:
    #config db
    conection = "dbname='cerebro'" \
                " user='cerebro'" \
                " host='cerebro-stage.ct2o8jgma4vs.us-west-2.rds.amazonaws.com' " \
                "password='N23E4Jz8KLRuSvGb' " \
                "connect_timeout=10"


    #atributos
    baseUrl="http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com"
    urlLogin=baseUrl+"/admin/login/"
    email="admin@admin.com"
    password="admin"
    #screenshot
    base_screenshot="C:/Users/x2/Desktop/cerebro/"

    #Drivers
    def drivers(x):
        #global x
        baseDriver="C:/Users/x2/Desktop/"
        if x=="ch":
            driver=webdriver.Chrome(baseDriver+"cerebro/util/drivers/chromedriver.exe")
            return driver
        else:
            if x=="fi":
                driver=webdriver.Firefox(executable_path=baseDriver+"cerebro/util/drivers/geckodriver.exe")
                return driver
            else:
                if x=="ie":
                    driver=webdriver.Ie(baseDriver+"cerebro/util/drivers/IEDriverServer.exe")
                    return driver
                else:
                    if x=="ed":
                        driver=webdriver.Edge(executable_path=baseDriver+"cerebro/util/drivers/MicrosoftWebDriver.exe")
                        return driver
                    else:
                        return None

    driverWeb=drivers("ch")






