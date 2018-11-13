import unittest
import time
from selenium import webdriver
import json
from random import randint
from cerebro.util.config import *
from cerebro.util.login import Login

class edituser(unittest.TestCase):
    def setUp(self):
        self.driver = modelConfig.driverWeb

    def testEditUsersSuccess(self):
        users = '''
        [{"email" : "Pedro64@gmail.com", "password" : "Pedro987654", "confirm_password" :  "Pedro987654", "name" : "Pedro Cruz Ortíz"},  
         {"email" : "Juan4678@gmail.com", "password" : "Juan63547878?¡:", "confirm_password" :  "Juan63547878?¡:", "name" : "Juan Gómez Gómez"},  
         {"email" : "Javier36@gmail.com", "password" : "Javier65465987987:", "confirm_password" :  "Javier65465987987:", "name" : "Javier Aguirre Aguirre"}               
        ]'''

        info = json.loads(users)
        rand=randint(0, len(info)-1)  #para mandar los registros del JSON

        driver = self.driver
        Login.testlogin(self)

        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)

        assert "Raw passwords are not stored, so there is no way to see this user's password, but you can change the password using this" in driver.find_element_by_xpath('//*[@id="form-edit"]/span').get_attribute('innerHTML')
        time.sleep(3)
        driver.find_element_by_css_selector('#form-edit > span > a').click()
        time.sleep(3)

        assert "Change of password" in driver.find_element_by_xpath('//*[@id="modal-change-pwd"]/div/div/div[1]/h1').get_attribute('innerHTML')
        time.sleep(3)
        #driver.find_element_by_css_selector('#modal-change-pwd > div > div > div.modal-header > h1').click()

        assert "Your password must contain at least 8 characters." in driver.find_element_by_xpath('//*[@id="form-change"]/div[1]/ul/li[2]').get_attribute('innerHTML')
        time.sleep(3)

        assert "Your password can't be too similar to your other personal information." in driver.find_element_by_xpath('//*[@id="form-change"]/div[1]/ul/li[1]').get_attribute('innerHTML')
        time.sleep(3)

        assert "Your password can't be entirely numeric." in driver.find_element_by_xpath('//*[@id="form-change"]/div[1]/ul/li[4]').get_attribute('innerHTML')
        time.sleep(3)

    def tearDown(self):
        self.driver.close()

if __name__== "__main__":
    unittest.main()
