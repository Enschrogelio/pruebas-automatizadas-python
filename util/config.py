from selenium import webdriver

class modelConfig:
    #config db
    connection = "dbname='cerebro'" \
                " user='cerebro'" \
                " host='cerebro-stage.ct2o8jgma4vs.us-west-2.rds.amazonaws.com' " \
                "password='N23E4Jz8KLRuSvGb' " \
                "connect_timeout=10"

    #atributos
    baseUrl = "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com"
    urlLogin = baseUrl+"/admin/login/"
    email = "admin@admin.com"
    password = "admin"
    #screenshot
    base_screenshot = "D:/TC_VARANGAR/TC_AUTOMATE/cerebro/"
    #Drivers
    def drivers(x):
        #global x
        baseDriver = "D:/TC_VARANGAR/TC_AUTOMATE/"
        if x == "ch":
            driver = webdriver.Chrome(executable_path=baseDriver+"cerebro/util/drivers/chromedriver.exe")
            return driver
        else:
            if x == "fi":
                driver = webdriver.Firefox(executable_path=baseDriver+"cerebro/util/drivers/geckodriver.exe")
                return driver
            else:
                if x == "ie":
                    driver = webdriver.Ie(executable_path=baseDriver+"cerebro/util/drivers/IEDriverServer.exe")
                    return driver
                else:
                    if x == "ed":
                        driver = webdriver.Edge(executable_path=baseDriver+"cerebro/util/drivers/MicrosoftWebDriver.exe")
                        return driver
                    else:
                        return None

    driverWeb = drivers("ch")






