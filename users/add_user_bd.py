import json
import time
import unittest
from random import randint

from util.config import ModelConfig
from util.functions import db_functions, logout, login
from util.functions import screenshot


class AddUserBd(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web

    def testAddUsersSuccess(self):
        users = '''
        [{"email" : "fernanda222@gmail.com", "password" : "2233445:", "confirm_password" : "2233445:",
          "name" : "Fernanda Rodriguez Martinez"},
         {"email" : "cesar444@gmail.com", "password" : "46546554?¡", "confirm_password" : "46546554?¡", 
          "name" : "Cesar Perez Lopez"},
         {"email" : "anita78@gmail.com", "password" : "97744552121?", "confirm_password" : "97744552121?", 
          "name" : "Anita Rodriguez Perez"}
        ]'''
        info = json.loads(users)
        rand = randint(0, len(info)-1)
        code = """
info = {0}
# Tour the json
for user in info: 
    cur.execute("DELETE FROM users WHERE email = '%s'" % user['email']) 
    cur.execute("DELETE FROM admin_historicaluser WHERE email = '%s'" % user['email'])
# print the returned value
print(cur.rowcount)
""".format(info)
        db_functions(code)

        driver = self.driver
        login(self)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)

        # Add user

        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="add-form-email"]').send_keys(info[rand]['email'])
        driver.find_element_by_xpath('//*[@id="add-form-password1"]').send_keys(info[rand]['password'])
        driver.find_element_by_xpath('//*[@id="add-form-password2"]').send_keys(info[rand]['confirm_password'])
        driver.find_element_by_xpath('//*[@id="add-form-name"]').send_keys(info[rand]['name'])

        # Screenshot

        path = "/users/screenshot/add/"
        screenshot(self, path)
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        time.sleep(3)

        # driver.find_element_by_id('#parent_id').click()
        # time.sleep(2)

        # Screenshot

        screenshot(self, path)
        driver.refresh()

        # Search user

        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(info[rand]['email'])
        time.sleep(5)

        # Compare

        self.assertEqual(driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[1]/td[1]')
                         .get_attribute('innerHTML'), info[rand]['email'], msg=None)
        time.sleep(5)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[1]/td[2]')
                         .get_attribute('innerHTML'), info[rand]['name'], msg=None)
        time.sleep(5)
        logout(self)
        driver.find_element_by_xpath('//*[@id="id_username"]').send_keys(info[rand]['email'])
        driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(info[rand]['password'])
        driver.find_element_by_xpath('//*[@id="formLogin"]/button ').click()

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
