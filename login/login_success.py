import unittest
from util.functions import ModelConfig, logout, screenshot


class LoginSuccess(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web

    def test_login_success(self):
        driver = self.driver
        path = "login/screenshot/test_login_success"
        driver.get(ModelConfig.url_login)
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
        driver.find_element_by_xpath('//*[@id="id_username"]').send_keys(ModelConfig.email)
        driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(ModelConfig.password)
        screenshot(self, path)
        driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()
        self.assertIn(ModelConfig.base_url + "/admin/clients/?next=/admin/login/", driver.current_url, msg=None)
        self.assertEqual("Clients", driver.find_element_by_xpath('//*[@id="logo-user"]')
                         .text.capitalize(), msg=None)
        screenshot(self, path)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
