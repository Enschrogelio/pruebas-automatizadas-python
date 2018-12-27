import unittest
from util.functions import ModelConfig, screenshot, sleep


class ResetPasswordSuccess(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web

    def test_reset_password(self):
        driver = self.driver
        path = "login/screenshot/test_reset_password"
        driver.get(ModelConfig.url_login)
        driver.find_element_by_xpath('//*[@id="content"]/p/a').click()
        sleep(2)
        self.assertIn(ModelConfig.base_url + "/admin/password_reset/", driver.current_url, msg=None)
        self.assertEqual("We are", driver.find_element_by_xpath('//*[@id="we"]')
                         .text, msg=None)
        self.assertEqual("Cerebro Smart Media", driver.find_element_by_xpath('//*[@id="content"]/h2')
                         .text, msg=None)
        self.assertEqual("Recover password", driver.find_element_by_xpath('//*[@id="subtitle"]')
                         .text, msg=None)
        self.assertEqual("We can help you reset your password and\nsecurity information. First write your "
                         "account\nand follow the instructions below.",
                         driver.find_element_by_css_selector('#content > p').text, msg=None)
        self.assertEqual("RESET MY PASSWORD", driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/button')
                         .text.upper(), msg=None)
        driver.find_element_by_xpath('//*[@id="id_email"]').send_keys(ModelConfig.email)
        screenshot(self, path)
        driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/button').click()
        sleep(2)
        self.assertIn(ModelConfig.base_url + "/admin/password_reset/done/", driver.current_url, msg=None)
        self.assertEqual("We are", driver.find_element_by_xpath('//*[@id="we"]')
                         .text, msg=None)
        self.assertEqual("Cerebro Smart Media", driver.find_element_by_xpath('//*[@id="content"]/h2')
                         .text, msg=None)
        self.assertEqual("We just sent you an email, run to check it",
                         driver.find_element_by_xpath('//*[@id="content"]/form/p').text, msg=None)
        self.assertEqual("GO BACK", driver.find_element_by_xpath('//*[@id="content"]/form/a').text.upper(), msg=None)
        screenshot(self, path)
        driver.find_element_by_xpath('//*[@id="content"]/form/a').click()
        sleep(2)
        self.assertIn(ModelConfig.base_url + "/admin/login/", driver.current_url, msg=None)
        screenshot(self, path)

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
