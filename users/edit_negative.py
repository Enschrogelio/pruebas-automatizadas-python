import json
import unittest
from time import sleep

from util.config import ModelConfig
from util.functions import db_functions, login

users = '''
        [  
         {"email" : "ema5646@gmail.com", "password" : "11122331546:", "confirm_password" :  "11122331546:", 
          "name" : "Ema Cruz Garcia"},  
         {"email" : "irma9647@gmail.com", "password" : "I945579546_?:", "confirm_password" :  "I945579546_?:", 
          "name" : "Irma Gonzalez Mora"}               
        ]'''


class EditNegative(unittest.TestCase):

    # noinspection PyCallByClass,PyTypeChecker
    @classmethod
    def setUpClass(cls):
        global users
        cls.driver = ModelConfig.driver_web
        info = json.loads(users)
        code = """
info = {0}
cur.execute("DELETE FROM users WHERE email = '%s'" % info[0]['email'])
cur.execute("DELETE FROM admin_historicaluser WHERE email = '%s'" % info[0]['email'])
sql = 'INSERT INTO users (name, password, status, email, created_at, updated_at, is_active, is_client)' \
      ' VALUES (%s, %s, %s, %s, current_timestamp, current_timestamp, %s, %s) returning email'
val = (info[0]['name'], info[0]['password'], '1', info[0]['email'], 'true', 'false')
cur.execute(sql, val)
    """.format(info)
        db_functions(code)
        cls.create_setup(cls)

    def create_setup(self):
        global users
        info = json.loads(users)
        driver = self. driver
        # Llamada a login
        login(self)
        self.assertIn(self, "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/",
                      driver.current_url)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        sleep(2)
        driver.find_element_by_xpath('//button[@id="inputSrc"]').click()
        sleep(1)
        driver.find_element_by_xpath('//input[@id="search"]').send_keys(info[0]['email'])
        sleep(2)
        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[1]/td[4]/a[1]/i').click()
        sleep(2)

    def test_no_email_edit(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').clear()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        self.assertEqual(driver.find_element_by_css_selector('#form-edit > div.form-group.has-error > span')
                         .get_attribute('innerText'), "This field is empty", msg=None)
        driver.refresh()

    def test_no_name_edit(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').send_keys("automatedtest@gmail.com")
        driver.find_element_by_xpath('//input[@id="edit-form-name"]').clear()
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        sleep(2)
        self.assertEqual(driver.find_element_by_css_selector("#form-edit > div.form-group.has-error > span")
                         .get_attribute('innerText'), "This field is empty", msg=None)
        driver.refresh()

    def test_email_not_full(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').send_keys("Holatest.com")
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        sleep(2)
        self.assertEqual(driver.find_element_by_xpath("//*[@id='form-edit']/div[1]/span").get_attribute('innerText'),
                         "Enter a valid mail", msg=None)
        driver.refresh()

    def test_email_double(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').send_keys("holatest@cq@.com")
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        sleep(2)
        self.assertEqual(driver.find_element_by_xpath("//*[@id='form-edit']/div[1]/span").get_attribute('innerText'),
                         "Enter a valid mail", msg=None)
        driver.refresh()

    def test_email_change_order(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').send_keys("holatest.com@hotmail")
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        sleep(1)
        self.assertEqual(driver.find_element_by_css_selector("#form-edit > div.form-group.has-error > span")
                         .get_attribute('innerText'), "Enter a valid mail", msg=None)
        driver.refresh()

    def test_email_plain_text(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').send_keys("holatest")
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        sleep(2)
        self.assertEqual(driver.find_element_by_xpath("//*[@id='form-edit']/div[1]/span").get_attribute('innerText'),
                         "Enter a valid mail", msg=None)
        driver.refresh()

    def test_password_short(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_link_text('form').click()
        sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').send_keys("short")
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').send_keys("short")
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]"
                                     "/div[@class='modal-box' and 1]/div[3]/button[1]").click()
        sleep(2)
        self.assertEqual(driver.find_element_by_xpath('//span[@class="help-block"]').get_attribute('innerText'),
                         "This password is too short. It must contain at least 8 characters.", msg=None)
        driver.refresh()

    def test_password_common(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_link_text('form').click()
        sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').send_keys("12345678")
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').send_keys("12345678")
        sleep(2)
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]"
                                     "/div[@class='modal-box' and 1]/div[3]/button[1]").click()
        sleep(2)
        self.assertEqual("This password is too common.", driver.find_element_by_xpath('//span[@class="help-block"]')
                         .get_attribute('innerText'), msg=None)
        driver.refresh()

    def test_password_numbers(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_link_text('form').click()
        sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').send_keys("10937361")
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').send_keys("10937361")
        sleep(2)
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]"
                                     "/div[@class='modal-box' and 1]/div[3]/button[1]").click()
        sleep(2)
        self.assertEqual(driver.find_element_by_xpath('//span[@class="help-block"]').get_attribute('innerText'),
                         "This password is entirely numeric.", msg=None)
        driver.refresh()

    def test_password_no_match(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_link_text('form').click()
        sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').send_keys("testnomatch")
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').send_keys("testnomat")
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]"
                                     "/div[@class='modal-box' and 1]/div[3]/button[1]").click()
        sleep(2)
        self.assertEqual(driver.find_element_by_xpath('//span[@class="help-block"]').get_attribute('innerText'),
                         "The two password fields didn't match.", msg=None)
        driver.refresh()

    def test_password_empty(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_link_text('form').click()
        sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').clear()
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]"
                                     "/div[@class='modal-box' and 1]/div[3]/button[1]").click()
        sleep(2)
        self.assertEqual("This field is empty", driver.find_element_by_xpath('//*[@id="form-change"]/div[1]/span')
                         .get_attribute('innerText'), msg=None)
        self.assertEqual("This field is empty", driver.find_element_by_xpath('//*[@id="form-change"]/div[2]/span')
                         .get_attribute('innerText'), msg=None)
        driver.refresh()

    def test_password_similar_info(self):
        global users
        info = json.loads(users)
        driver = self.driver
        sleep(2)
        driver.find_element_by_link_text('form').click()
        sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').send_keys(info[0]['email'])
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').send_keys(info[0]['email'])
        sleep(2)
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]"
                                     "/div[@class='modal-box' and 1]/div[3]/button[1]").click()
        sleep(2)
        self.assertEqual(driver.find_element_by_xpath('//span[@class="help-block"]').get_attribute('innerText'),
                         "The password is too similar to the email.", msg=None)
        driver.refresh()

    # noinspection PyUnresolvedReferences
    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
