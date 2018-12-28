import json
import unittest
from time import sleep
from util.config import ModelConfig
from util.functions import login, db_functions, screenshot, randoms, logout

client = "arcapruebas2@gmail.com"
campaign = '''
    [
        {"name": "RogelioElim", "budget": "2.00", "url": "https://www.google.com", "objetive": "2", 
         "industry": "Automotriz", "category": "llantas", "camcode": "ENSCH-75"}
    ]'''
info = json.loads(campaign)


class EditCampaign(unittest.TestCase):
    def campaign_main(self):
        driver = self.driver
        # login
        login(self)
        sleep(2)
        # Click en clientes
        driver.find_element_by_xpath('//*[@id="inputSrc"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(client)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[5]/a[1]/i').click()
        sleep(1)
        # Click en edit
        driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr[1]/td[8]/a[2]').click()
        sleep(1)
        path = "clients/campaigns/screenshot/"
        screenshot(self, path)

    # noinspection PyCallByClass,PyTypeChecker
    @classmethod
    def setUpClass(cls):
        cls.driver = ModelConfig.driver_web
        cls.driver.maximize_window()
        code = """
info = {0}
client = "{1}"
cur.execute("SELECT id FROM clients WHERE email = '%s'" % client)
id_client = cur.fetchone()[0]
cur.execute("DELETE FROM campaigns WHERE name = '%s' AND budget = %s AND objetive = %s"
            % (info[0]['name'], info[0]['budget'], info[0]['objetive']))
sql = "INSERT INTO campaigns (cam_code, name, industry, category, budget, url, redirect_url, script_snippet, objetive, " \
      "status, dbm_client_secret, dbm_client_id, created_at, updated_at, client_id, utm_campaign, utm_source, ga_id, " \
      "token_access_google_dbm) VALUES (%s, %s, %s, %s, %s, %s, '', '', %s, 1, '', '', %s, %s, %s, '', '', '', '')"
val = (info[0]['camcode'], info[0]['name'], info[0]['industry'], info[0]['category'], info[0]['budget'], info[0]['url'],
       info[0]['objetive'], strftime("%Y/%m/%d"), strftime("%Y/%m/%d"), id_client)
cur.execute(sql, val)
""".format(info, client)
        db_functions(code)
        cls.campaign_main(cls)

    def test_campaign_empty(self):
        driver = self.driver
        sleep(2)
        # clean fields
        driver.find_element_by_css_selector('#mod-camp-name').clear()
        driver.find_element_by_css_selector('#mod-camp-budget').clear()
        driver.find_element_by_css_selector('#mod-camp-url').clear()
        driver.find_element_by_css_selector('#mod-camp-objetive').clear()
        driver.find_element_by_xpath('//*[@id="modal-edit-campaign"]/div/div/div[3]/button').click()
        # asserts
        self.assertEqual("This field is empty",
                         driver.find_element_by_xpath('//*[@id="form-edit-campaign"]/div[2]/span').text, msg=None)
        self.assertEqual("This field is empty.",
                         driver.find_element_by_xpath('//*[@id="form-edit-campaign"]/div[6]/span').text, msg=None)
        self.assertEqual("This field is empty",
                         driver.find_element_by_xpath('//*[@id="form-edit-campaign"]/div[7]/span').text, msg=None)
        self.assertEqual("This field is empty",
                         driver.find_element_by_xpath('//*[@id="form-edit-campaign"]/div[8]/span').text, msg=None)

    def test_min(self):
        driver = self.driver
        sleep(2)
        # name
        driver.find_element_by_css_selector('#mod-camp-name').clear()
        driver.find_element_by_css_selector('#mod-camp-name').send_keys(randoms(1, "letter"))
        # budget
        driver.find_element_by_css_selector('#mod-camp-budget').clear()
        driver.find_element_by_css_selector('#mod-camp-budget').send_keys(randoms(1, "number"))
        # url
        driver.find_element_by_css_selector('#mod-camp-url').clear()
        driver.find_element_by_css_selector('#mod-camp-url')\
            .send_keys("https://%s" % randoms(1, "letter")+".com")
        # objeive
        driver.find_element_by_css_selector('#mod-camp-objetive').clear()
        driver.find_element_by_css_selector('#mod-camp-objetive').send_keys(randoms(1, "number"))
        # click Save
        # driver.find_element_by_xpath('//*[@id="modal-edit-campaign"]/div/div/div[3]/button').click()

    def test_max(self):
        driver = self.driver
        sleep(2)
        # name
        driver.find_element_by_css_selector('#mod-camp-name').clear()
        driver.find_element_by_css_selector('#mod-camp-name').send_keys(randoms(250, "letter"))
        # budget
        driver.find_element_by_css_selector('#mod-camp-budget').clear()
        driver.find_element_by_css_selector('#mod-camp-budget').send_keys(randoms(250, "number"))
        # url
        driver.find_element_by_css_selector('#mod-camp-url').clear()
        driver.find_element_by_css_selector('#mod-camp-url')\
            .send_keys("https://%s" % randoms(250, "letter")+".com")
        # objeive
        driver.find_element_by_css_selector('#mod-camp-objetive').clear()
        driver.find_element_by_css_selector('#mod-camp-objetive').send_keys(randoms(250, "number"))
        # click Save
        driver.find_element_by_xpath('//*[@id="modal-edit-campaign"]/div/div/div[3]/button').click()
        sleep(2)
        # asserts Budget
        self.assertEqual("Enter a valid budget. Maximum allowed decimals: 2",
                         driver.find_element_by_xpath('//*[@id="form-edit-campaign"]/div[5]/span').text, msg=None)
        # asserts objetive
        self.assertEqual("Please input a value between 0-2147483647.",
                         driver.find_element_by_xpath('//*[@id="form-edit-campaign"]/div[7]/span').text, msg=None)

    def test_special(self):
        driver = self.driver
        sleep(4)
        # name
        driver.find_element_by_css_selector('#mod-camp-name').clear()
        driver.find_element_by_css_selector('#mod-camp-name').send_keys(randoms(100, "special"))
        # budget
        driver.find_element_by_css_selector('#mod-camp-budget').clear()
        driver.find_element_by_css_selector('#mod-camp-budget').send_keys(randoms(100, "special"))
        # url
        driver.find_element_by_css_selector('#mod-camp-url').clear()
        driver.find_element_by_css_selector('#mod-camp-url').send_keys("https://%s" %
                                                                                     randoms(10, "special")+".com")
        # objetive
        driver.find_element_by_css_selector('#mod-camp-objetive').clear()
        driver.find_element_by_css_selector('#mod-camp-objetive').send_keys(randoms(100, "special"))
        # click Save
        driver.find_element_by_xpath('//*[@id="modal-edit-campaign"]/div/div/div[3]/button').click()
        sleep(2)
        # asserts Budget
        self.assertEqual("Enter a valid budget. "
                         "Maximum allowed decimals: 2",
                         driver.find_element_by_xpath('//*[@id="form-edit-campaign"]/div[5]/span').text, msg=None)
        # asserts objetive
        self.assertEqual("This field is empty",
                         driver.find_element_by_xpath('//*[@id="form-edit-campaign"]/div[7]/span').text, msg=None)

    # noinspection PyUnresolvedReferences
    @classmethod
    def tearDownClass(cls):
        logout(cls)
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
