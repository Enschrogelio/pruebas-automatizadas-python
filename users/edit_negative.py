import unittest
import time
from selenium import webdriver
from util.login import *
from util.config import *


class EditNegative(unittest.TestCase):

    @classmethod
    def setUpClass(self):
       self.driver = ModelConfig.driver_web


    def test_no_email_edit(self):
        driver = self.driver

       # assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[10]/td[4]/a[1]/i').click()
        time.sleep(2)
        driver.find_element_by_css_selector("#form-edit #id_email").clear()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        self.assertEqual("Complete this field.",driver.find_element_by_css_selector('#form-edit > div.form-group.has-error > span').get_attribute('innerText' ), msg=None)
        path = "/users/screenshot/add/"
        screenshot(self, path)


    def test_no_name_edit(self):
        driver = self.driver
       # Login.testlogin(self)
       # time.sleep(3)
       # assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[6]/td[4]/a[1]/i').click()
        time.sleep(2)
        driver.find_element_by_css_selector("#form-edit #id_name").clear()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(2)
        self.assertEqual("This field is empty.",driver.find_element_by_css_selector("#form-edit > div.form-group.has-error > span").get_attribute('innerText' ), msg=None)
        path = "/users/screenshot/add/"
        screenshot(self, path)


    def test_special_keys_name(self):
        driver = self.driver
        #Login.testlogin(self)
        #time.sleep(2)
        #assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[6]/td[4]/a[1]/i').click()
        time.sleep(2)
        driver.find_element_by_css_selector("#form-edit #id_name").clear()
        time.sleep(2)
        driver.find_element_by_css_selector("#form-edit #id_name").send_keys(")=/%$&()/%$$$$$")
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(2)
        self.assertEqual("Please enter a valid name.",driver.find_element_by_xpath("#form-edit > div.form-group.has-error > span").get_attribute('innerText' ), msg=None)
        path = "/users/screenshot/add/"
        screenshot(self, path)





    def test_email_not_full(self):
        driver = self.driver
       # Login.testlogin(self)
        #time.sleep(2)
        #assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[6]/td[4]/a[1]/i').click()
        time.sleep(2)
        driver.find_element_by_css_selector("#form-edit #id_email").clear()
        time.sleep(2)
        driver.find_element_by_css_selector("#form-edit #id_email").send_keys("holatest.com")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(3)
        self.assertEqual("Please enter a valid email address.",driver.find_element_by_xpath("//*[@id='form-edit']/div[1]/span").get_attribute('innerText' ), msg=None)
        path = "/users/screenshot/add/"
        screenshot(self, path)


    def test_email_doublea(self):
        driver = self.driver
       # Login.testlogin(self)
        time.sleep(2)
        self.assertIn("http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/", driver.current_url,
                      msg=None)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[6]/td[4]/a[1]/i').click()
        time.sleep(2)
        driver.find_element_by_css_selector("#form-edit #id_email").clear()
        time.sleep(2)
        driver.find_element_by_css_selector("#form-edit #id_email").send_keys("holatest@cq@.com")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(3)
        self.assertEqual("Please enter a valid email address.",driver.find_element_by_xpath("//*[@id='form-edit']/div[1]/span").get_attribute('innerText' ), msg=None)
        path = "/users/screenshot/add/"
        screenshot(self, path)


    def test_email_change_order(self):
        driver = self.driver
        login(self)
        time.sleep(2)
        self.assertIn("http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/", driver.current_url,
                  msg=None)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[6]/td[4]/a[1]/i').click()
        time.sleep(3)
        driver.find_element_by_css_selector("#form-edit #id_email").clear()
        time.sleep(2)
        driver.find_element_by_css_selector("#form-edit #id_email").send_keys("holatest.com@hotmail")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(3)
        self.assertEqual("Enter a valid email address.",driver.find_element_by_xpath("//*[@id='form-edit']/div[1]/span").get_attribute('innerText' ), msg=None)
        path = "/users/screenshot/add/"
        screenshot(self, path)
        driver.refresh()



    def test_email_plain_text(self):
        driver = self.driver
      #  Login.testlogin(self)
      #  time.sleep(2)
      #  assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[6]/td[4]/a[1]/i').click()
        time.sleep(2)
        driver.find_element_by_css_selector("#form-edit #id_email").clear()
        time.sleep(2)
        driver.find_element_by_css_selector("#form-edit #id_email").send_keys("holatest")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(3)
        self.assertEqual("Please enter a valid email address.",driver.find_element_by_xpath("//*[@id='form-edit']/div[1]/span").get_attribute('innerText' ), msg=None)
        path = "/users/screenshot/add/"
        screenshot(self, path)



    @classmethod
    def tearDownClass(cls):
        cls.driver.close()



if __name__ == "__main__":
    unittest.main()
