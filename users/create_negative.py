import unittest
from time import sleep

from util.config import ModelConfig
from util.functions import login, logout


class CreateNegative(unittest.TestCase):

    # noinspection PyCallByClass,PyTypeChecker
    @classmethod
    def setUpClass(cls):
        cls.driver = ModelConfig.driver_web
        cls.create_setup(cls)

    def create_setup(self):
        driver = self.driver
        #  Llamada a login
        login(self)
        sleep(1)
        self.assertIn(self, "http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/?next=/admin/login/",
                      driver.current_url)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        sleep(2)
        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        sleep(2)

    def test_bad_mail(self):
        driver = self.driver
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("admin")
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        sleep(2)
        self.assertEqual("Enter a valid mail", driver.find_element_by_xpath('//*[@id="form-add"]/div[1]/span')
                         .get_attribute('innerText'), msg=None)

    def test_equal_bad_pass(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-name"]').clear()
        sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("mail1@gmail.com")
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').send_keys("123456")
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').send_keys("678901")
        driver.find_element_by_xpath('//input[@id="add-form-name"]').send_keys("señor tester")
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        sleep(2)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add"]/div[3]/span').get_attribute('innerText'),
                         "The two password fields didn't match.", msg=None)

    def test_short_pass(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-name"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("test@tester.com")
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').send_keys("1234")
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').send_keys("1234")
        driver.find_element_by_xpath('//input[@id="add-form-name"]').send_keys("tester")
        sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        sleep(2)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add"]/div[3]/span').get_attribute('innerText'),
                         "This password is too short. It must contain at least 8 characters.", msg=None)

    def test_easy_pass(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("mail1@gmail.com")
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').send_keys("12345678")
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').send_keys("12345678")
        driver.find_element_by_xpath('//input[@id="add-form-name"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-name"]').send_keys("hola como estas")
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        sleep(2)
        self.assertEqual("This password is too common.", driver.find_element_by_xpath('//*[@id="form-add"]/div[3]/span')
                         .get_attribute('innerText'), msg=None)

    def test_no_fields_create(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-name"]').clear()
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        sleep(1)
        self.assertEqual(driver.find_element_by_xpath('//div[1]/span[@class="help-block help-block--bottom" and 1]')
                         .get_attribute('innerText'), "This field is empty", msg=None)
        sleep(1)
        self.assertEqual(driver.find_element_by_xpath('//div[2]/span[@class="help-block help-block--bottom" and 1]')
                         .get_attribute('innerText'), "This field is empty", msg=None)
        sleep(1)
        self.assertEqual(driver.find_element_by_xpath('//div[3]/span[@class="help-block help-block--bottom" and 1]')
                         .get_attribute('innerText'), "This field is empty", msg=None)
        sleep(1)
        self.assertEqual(driver.find_element_by_xpath('//div[4]/span[@class="help-block help-block--bottom" and 1]')
                         .get_attribute('innerText'), "This field is empty", msg=None)

    def test_email_not_full(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        sleep(1)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("holatest.com")
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password1"]').send_keys("holatest")
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-password2"]').send_keys("holatest")
        driver.find_element_by_xpath('//input[@id="add-form-name"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-name"]').send_keys("Jonathan test")
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        self.assertEqual(driver.find_element_by_css_selector('#form-add > div:nth-child(2) > span')
                         .get_attribute('innerText'), "Enter a valid mail", msg=None)

    def test_email_double(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("holatest@cq@.com")
        sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        sleep(3)
        self.assertEqual(driver.find_element_by_xpath("//*[@id='form-add']/div[1]/span").get_attribute('innerText'),
                         "Enter a valid mail", msg=None)

    def test_email_change_order(self):
        driver = self.driver
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("holatest.com@hotmail")
        sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        sleep(3)
        self.assertEqual(driver.find_element_by_xpath("//*[@id='form-add']/div[1]/span").get_attribute('innerText'),
                         "Enter a valid mail", msg=None)

    def test_email_plain_text(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').clear()
        # driver.find_element_by_css_selector("#form-add #id_email").clear()
        sleep(2)
        driver.find_element_by_xpath('//input[@id="add-form-email"]').send_keys("holatest")
        # driver.find_element_by_css_selector("#form-add #id_email").send_keys("holatest")
        sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        sleep(3)
        self.assertEqual(driver.find_element_by_xpath("//*[@id='form-add']/div[1]/span").get_attribute('innerText'),
                         "Enter a valid mail", msg=None)

    # noinspection PyUnresolvedReferences
    @classmethod
    def tearDownClass(cls):
        logout(cls)
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
