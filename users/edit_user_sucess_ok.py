import unittest
import time
from selenium import webdriver
import json
from random import randint
from util.config import *
from util.functions import logout


class EditUser(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web

    def testEditUsersSuccess(self, random=None):
        users = '''
        [  
         {"email": "ricardo647@gmail.com", "password": "111246?:", "confirm_password":  "111246?:", "name": "Ricardo"},  
         {"email": "irma9647@gmail.com", "password": "I945448_?¡:", "confirm_password":  "I945448_?¡:", "name": "Irma"}               
        ]'''

        info = json.loads(users)
        rand=randint(0, len(info)-1)  # Send the records

        driver = self.driver
        time.sleep(3)

        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)

        # User search

        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys("richard321@outlook.com")
        time.sleep(5)

        # Edit user

        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr/td[4]/a[1]/i').click()
        time.sleep(5)
        driver.find_element_by_css_selector('#form-edit #id_status').click()
        random=randint(0,2)
        driver.find_element_by_css_selector('#form-edit #id_status > option[value="%d"]' %random).click()
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


if __name__ == "__main__":
    unittest.main()