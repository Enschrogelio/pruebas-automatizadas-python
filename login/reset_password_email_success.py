import unittest

from util.functions import ModelConfig, screenshot, sleep, logout


class ResetPasswordEmailSuccess(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()

    def test_reset_password_email(self):
        driver = self.driver
        email = 'arcapruebas@gmail.com'
        password = '1a23456789'
        similary = 'arca1234'
        path = "login/screenshot/test_reset_password_email"
        browser_name = self.driver.capabilities['browserName']
        # Precondición: Correo como primer registro en bandeja y cambiar valores de las variables email,
        # password y similary
        driver.get('https://mail.google.com/mail/u/0/#inbox')

        sleep(8)
        driver.find_element_by_css_selector('#identifierId').send_keys(email)
        driver.find_element_by_css_selector('#identifierNext > content').click()
        sleep(5)
        driver.find_element_by_css_selector('#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input')\
            .send_keys(password)
        driver.find_element_by_css_selector('#passwordNext > content').click()
        sleep(5)
        driver.find_element_by_xpath('//*[@class="Cp"]/div/table/tbody/tr[1]/td[5]').click()
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
        self.assertEqual("SIGN IN", driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/div/button')
                         .text.upper(), msg=None)
        driver.find_element_by_xpath('//*[@id="id_new_password1"]').send_keys('12345678#9')
        driver.find_element_by_xpath('//*[@id="id_new_password2"]').send_keys('12345678#')
        driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/div/button').click()
        sleep(7)
        self.assertEqual("The two password fields didn't match.",
                         driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/strong').text, msg=None)
        screenshot(self, path)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="id_new_password1"]').send_keys('123456789')
        driver.find_element_by_xpath('//*[@id="id_new_password2"]').send_keys('123456789')
        driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/div/button').click()
        sleep(3)
        self.assertEqual("This password is too common.",
                         driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/strong').text, msg=None)
        self.assertEqual("This password is entirely numeric.",
                         driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/strong').text, msg=None)
        screenshot(self, path)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="id_new_password1"]').send_keys(similary)
        driver.find_element_by_xpath('//*[@id="id_new_password2"]').send_keys(similary)
        driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/div/button').click()
        sleep(5)
        self.assertEqual("The password is too similar to the email.",
                         driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/strong').text, msg=None)
        screenshot(self, path)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="id_new_password1"]').send_keys('1234567')
        driver.find_element_by_xpath('//*[@id="id_new_password2"]').send_keys('1234567')
        driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/div/button').click()
        sleep(5)
        self.assertEqual("This password is too short. It must contain at least 8 characters.",
                         driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/strong').text, msg=None)
        self.assertEqual("This password is too common.",
                         driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/strong').text, msg=None)
        self.assertEqual("This password is entirely numeric.",
                         driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[3]/strong').text, msg=None)
        screenshot(self, path)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="id_new_password1"]').send_keys('12345678#9')
        driver.find_element_by_xpath('//*[@id="id_new_password2"]').send_keys('12345678#9')
        driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/div/button').click()
        sleep(3)
        self.assertEqual("We are", driver.find_element_by_xpath('//*[@id="we"]')
                         .text, msg=None)
        self.assertEqual("Cerebro Smart Media", driver.find_element_by_xpath('//*[@id="content"]/h2')
                         .text, msg=None)
        self.assertEqual("Please login to your account", driver.find_element_by_xpath('//*[@id="subtitle"]')
                         .text, msg=None)
        self.assertEqual("SIGN IN", driver.find_element_by_xpath('//*[@id="formLogin"]/button')
                         .text.upper(), msg=None)
        screenshot(self, path)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="id_username"]').send_keys(email)
        driver.find_element_by_xpath('//*[@id="id_password"]').send_keys('12345678#9')
        driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()
        sleep(3)
        self.assertIn("http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/", driver.current_url,
                      msg=None)
        logout(self)
        driver.switch_to.window(driver.window_handles[0])
        sleep(5)
        driver.find_element_by_xpath('//table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/'
                                     'div[2]/div[3]/div[3]/div/div[2]/div[2]/a/h2').click()
        sleep(5)
        if browser_name == "chrome" or browser_name == "MicrosoftEdge":
            driver.switch_to.window(driver.window_handles[2])
        else:
                if browser_name == "firefox":
                    driver.switch_to.window(driver.window_handles[1])
        sleep(5)
        self.assertEqual("We are", driver.find_element_by_xpath('//*[@id="we"]').get_attribute("innerHTML"), msg=None)
        self.assertEqual("Cerebro Smart Media", driver.find_element_by_xpath('//*[@id="content"]/h2')
                         .text, msg=None)
        self.assertEqual("Set new password", driver.find_element_by_xpath('//*[@id="subtitle"]')
                         .text, msg=None)
        self.assertEqual("The reset password link is no longer valid",
                         driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/form/fieldset/div/div/strong')
                         .text, msg=None)
        self.assertEqual("GO BACK", driver.find_element_by_xpath('//*[@id="content"]/form/fieldset/div/a')
                         .text.upper(), msg=None)
        screenshot(self, path)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()