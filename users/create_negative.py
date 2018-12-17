import unittest
import time
from util.functions import *
from util.config import *


class CreateNegative(unittest.TestCase):

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
        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        time.sleep(2)

    def test_bad_mail(self):
        driver = self.driver
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("admin")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        time.sleep(2)
        self.assertEqual("Enter valid email.",driver.find_element_by_xpath('//*[@id="form-add"]/div[1]/span').get_attribute('innerText' ), msg=None)
        driver.refresh()

    # no muestra el mensaje, y corta la ejecucion
    def test_equal_badpass (self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-name"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("mail1@gmail.com")
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').send_keys("123456")
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').send_keys("678901")
        driver.find_element_by_xpath('//input[@id="add-form-name"]').send_keys("señor tester")
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        time.sleep(2)
        self.assertEqual("The two password fields didn't match.",driver.find_element_by_xpath('//*[@id="form-add"]/div[3]/span').get_attribute('innerText' ), msg=None)
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[1]/button').click()
        driver.refresh()

    def test_short_pass(self):
        driver = self.driver
    # codigo comentado, debido a que no muestra el mensaje, y corta la ejecucion
        time.sleep(2)
    #      # assert "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/" in driver.current_url
    #      # driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
    #      # driver.find_element_by_xpath('//*[@id="btn-add"]').click()
    #      time.sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-name"]').clear()
    #      driver.find_element_by_css_selector("#form-add #id_email").clear()
    #      driver.find_element_by_css_selector("#form-add #id_password1").clear()
    #      driver.find_element_by_css_selector("#form-add #id_password2").clear()
    #      driver.find_element_by_css_selector("#form-add #id_name").clear()
    #      time.sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("test@tester.com")
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').send_keys("1234")
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').send_keys("1234")
        driver.find_element_by_xpath('//input[@id="add-form-name"]').send_keys("tester")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[1]/button').click()
        time.sleep(2)
        self.assertEqual("This password is too short. It must contain at least 8 characters.",driver.find_element_by_xpath('//*[@id="form-add"]/div[3]/span').get_attribute('innerText' ), msg=None)

        driver.refresh()

    def test_easy_pass(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("mail1@gmail.com")
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').send_keys("12345678")
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').send_keys("12345678")
        driver.find_element_by_xpath('//input[@id="add-form-name"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-name"]').send_keys("hola como estas")
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        time.sleep(2)
        self.assertEqual("This password is too common.",driver.find_element_by_xpath('//*[@id="form-add"]/div[3]/span').get_attribute('innerText' ), msg=None)
        driver.refresh()

    def test_no_fields_create(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-name"]').clear()
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        time.sleep(1)
        self.assertEqual("This field is empty.",driver.find_element_by_xpath('//div[1]/span[@class="help-block help-block--bottom" and 1]').get_attribute('innerText'), msg=None)
        time.sleep(1)
        self.assertEqual("This field is empty.",driver.find_element_by_xpath('//div[2]/span[@class="help-block help-block--bottom" and 1]').get_attribute('innerText'), msg=None)
        time.sleep(1)
        self.assertEqual("This field is empty.",driver.find_element_by_xpath('//div[3]/span[@class="help-block help-block--bottom" and 1]').get_attribute('innerText'), msg=None)
        time.sleep(1)
        self.assertEqual("This field is empty.",driver.find_element_by_xpath('//div[4]/span[@class="help-block help-block--bottom" and 1]').get_attribute('innerText'), msg=None)
        # self.assertEqual("This field is empty.",driver.find_element_by_css_selector('#form-add > div:nth-child(2) > span').get_attribute('innerText' ), msg=None)
        # self.assertEqual("This field is empty.",driver.find_element_by_css_selector('#form-add > div:nth-child(3) > span').get_attribute('innerText' ), msg=None)
        # self.assertEqual("This field is empty.",driver.find_element_by_css_selector('#form-add > div:nth-child(4) > span').get_attribute('innerText' ), msg=None)
        # self.assertEqual("This field is empty.",driver.find_element_by_css_selector('#form-add > div:nth-child(5) > span').get_attribute('innerText' ), msg=None)
        driver.refresh()

    def test_special_keys_name(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-name"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("testing6@hotmail.com")
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').send_keys("holatest")
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').send_keys("holatest")
        driver.find_element_by_xpath('//input[@id="add-form-name"]').send_keys("%$TR&$#&&#$$!$#%")
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        time.sleep(1)
        self.assertEqual("Please enter a valid name.",driver.find_element_by_xpath('//div[4]/span[@class="help-block help-block--bottom" and 1]').get_attribute('innerText' ), msg=None)
        driver.refresh()

    def test_email_not_full(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        time.sleep(1)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("holatest.com")
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').send_keys("holatest")
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').send_keys("holatest")
        driver.find_element_by_xpath('//input[@id="add-form-name"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-name"]').send_keys("Jonathan test")
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        self.assertEqual("Enter valid email",driver.find_element_by_css_selector('#form-add > div:nth-child(2) > span').get_attribute('innerText' ), msg=None)
        driver.refresh()

    def test_email_doublea(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        # driver.find_element_by_css_selector("#form-add #id_email").clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("holatest@cq@.com")
        # driver.find_element_by_css_selector("#form-add #id_email").send_keys("holatest@cq@.com")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        time.sleep(3)
        self.assertEqual("Please enter a valid email address.",driver.find_element_by_xpath("//*[@id='form-add']/div[1]/span").get_attribute('innerText' ), msg=None)
        driver.refresh()

       # Falla porque no sale msj de error
    def test_email_change_order(self):
        driver = self.driver
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("holatest.com@hotmail")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        time.sleep(3)
        self.assertEqual("Enter a valid email address.",driver.find_element_by_xpath("//*[@id='form-edit']/div[1]/span").get_attribute('innerText' ), msg=None)
        driver.refresh()

    def test_email_plain_text(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        # driver.find_element_by_css_selector("#form-add #id_email").clear()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("holatest")
        # driver.find_element_by_css_selector("#form-add #id_email").send_keys("holatest")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        time.sleep(3)
        self.assertEqual("Please enter a valid email address.",driver.find_element_by_xpath("//*[@id='form-add']/div[1]/span").get_attribute('innerText' ), msg=None)
        driver.refresh()


    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
