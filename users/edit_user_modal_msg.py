import unittest
import time
import json
from random import randint
from util.config import ModelConfig
from util.functions import db_functions, logout, login
from util.functions import screenshot


users = '''
        [  
         {"email" : "ema5646@gmail.com", "password" : "11122331546:", "confirm_password" :  "11122331546:", 
          "name" : "Ema Cruz Garcia"},  
         {"email" : "irma9647@gmail.com", "password" : "I945579546_?:", "confirm_password" :  "I945579546_?:", 
          "name" : "Irma Gonzalez Mora"}               
        ]'''


class EditModal(unittest.TestCase):

    def setUp(self):
        global users
        self.driver = ModelConfig.driver_web

        # Preparation of environment

        info = json.loads(users)
        # rand=randint(0, len(info)-1)  # to send the JSON logs
        code = """
                
info = {0}
cur.execute("DELETE FROM users WHERE email = '%s'" % info[0]['email'])
cur.execute("DELETE FROM admin_historicaluser WHERE email = '%s'" % user['email'])
sql = 'INSERT INTO users (name, password, status, email, created_at, updated_at, is_active, is_client)' \
      ' VALUES (%s, %s, %s, %s, current_timestamp, current_timestamp, %s,) returning email'
val = (info[0]['name'], info[0]['password'], '1', info[0]['email'], 'true', 'false')
cur.execute(sql, val)
# print the returned value
print(cur.fetchone()[0])
""".format(info)
        db_functions(code)

    def test_edit_user_bd(self):
        global users

        info = json.loads(users)
        driver = self.driver

        # Login

        login(self)
        time.sleep(3)

        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)

        # Search user

        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(info[0]['email'])
        time.sleep(5)

        # Edit the status

        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr/td[4]/a[1]/i').click()
        time.sleep(5)
        driver.find_element_by_css_selector('#form-edit #edit-form-status').click()
        aleatory = randint(0, 2)
        driver.find_element_by_css_selector('#form-edit #edit-form-status> option[value="%d"]' % aleatory).click()
        print(driver.find_element_by_xpath('//*[@id="form-edit"]/span').get_attribute('innerHTML'))

        # Add assert

        # self.assertIn("Raw passwords are not stored, so there is no way to see this user's password,"
        #               "but you can change the password using this",
        #               driver.find_element_by_xpath('//*[@id="form-edit"]/span/').get_attribute('innerHTML'), msg=None)
        # time.sleep(10)

        driver.find_element_by_css_selector('#form-edit > span > a').click()
        time.sleep(3)
        driver.find_element_by_css_selector('#form-change #change-pwd-password1').clear()
        driver.find_element_by_css_selector('#form-change #change-pwd-password1').send_keys(info[0]["password"])
        time.sleep(3)
        self.assertIn("Your password can't be too similar to your other personal information.",
                      driver.find_element_by_xpath('//*[@id="form-change"]/div[1]/ul/li[1]')
                      .get_attribute('innerHTML'), msg=None)
        time.sleep(3)
        self.assertIn("Your password must contain at least 8 characters.",
                      driver.find_element_by_xpath('//*[@id="form-change"]/div[1]/ul/li[2]')
                      .get_attribute('innerHTML'), msg=None)
        time.sleep(3)
        self.assertIn("Your password can't be a commonly used password.",
                      driver.find_element_by_xpath('//*[@id="form-change"]/div[1]/ul/li[3]')
                      .get_attribute('innerHTML'), msg=None)
        time.sleep(3)
        self.assertIn("Your password can't be entirely numeric.",
                      driver.find_element_by_xpath('//*[@id="form-change"]/div[1]/ul/li[4]')
                      .get_attribute('innerHTML'), msg=None)
        time.sleep(3)
        driver.find_element_by_css_selector('#form-change #change-pwd-password2').clear()
        driver.find_element_by_css_selector('#form-change #change-pwd-password2').send_keys(info[0]["password"])
        driver.find_element_by_xpath('//*[@id="modal-change-pwd"]/div/div/div[3]/button').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(2)
        # Screenshot

        path = "/users/screenshot/edit/"
        screenshot(self, path)
        time.sleep(2)

        # Search user

        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(info[0]['email'])
        time.sleep(5)

        # Edit the name

        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr/td[4]/a[1]/i').click()
        time.sleep(5)
        driver.find_element_by_css_selector('#form-edit #edit-form-name').clear()
        driver.find_element_by_css_selector('#form-edit #edit-form-name').send_keys(info[0]["name"])
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(2)

        # Screenshot

        screenshot(self, path)

        # Search user

        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(info[0]['email'])
        time.sleep(5)

        # Edit the email

        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr/td[4]/a[1]/i').click()
        time.sleep(5)
        driver.find_element_by_css_selector('#form-edit #edit-form-email').clear()
        driver.find_element_by_css_selector('#form-edit #edit-form-email').send_keys(info[0]["email"])
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(2)

        # Screenshot

        path = "/users/screenshot/add/"
        screenshot(self, path)

    def tearDown(self):
        logout(self)

        self.driver.close()


if __name__ == "__main__":
    unittest.main()
