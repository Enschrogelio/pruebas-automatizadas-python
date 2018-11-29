import unittest
import time
import json
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

        # Send the records

        rand=randint(0, len(info)-1)
        code = """
           
info = {0}
# Tour the json
for user in info: 
    cur.execute("DELETE FROM users WHERE email = '%s'" % user['email']) 
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
        driver.find_element_by_xpath('//*[@id="id_email"]').send_keys(info[rand]['email'])
        driver.find_element_by_xpath('//*[@id="id_password1"]').send_keys(info[rand]['password'])
        driver.find_element_by_xpath('//*[@id="id_password2"]').send_keys(info[rand]['confirm_password'])
        driver.find_element_by_xpath('//*[@id="id_name"]').send_keys(info[rand]['name'])

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

        # Read modal messages

        # self.equals("Record successfully added",
        #               driver.find_element_by_css_selector('#form-group').get_attribute('innerHTML'),
        #               msg=None)
        # time.sleep(5)

        # time.sleep(3)
        # self.assertIn("Your password can't be too similar to your other personal information.",
        # driver.find_element_by_xpath('//*[@id="form-change"]/div[1]/ul/li[1]').get_attribute('innerHTML'), msg=None)

        # Search user

        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(info[0]['email'])
        time.sleep(5)

        # Compare

        self.assertEqual(driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[1]/td[1]')
                        .get_attribute('innerHTML'),info[rand]['email'], msg=None)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[1]/td[2]')
                         .get_attribute('innerHTML'),info[rand]['name'], msg=None)
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
