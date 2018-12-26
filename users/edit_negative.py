import unittest
import time
from util.functions import *
from util.config import *


class EditNegative(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = ModelConfig.driver_web
        cls.create_setup(cls)

    def create_setup(self):
        driver = self. driver
        #  Llamada a login
        login(self)
        self.assertIn(self,"http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/", driver.current_url,
                      msg=None)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[3]/td[4]/a[1]/i').click()
        time.sleep(2)

    def test_no_email_edit(self):
        driver = self.driver
        driver.find_element_by_xpath('//input[@id="edit-form-email"]').clear()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        self.assertEqual("This field is empty.",driver.find_element_by_css_selector('#form-edit > div.form-group.has-error > span').get_attribute('innerText' ), msg=None)
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
        self.assertEqual("This field is empty.",driver.find_element_by_css_selector("#form-edit > div.form-group.has-error > span").get_attribute('innerText' ), msg=None)
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
        self.assertEqual("Please enter a valid name.",driver.find_element_by_css_selector("#form-edit > div.form-group.has-error > span").get_attribute('innerText' ), msg=None)
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
        self.assertEqual("Please enter a valid email address.",driver.find_element_by_xpath("//*[@id='form-edit']/div[1]/span").get_attribute('innerText' ), msg=None)
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
        self.assertEqual("Please enter a valid email address.",driver.find_element_by_xpath("//*[@id='form-edit']/div[1]/span").get_attribute('innerText' ), msg=None)
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
         self.assertEqual("Enter a valid email address.",driver.find_element_by_css_selector("#form-edit > div.form-group.has-error > span").get_attribute('innerText'), msg=None)
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
        self.assertEqual("Please enter a valid email address.",driver.find_element_by_xpath("//*[@id='form-edit']/div[1]/span").get_attribute('innerText' ), msg=None)
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
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]/div[@class='modal-box' and 1]/div[@class='modal-footer col-md-12 ' and 3]/button[1]").click()
        time.sleep(2)
        self.assertEqual("This password is too short. It must contain at least 8 characters.", driver.find_element_by_xpath('//span[@class="help-block"]').get_attribute('innerText'), msg=None)
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
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]/div[@class='modal-box' and 1]/div[@class='modal-footer col-md-12 ' and 3]/button[1]").click()
        time.sleep(2)
        self.assertEqual("This password is too common.", driver.find_element_by_xpath('//span[@class="help-block"]').get_attribute('innerText'), msg=None)
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
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]/div[@class='modal-box' and 1]/div[@class='modal-footer col-md-12 ' and 3]/button[1]").click()
        time.sleep(2)
        self.assertEqual("This password is entirely numeric.", driver.find_element_by_xpath('//span[@class="help-block"]').get_attribute('innerText'), msg=None)
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
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]/div[@class='modal-box' and 1]/div[@class='modal-footer col-md-12 ' and 3]/button[1]").click()
        time.sleep(2)
        self.assertEqual("The two password fields didn't match.", driver.find_element_by_xpath('//span[@class="help-block"]').get_attribute('innerText'), msg=None)
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
        driver.find_element_by_xpath("//div[@id='modal-change-pwd']/div[@class='modal-dialog box' and 1]/div[@class='modal-box' and 1]/div[@class='modal-footer col-md-12 ' and 3]/button[1]").click()
        time.sleep(2)
        self.assertEqual("This field is empty", driver.find_element_by_xpath('//span[@class="help-block"]').get_attribute('innerText'), msg=None)
        driver.refresh()


    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
