import unittest
from util.functions import ModelConfig, logout, screenshot, sleep


class RedirectLoginSuccess(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web

    def test_redirect_login_success(self):
        driver = self.driver
        path = "login/screenshot/test_redirect_login_success"
        driver.get(ModelConfig.base_url + "/admin/client/update/1/")
        sleep(4)
        self.assertEqual("We are", driver.find_element_by_xpath('//*[@id="we"]')
                         .text, msg=None)
        self.assertEqual("Cerebro Smart Media", driver.find_element_by_xpath('//*[@id="content"]/h2')
                         .text, msg=None)
        self.assertEqual("Please login to see this page.", driver.find_element_by_xpath('//*[@id="subtitle"]')
                         .text, msg=None)
        self.assertEqual("keep me signed in", driver.find_element_by_xpath('//*[@id="container_remember"]/label')
                         .text, msg=None)
        self.assertEqual("Forgot password?", driver.find_element_by_xpath('//*[@id="content"]/p/a')
                         .text, msg=None)
        driver.find_element_by_xpath('//*[@id="id_username"]').send_keys(ModelConfig.email)
        driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(ModelConfig.password)
        screenshot(self, path)
        driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()
        sleep(4)
        self.assertIn(ModelConfig.base_url + "/admin/client/update/1/", driver.current_url, msg=None)
        sleep(4)
        screenshot(self, path)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
