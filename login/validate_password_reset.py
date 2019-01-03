import unittest
from util.functions import ModelConfig, screenshot, sleep


class ValidatePasswordReset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = ModelConfig.driver_web
        driver = cls.driver
        driver.get(ModelConfig.url_login)

    def test_reset_data_required(self):
        driver = self.driver
        path = "login/screenshot/test_reset_data_required"
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
        driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/button').click()
        sleep(5)
        self.assertEqual("Completa este campo", driver.page_source)
        screenshot(self, path)

    def test_reset_format_email(self):
        driver = self.driver
        path = "login/screenshot/test_reset_format_email"
        driver.find_element_by_xpath('//*[@id="content"]/p/a').click()
        sleep(3)
        driver.find_element_by_xpath('//*[@id="id_email"]').clear()
        driver.find_element_by_xpath('//*[@id="id_email"]').send_keys("sonia.amezcua")
        driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/button').click()
        sleep(1)
        self.assertEqual('Incluye un signo "@" en la dirección de correo electrónico. '
                         'La dirección "sonia.amezcua" no incluye el signo "@".', driver.page_source)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_email"]').clear()
        driver.find_element_by_xpath('//*[@id="id_email"]').send_keys("sonia.amezcua@")
        driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/button').click()
        sleep(1)
        self.assertEqual('Invalid email format',
                         driver.find_element_by_css_selector('#formLogin > div.form-group.has-error > span')
                         .text, msg=None)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_email"]').clear()
        driver.find_element_by_xpath('//*[@id="id_email"]').send_keys("sonia.amezcua@varangard.")
        driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/button').click()
        sleep(1)
        self.assertEqual('Invalid email format',
                         driver.find_element_by_css_selector('#formLogin > div.form-group.has-error > span')
                         .text, msg=None)
        screenshot(self, path)
        sleep(1)
    # driver.find_element_by_xpath('//*[@id="id_email"]').clear()
    # driver.find_element_by_xpath('//*[@id="id_email"]').send_keys("sonia.amezcua@varangard")
    # driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/button').click()
    # sleep(1)
    # self.assertEqual('Invalid email format',
    #                  driver.find_element_by_css_selector('#formLogin > div.form-group.has-error > span')
    #                  .text, msg=None)
    # screenshot(self, path)
    # sleep(5)

    # noinspection PyUnresolvedReferences
    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
