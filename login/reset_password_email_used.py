import unittest

from util.functions import ModelConfig, screenshot, sleep

# Precondiciones:
# - Correo como primer registro en bandeja de entrada y cambiar valores de las variables email y password
# - Haber utilizado el correo y cambiado la contraseña
email = "arcapruebas@gmail.com"
password = 'pruebasarca1'


class ResetPasswordEmailSuccess(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()

    def test_reset_password_email(self):
        driver = self.driver
        path = "login/screenshot/test_reset_password_email"
        browser_name = self.driver.capabilities['browserName']

        driver.get('https://mail.google.com/mail/u/0/#inbox')

        sleep(8)
        driver.find_element_by_css_selector('#identifierId').send_keys(email)
        driver.find_element_by_css_selector('#identifierNext > content').click()
        sleep(5)
        driver.find_element_by_css_selector('#password > div > div > div > input')\
            .send_keys(password)
        driver.find_element_by_css_selector('#passwordNext > content').click()
        sleep(5)
        driver.find_element_by_xpath('//table/tbody/tr[1]/td[5]').click()
        sleep(10)
        self.assertIn("Password reset on",
                      driver.find_element_by_xpath('//*[@role="main"]/div/table/tr/td[1]/div[2]/div[1]/div[2]'
                                                   '/div[1]/h2').get_attribute("innerHTML"), msg=None)
        self.assertEqual("Hey there,", driver.find_element_by_xpath('//*[@role="listitem"]/div/div/div/div[1]/div[1]'
                                                                    '/div[2]/div[3]/div[3]/div[1]/div[2]/div[2]/h1')
                         .get_attribute("innerHTML"), msg=None)
        self.assertEqual("Someone requested a new password for you Cerebro account.",
                         driver.find_element_by_xpath('//*[@role="listitem"]/div/div/div/div[1]/div[1]'
                                                      '/div[2]/div[3]/div[3]/div[1]/div[2]/div[2]/p[1]')
                         .get_attribute("innerHTML"), msg=None)
        self.assertEqual("Reset Password",
                         driver.find_element_by_xpath('//*[@role="listitem"]/div/div/div/div[1]/div[1]'
                                                      '/div[2]/div[3]/div[3]/div[1]/div[2]/div[2]/a/h2')
                         .get_attribute("innerHTML"), msg=None)
        self.assertEqual("If you didn't make this request then you can safely ignore this email.",
                         driver.find_element_by_xpath('//*[@role="listitem"]/div/div/div/div[1]/div[1]'
                                                      '/div[2]/div[3]/div[3]/div[1]/div[2]/div[2]/p[2]')
                         .get_attribute("innerHTML"), msg=None)
        driver.find_element_by_xpath('//table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/'
                                     'div[2]/div[3]/div[3]/div/div[2]/div[2]/a/h2').click()
        screenshot(self, path)
        sleep(5)
        driver.switch_to.window(driver.window_handles[1])
        sleep(3)
        self.assertEqual("We are", driver.find_element_by_xpath('//*[@id="we"]')
                         .text, msg=None)
        self.assertEqual("Cerebro Smart Media", driver.find_element_by_xpath('//*[@id="content"]/h2')
                         .text, msg=None)
        self.assertEqual("Set new password", driver.find_element_by_xpath('//*[@id="subtitle"]')
                         .text, msg=None)
        self.assertEqual("The reset password link is no longer valid",
                         driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/div/div/strong')
                         .text, msg=None)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/div/a').text.upper(),
                         "GO BACK", msg=None)
        screenshot(self, path)
        driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/div/a').click()
        sleep(2)
        self.assertEqual("http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/login/", driver.current_url,
                         msg=None)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
