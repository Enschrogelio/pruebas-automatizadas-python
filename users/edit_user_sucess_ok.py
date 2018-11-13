import unittest
import time
from selenium import webdriver
import json
from random import randint
from cerebro.util.config import *
from cerebro.util.functions import logout
from cerebro.util.login import Login

class EditUser(unittest.TestCase):
    def setUp(self):
        self.driver = modelConfig.driverWeb

    def testEditUsersSuccess(self):
        users = '''
        [  
         {"email" : "ricardo647@gmail.com", "password" : "1112233584546?:", "confirm_password" :  "1112233584546?:", "name" : "Ricardo Mora Ortíz"},  
         {"email" : "irma9647@gmail.com", "password" : "I9454648_?¡:", "confirm_password" :  "I9454648_?¡:", "name" : "Irma González Mora"}               
        ]'''

        info = json.loads(users)
        rand=randint(0, len(info)-1)  #para mandar los registros del JSON

        driver = self.driver

        Login.testlogin(self)
        time.sleep(3)

        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)

        # búsqueda de usuario
        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys("richard321@outlook.com")
        time.sleep(5)

        # editar usuario

        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr/td[4]/a[1]/i').click()
        time.sleep(5)
        driver.find_element_by_css_selector('#form-edit #id_status').click()
        aleatorio=randint(0,2)
        driver.find_element_by_css_selector('#form-edit #id_status > option[value="%d"]' %aleatorio).click()
        print(driver.find_element_by_xpath('//*[@id="form-edit"]/span').get_attribute('innerHTML'))
        time.sleep(2)

        assert "Raw passwords are not stored, so there is no way to see this user's password, but you can change the password using this" in driver.find_element_by_xpath('//*[@id="form-edit"]/span').get_attribute('innerHTML')
        time.sleep(3)
        driver.find_element_by_css_selector('#form-edit > span > a').click()
        time.sleep(3)
        driver.find_element_by_css_selector('#form-change #id_password1').clear()
        driver.find_element_by_css_selector('#form-change #id_password1').send_keys("Jany123456?")
        time.sleep(3)
        driver.find_element_by_css_selector('#form-change #id_password2').clear()
        driver.find_element_by_css_selector('#form-change #id_password2').send_keys("Jany123456?")
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="modal-change-pwd"]/div/div/div[3]/button').click()

        assert "Record successfully updated" not in driver.page_source
        time.sleep(3)

    def tearDown(self):
        logout(self)
        self.driver.close()

if __name__== "__main__":
    unittest.main()