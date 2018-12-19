import unittest
from util.functions import ModelConfig, sleep, screenshot

email_inexist = "sonia.amezcua1@varangard.com"
password_inexist = "123"
class ValidateLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = ModelConfig.driver_web
        driver = cls.driver
        driver.get(ModelConfig.url_login)

    def test_data_required(self):
        driver = self.driver
        path = "login/screenshot/test_data_required"
        self.assertEqual("We are", driver.find_element_by_xpath('//*[@id="we"]')
                         .text, msg=None)
        self.assertEqual("Cerebro Smart Media", driver.find_element_by_xpath('//*[@id="content"]/h2')
                         .text, msg=None)
        self.assertEqual("Please login to your account", driver.find_element_by_xpath('//*[@id="subtitle"]')
                         .text, msg=None)
        self.assertEqual("keep me signed in", driver.find_element_by_xpath('//*[@id="container_remember"]/label')
                         .text, msg=None)
        self.assertEqual("Forgot password?", driver.find_element_by_xpath('//*[@id="content"]/p/a')
                         .text, msg=None)
        driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()
        sleep(2)
        self.assertEqual("Email is required", driver.find_element_by_xpath('//*[@id="formLogin"]/div[1]/span')
                         .text, msg=None)
        screenshot(self, path)

    def test_format_email(self):
        driver = self.driver
        path = "login/screenshot/test_format_email"
        sleep(3)
        driver.find_element_by_xpath('//*[@id="id_username"]').clear()
        driver.find_element_by_xpath('//*[@id="id_username"]').send_keys("sonia.amezcua")
        driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()
        sleep(1)
        self.assertEqual('Invalid email format',
                         driver.find_element_by_css_selector('#formLogin > div.form-group.has-error > span')
                         .text, msg=None)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_username"]').clear()
        driver.find_element_by_xpath('//*[@id="id_username"]').send_keys("sonia.amezcua@")
        driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()
        sleep(1)
        self.assertEqual('Invalid email format',
                         driver.find_element_by_css_selector('#formLogin > div.form-group.has-error > span')
                         .text, msg=None)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_username"]').clear()
        driver.find_element_by_xpath('//*[@id="id_username"]').send_keys("sonia.amezcua@varangard.")
        driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()
        sleep(1)
        self.assertEqual('Invalid email format',
                         driver.find_element_by_css_selector('#formLogin > div.form-group.has-error > span')
                         .text, msg=None)
        screenshot(self, path)
    sleep(1)
    # driver.find_element_by_xpath('//*[@id="id_username"]').clear()
    # driver.find_element_by_xpath('//*[@id="id_username"]').send_keys("sonia.amezcua@varangard")
    # driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()
    # sleep(1)
    # self.assertEqual('Invalid email format',
    #                  driver.find_element_by_css_selector('#formLogin > div.form-group.has-error > span')
    #                  .text, msg=None)
    # screenshot(self, path)
    # sleep(5)

    def test_incorrect_data(self):
        driver = self.driver
        path = "login/screenshot/test_incorrect_data"
        sleep(2)
        driver.find_element_by_xpath('//*[@id="id_username"]').clear()
        driver.find_element_by_xpath('//*[@id="id_username"]').send_keys(email_inexist)
        driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(password_inexist)
        driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()
        sleep(2)
        self.assertEqual("Your username and password didn't match.\nPlease try again.",
                         driver.find_element_by_xpath('//*[@id="formLogin"]/p').text, msg=None)
        screenshot(self, path)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="id_username"]').clear()
        driver.find_element_by_xpath('//*[@id="id_username"]').send_keys(ModelConfig.email)
        driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(password_inexist)
        driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()
        sleep(2)
        self.assertEqual("Your username and password didn't match.\nPlease try again.",
                         driver.find_element_by_xpath('//*[@id="formLogin"]/p').text, msg=None)
        screenshot(self, path)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="id_username"]').clear()
        driver.find_element_by_xpath('//*[@id="id_username"]').send_keys(email_inexist)
        driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(ModelConfig.password)
        driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()
        sleep(2)
        self.assertEqual("Your username and password didn't match.\nPlease try again.",
                         driver.find_element_by_xpath('//*[@id="formLogin"]/p').text, msg=None)
        screenshot(self, path)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == '__main__':
    unittest.main()
