import unittest
from util.functions import ModelConfig, screenshot, sleep, db_functions

users = [
    {"email": "arcapruebas@gmail.com", "password": "1a23456789", "name": "Test Reset"}
]


class ResetPasswordSuccess(unittest.TestCase):

    def setUp(self):
        code = """ 
info = {0}
cur.execute("DELETE FROM users WHERE email = '%s'" % info[0]['email'])
cur.execute("DELETE FROM admin_historicaluser WHERE email = '%s'" % info[0]['email'])
sql = 'INSERT INTO users (name, password, status, email, created_at, updated_at, is_active, is_client)' \
      ' VALUES (%s, %s, %s, %s, current_timestamp, current_timestamp, %s, %s) returning email'
val = (info[0]['name'], info[0]['password'], '1', info[0]['email'], 'true', 'false')
cur.execute(sql, val)
""".format(users)
        db_functions(code)
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()

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
        driver.find_element_by_xpath('//*[@id="id_email"]').send_keys(users[0]['email'])
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
