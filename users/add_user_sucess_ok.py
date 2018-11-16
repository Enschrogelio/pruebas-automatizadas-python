import unittest
import time
from selenium import webdriver
import json
from random import randint
from util.config import *
from util.functions import db_functions, logout, login
from util.functions import screenshot


class AddUser(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web

    def testAddUsersSuccess(self):
        users = '''
        [{"email" : "karla27@gmail.com", "password" : "1122244484545:", "confirm_password" :  "1122244484545:", 
          "name" : "Karla Martinez Chavez"},
         {"email" : "margarita28@gmail.com", "password" : "9876432112345678?", "confirm_password" :  "9876432112345678?", 
          "name" : "Margarita Chavez Flores"},
         {"email" : "elizabeth01@gmail.com", "password" : "5655fjg56454?", "confirm_password" :  "5655fjg56454?", 
          "name" : "Elizabeth Gonzalez Acosta"}
        ]'''

        info = json.loads(users)
        rand=randint(0, len(info)-1)  # to send the JSON logs

        driver = self.driver
        time.sleep(3)
        login(self)

        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)

        # Add users

        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="id_email"]').send_keys(info[rand]['email'])
        driver.find_element_by_xpath('//*[@id="id_password1"]').send_keys(info[rand]['password'])
        driver.find_element_by_xpath('//*[@id="id_password2"]').send_keys(info[rand]['confirm_password'])
        driver.find_element_by_xpath('//*[@id="id_name"]').send_keys(info[rand]['name'])
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        time.sleep(2)

        # Screenshot

        path = "/users/screenshot/add/"
        screenshot(self, path)

        driver.refresh()

        # Read modal messages

        assert "Record successfully added" not in driver.page_source

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
