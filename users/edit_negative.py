import unittest
import time
import json
from util.functions import db_functions, login
from util.config import ModelConfig

users = '''
        [  
         {"email" : "ema5646@gmail.com", "password" : "11122331546:", "confirm_password" :  "11122331546:", 
          "name" : "Ema Cruz Garcia"},  
         {"email" : "irma9647@gmail.com", "password" : "I945579546_?:", "confirm_password" :  "I945579546_?:", 
          "name" : "Irma Gonzalez Mora"}               
        ]'''

class EditNegative(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global users
        cls.driver = ModelConfig.driver_web
        cls.create_setup(cls)
        # Preparation of environment

        info = json.loads(users)
        # rand=randint(0, len(info)-1)  # to send the JSON logs
        code = """
                
info = {0}
cur.execute("DELETE FROM users WHERE email = '%s'" % info[0]['email'])
cur.execute("DELETE FROM admin_historicaluser WHERE email = '%s'" % info[0]['email'])
sql = 'INSERT INTO users (name, password, status, email, created_at, updated_at, is_active, is_client)' \
      ' VALUES (%s, %s, %s, %s, current_timestamp, current_timestamp, %s, %s) returning email'
val = (info[0]['name'], info[0]['password'], '1', info[0]['email'], 'true', 'false')
cur.execute(sql, val)

# print the returned value
print(cur.fetchone()[0])
""".format(info)
        db_functions(code)

    def create_setup(self):
        global users
        info = json.loads(users)
        driver = self. driver
        #  Llamada a login
        login(self)
        self.assertIn(self,"http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/",
                      driver.current_url, msg=None)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)
        driver.find_element_by_xpath('//button[@id="inputSrc"]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//input[@id="search"]').send_keys(info[0]['email'])
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[1]/td[4]/a[1]/i').click()
        #driver.find_element_by_css_selector("#form-edit #id_email").clear()
        #driver.find_element_by_xpath('//i[@class="glyphicon glyphicon-pencil"]').click
        time.sleep(2)

    def test_no_email_edit(self):
        driver = self.driver
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').clear()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        self.assertEqual("This field is empty.",driver.find_element_by_css_selector
        ('#form-edit > div.form-group.has-error > span').get_attribute('innerText' ), msg=None)
        driver.refresh()

    def test_no_name_edit(self):
        driver = self.driver
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').clear()
        # driver.find_element_by_css_selector("#form-edit #id_email").clear()
        time.sleep(1)
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').send_keys("automatedtest@gmail.com")
        # driver.find_element_by_css_selector("#form-edit #id_email").send_keys("automatedtest@gmail.com")
        time.sleep(1)
        driver.find_element_by_xpath('//input[@id="edit-form-name"]').clear()
        # driver.find_element_by_css_selector("#form-edit #id_name").clear()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(2)
        self.assertEqual("This field is empty.",driver.find_element_by_css_selector
        ("#form-edit > div.form-group.has-error > span").get_attribute('innerText' ), msg=None)
        driver.refresh()

    def test_special_keys_name(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').clear()
        # driver.find_element_by_css_selector("#form-edit #id_email").clear()
        time.sleep(1)
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').send_keys("automatedtest@gmail.com")
        # driver.find_element_by_css_selector("#form-edit #id_email").send_keys("automatedtest@gmail.com")
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="edit-form-name"]').clear()
        # driver.find_element_by_css_selector("#form-edit #id_name").clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="edit-form-name"]').send_keys(")=/%$&()/%$$$$$")
        # driver.find_element_by_css_selector("#form-edit #id_name").send_keys(")=/%$&()/%$$$$$")
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(2)
        self.assertEqual("Please enter a valid name.",driver.find_element_by_css_selector
        ("#form-edit > div.form-group.has-error > span").get_attribute('innerText' ), msg=None)
        driver.refresh()

    def test_email_not_full(self):
        driver = self.driver
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').clear()
        # driver.find_element_by_css_selector("#form-edit #id_email").clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').send_keys("Holatest.com")
        # driver.find_element_by_css_selector("#form-edit #id_email").send_keys("holatest.com")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(3)
        self.assertEqual("Please enter a valid email address.",driver.find_element_by_xpath
        ("//*[@id='form-edit']/div[1]/span").get_attribute('innerText' ), msg=None)
        driver.refresh()

    def test_email_doublea(self):
        driver = self.driver
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').clear()
        # driver.find_element_by_css_selector("#form-edit #id_email").clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').send_keys("holatest@cq@.com")
        # driver.find_element_by_css_selector("#form-edit #id_email").send_keys("holatest@cq@.com")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(3)
        self.assertEqual("Please enter a valid email address.",driver.find_element_by_xpath
        ("//*[@id='form-edit']/div[1]/span").get_attribute('innerText' ), msg=None)
        driver.refresh()

    def test_email_change_order(self):
         driver = self.driver
         driver.find_element_by_xpath('//input[@id="edit-form-email"]').clear()
         #driver.find_element_by_css_selector("#form-edit #id_email").clear()
         time.sleep(2)
         driver.find_element_by_xpath('//input[@id="edit-form-email"]').send_keys("holatest.com@hotmail")
         # driver.find_element_by_css_selector("#form-edit #id_email").send_keys("holatest.com@hotmail")
         time.sleep(2)
         driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
         time.sleep(1)
         self.assertEqual("Enter a valid email address.",driver.find_element_by_css_selector
         ("#form-edit > div.form-group.has-error > span").get_attribute('innerText'), msg=None)
         driver.refresh()

    def test_email_plain_text(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').clear()
        # driver.find_element_by_css_selector("#form-edit #id_email").clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').send_keys("holatest")
        # driver.find_element_by_css_selector("#form-edit #id_email").send_keys("holatest")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(2)
        self.assertEqual("Please enter a valid email address.",driver.find_element_by_xpath(
            "//*[@id='form-edit']/div[1]/span").get_attribute('innerText' ), msg=None)
        driver.refresh()

    def test_password_short(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_link_text('form').click()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').send_keys("short")
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').send_keys("short")
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]"
                                     "/div[@class='modal-box' and 1]/div[@class='modal-footer col-md-12 ' and 3]"
                                     "/button[1]").click()
        time.sleep(2)
        self.assertEqual("This password is too short. It must contain at least 8 characters.",
                         driver.find_element_by_xpath('//span[@class="help-block"]').get_attribute('innerText'), msg=None)
        driver.refresh()

    def test_password_common(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_link_text('form').click()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').send_keys("12345678")
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').send_keys("12345678")
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]"
                "/div[@class='modal-box' and 1]/div[@class='modal-footer col-md-12 ' and 3]/button[1]").click()
        time.sleep(2)
        self.assertEqual("This password is too common.", driver.find_element_by_xpath('//span[@class="help-block"]')
                         .get_attribute('innerText'), msg=None)
        driver.refresh()

    def test_password_numbers(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_link_text('form').click()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').send_keys("10937361")
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').send_keys("10937361")
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]"
                 "/div[@class='modal-box' and 1]/div[@class='modal-footer col-md-12 ' and 3]/button[1]").click()
        time.sleep(2)
        self.assertEqual("This password is entirely numeric.", driver.find_element_by_xpath(
            '//span[@class="help-block"]').get_attribute('innerText'), msg=None)
        driver.refresh()

    def test_password_no_match(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_link_text('form').click()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').send_keys("testnomatch")
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').send_keys("testnomat")
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]"
                    "/div[@class='modal-box' and 1]/div[@class='modal-footer col-md-12 ' and 3]/button[1]").click()
        time.sleep(2)
        self.assertEqual("The two password fields didn't match.", driver.find_element_by_xpath
        ('//span[@class="help-block"]').get_attribute('innerText'), msg=None)
        driver.refresh()

    def test_password_empty(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_link_text('form').click()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]"
                     "/div[@class='modal-box' and 1]/div[@class='modal-footer col-md-12 ' and 3]/button[1]").click()
        time.sleep(2)
        self.assertEqual("This field is empty", driver.find_element_by_xpath('//span[@class="help-block"]')
                         .get_attribute('innerText'), msg=None)
        driver.refresh()

    def test_password_similar_info(self):
        global users
        info = json.loads(users)
        driver = self.driver
        time.sleep(2)
        #element=driver.find_element_by_xpath('//input[@id="edit-form-email"]')
        #passtext=element.text
        # print(NewPass)
        #time.sleep(1)
        driver.find_element_by_link_text('form').click()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="change-pwd-password1"]').send_keys(info[0]['email'])
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="change-pwd-password2"]').send_keys(info[0]['email'])
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]"
                                     "/div[@class='modal-box' and 1]/div[@class='modal-footer col-md-12 ' and 3]"
                                     "/button[1]").click()
        time.sleep(2)
        self.assertEqual("The password is too similar to the email.", driver.find_element_by_xpath('//span'
                        '[@class="help-block"]').get_attribute('innerText'), msg=None)
        driver.refresh()


    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
