import unittest
import time
from selenium import webdriver
import json
from random import randint
from util.config import *
from util.functions import screenshot
from util.functions import db_functions, logout, login


class DeletedUser(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web

    def testDeletedUsersSuccess(self):
        users = '''
        [{"email" : "carlos967@gmail.com", "password" : "956541313187", "confirm_password" :  "956541313187",  
          "name" : "Carlos Gonzalez Acuna"},  
         {"email" : "ricardo647@gmail.com", "password" : "1112233584546?:", "confirm_password" :  "1112233584546?:", 
          "name" : "Ricardo Mora Ortiz"},  
         {"email" : "irma9647@gmail.com", "password" : "I9454648_?¡:", "confirm_password" :  "I9454648_?¡:", 
          "name" : "Irma Gonzalez Mora"}               
        ]'''

        info = json.loads(users)
        rand=randint(0, len(info)-1)  # to send the JSON logs
        driver = self.driver

        login(self)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)

        # Find user

        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys("letybernal3@outlook.com")
        time.sleep(5)

        # Remove user

        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr/td[4]/a[2]/i').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="modal-delete"]/div/div/div[3]/div[2]/button').click()
        time.sleep(4)
        driver.find_element_by_css_selector('#form-confirm #input-email').send_keys("letybernal3@outlook.com")
        time.sleep(4)
        driver.find_element_by_xpath('//*[@id="btn-submit"]').click()
        time.sleep(4)
        driver.refresh()
        time.sleep(4)

        # Screenshot

        path="/users/screenshot/add/"
        screenshot(self, path)

        # Find user

        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys("jegb02@gmail.com")
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr/td[4]/a[2]/i').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="modal-delete"]/div/div/div[3]/div[1]/button').click()
        time.sleep(4)

        # Screenshot

        screenshot(self, path)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

