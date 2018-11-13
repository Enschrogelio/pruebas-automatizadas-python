import unittest
import time
from selenium import webdriver
import json
from random import randint
from cerebro.util.config import *
from cerebro.util.functions import logout
from cerebro.util.login import Login

class AddUser(unittest.TestCase):
    def setUp(self):
        self.driver = modelConfig.driverWeb

    def testAddUsersSuccess(self):
        users = '''
        [{"email" : "karla27@gmail.com", "password" : "1122244484545:", "confirm_password" :  "1122244484545:", "name" : "Karla Martínez Chávez"},
             {"email" : "margarita28@gmail.com", "password" : "9876432112345678?", "confirm_password" :  "9876432112345678?", "name" : "Margarit Chávez Bernal"},
             {"email" : "elizabeth97@gmail.com", "password" : "aajgfjg56454??", "confirm_password" :  "aajgfjg56454??", "name" : "Elizabeth González Acuña"}
        ]'''

        info = json.loads(users)
        rand=randint(0, len(info)-1)  #para mandar los registros del JSON

        driver = self.driver
        time.sleep(3)
        Login.testlogin(self)
        time.sleep(3)

        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)

        #agregar usuarios

        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="id_email"]').send_keys(info[rand]['email'])
        driver.find_element_by_xpath('//*[@id="id_password1"]').send_keys(info[rand]['password'])
        driver.find_element_by_xpath('//*[@id="id_password2"]').send_keys(info[rand]['confirm_password'])
        driver.find_element_by_xpath('//*[@id="id_name"]').send_keys(info[rand]['name'])
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        time.sleep(2)

        driver.refresh()

        #leer mensajes del modal

        assert "Record successfully added" not in driver.page_source
        # assert "texto" in driver.page_source

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__== "__main__":
    unittest.main()
