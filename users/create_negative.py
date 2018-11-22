import unittest
import time
from selenium import webdriver
from util.functions import *
from util.config import *


class WrongMail(unittest.TestCase):
    def setUp(self):
        login(self)
        sleep(3)
        driver = self.driver
        self.assertIn("http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/", driver.current_url,
                  msg=None)

    def test_bad_mail(self):
         driver = self.driver
         Login.testlogin(self)
         time.sleep(2)
         assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
         driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
         time.sleep(2)
         driver.find_element_by_xpath('//*[@id="btn-add"]').click()
         time.sleep(2)
         driver.find_element_by_xpath('//*[@id="id_email"]').send_keys("admin")
         driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
         self.assertEqual("Enter valid email.",driver.find_element_by_xpath('//*[@id="form-add"]/div[1]/span').get_attribute('innerText' ), msg=None)

    def test_equal_badpass (self):
         driver = self.driver
         Login.testlogin(self)
         time.sleep(2)
         assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
         driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
         time.sleep(2)
         driver.find_element_by_xpath('//*[@id="btn-add"]').click()
         time.sleep(2)
         driver.find_element_by_xpath('//*[@id="id_email"]').send_keys("mail1@gmail.com")
         driver.find_element_by_xpath('//*[@id="id_password1"]').send_keys("123456")
         driver.find_element_by_xpath('//*[@id="id_password2"]').send_keys("6789")
         driver.find_element_by_xpath('//*[@id="id_name"]').send_keys("hola como estas")
         driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
         time.sleep(2)
         self.assertEqual("The two password fields didn't match.",driver.find_element_by_xpath('//*[@id="form-add"]/div[3]/span').get_attribute('innerText' ), msg=None)
         driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[1]/button').click()

    def test_special_keys(self):
         driver = self.driver
         time.sleep(2)
         assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
         driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
         driver.find_element_by_xpath('//*[@id="btn-add"]').click()
         time.sleep(2)
         driver.find_element_by_xpath('//*[@id="id_email"]').send_keys("mail1@gmail.com")
         driver.find_element_by_xpath('//*[@id="id_password1"]').send_keys("1234")
         driver.find_element_by_xpath('//*[@id="id_password2"]').send_keys("1234")
         driver.find_element_by_xpath('//*[@id="id_name"]').send_keys("hola como estas")
         driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
         time.sleep(2)
         self.assertEqual("This password is too short. It must contain at least 8 characters.",driver.find_element_by_xpath('//*[@id="form-add"]/div[3]/span').get_attribute('innerText' ), msg=None)
         driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[1]/button').click()

    def test_easy_pass(self):
         driver = self.driver
         time.sleep(2)
         assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
         driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
         driver.find_element_by_xpath('//*[@id="btn-add"]').click()
         time.sleep(2)
         driver.find_element_by_xpath('//*[@id="id_email"]').send_keys("mail1@gmail.com")
         driver.find_element_by_xpath('//*[@id="id_password1"]').send_keys("12345678")
         driver.find_element_by_xpath('//*[@id="id_password2"]').send_keys("12345678")
         driver.find_element_by_xpath('//*[@id="id_name"]').send_keys("hola como estas")
         driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
         time.sleep(2)
         self.assertEqual("This password is too common.",driver.find_element_by_xpath('//*[@id="form-add"]/div[3]/span').get_attribute('innerText' ), msg=None)



    def test_no_fields_create(self):
          driver = self.driver
          Login.testlogin(self)
          time.sleep(2)
          assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
          driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
          time.sleep(2)
          driver.find_element_by_xpath('//*[@id="btn-add"]').click()
          time.sleep(2)
          driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
          self.assertEqual("This field is empty.",driver.find_element_by_css_selector('#form-add > div:nth-child(2) > span').get_attribute('innerText' ), msg=None)
          self.assertEqual("This field is empty.",driver.find_element_by_css_selector('#form-add > div:nth-child(3) > span').get_attribute('innerText' ), msg=None)
          self.assertEqual("This field is empty.",driver.find_element_by_css_selector('#form-add > div:nth-child(4) > span').get_attribute('innerText' ), msg=None)
          self.assertEqual("This field is empty.",driver.find_element_by_css_selector('#form-add > div:nth-child(5) > span').get_attribute('innerText' ), msg=None)

    def test_special_keys_name(self):
       driver = self.driver
       Login.testlogin(self)
       time.sleep(2)
       assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
       driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
       time.sleep(2)
       driver.find_element_by_xpath('//*[@id="btn-add"]').click()
       time.sleep(2)
       driver.find_element_by_xpath('//*[@id="id_email"]').send_keys("testing@hotmail.com")
       driver.find_element_by_xpath('//*[@id="id_password1"]').send_keys("holatest")
       driver.find_element_by_xpath('//*[@id="id_password2"]').send_keys("holatest")
       driver.find_element_by_xpath('//*[@id="id_name"]').send_keys("%$TR&$#&&#$$!$#%")
       driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
       self.assertEqual("Please enter a valid name.",driver.find_element_by_css_selector('#form-add > div:nth-child(5) > span').get_attribute('innerText' ), msg=None)

    def test_email_not_full(self):
          driver = self.driver
          Login.testlogin(self)
          time.sleep(2)
          assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
          driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
          time.sleep(2)
          driver.find_element_by_xpath('//*[@id="btn-add"]').click()
          time.sleep(2)
          driver.find_element_by_xpath('//*[@id="id_email"]').send_keys("holatest.com")
          driver.find_element_by_xpath('//*[@id="id_password1"]').send_keys("holatest")
          driver.find_element_by_xpath('//*[@id="id_password2"]').send_keys("holatest")
          driver.find_element_by_xpath('//*[@id="id_name"]').send_keys("Jonathan test")
          driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
          self.assertEqual("Enter valid email",driver.find_element_by_css_selector('#form-add > div:nth-child(2) > span').get_attribute('innerText' ), msg=None)

    def test_email_doublea(self):
       driver = self.driver
       Login.testlogin(self)
       time.sleep(2)
       assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
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


    def test_email_change_order(self):
       driver = self.driver
       Login.testlogin(self)
       time.sleep(2)
       assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
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


    def test_email_plain_text(self):
       driver = self.driver
       Login.testlogin(self)
       time.sleep(2)
       assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
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



    def tearDown(cls):
         cls.driver.close()


if __name__ == "__main__":
    unittest.main()
