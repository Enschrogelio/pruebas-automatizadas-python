import json
import unittest
from time import sleep
from util.config import ModelConfig
from util.functions import login, db_functions, screenshot, randoms, logout

client = "arcapruebas2@gmail.com"
campaign = '''
    [{"name" : "RogelioElim", "budget":"2.00", "url":"https://www.google.com", "objetive":"2", "industry":"Automotriz",
      "category":"llantas", "camcode":"ENSCH-75"},
    {"name" : "Rogelio 2", "budget":"4.0", "url":"https://www.facebook.com/a", "objetive":"4.0"}]'''
info = json.loads(campaign)


class EditCampaign(unittest.TestCase):
    def campaign_main(self):
        global campaign
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
        sleep(2)
        # view campaign
        driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr[1]/td[10]/a[1]/i').click()
        # view edit
        driver.find_element_by_xpath('//*[@id="green-edit"]').click()

    # noinspection PyCallByClass,PyTypeChecker
    @classmethod
    def setUpClass(cls):
        cls.driver = ModelConfig.driver_web
        cls.driver.maximize_window()
        code = """
info = {0}
cur.execute("DELETE FROM campaigns WHERE name = '%s' AND budget = %s AND objetive = %s"
            % (info[1]['name'], info[1]['budget'], info[1]['objetive']))
sql = 'INSERT INTO campaigns (url, cam_code, name, budget, objetive, industry, category, created_at, updated_at,' \
      'redirect_url, script_snippet, status, ga_api_key, ga_api_secret, dbm_client_secret, dbm_client_id, client_id) ' \
      'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
val = (info[0]['url'], info[0]['camcode'], info[0]['name'], info[0]['budget'], info[0]['objetive'], info[0]['industry'],
       info[0]['category'], strftime("%Y/%m/%d"), strftime("%Y/%m/%d"), '', '', 1, '', '', '', '', 2)
""".format(info)
        db_functions(code)
        cls.campaign_main(cls)

    def test_campaign_empty(self):
        driver = self.driver
        sleep(2)
        # name
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[1]/input").clear()
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[1]/input").clear()
        # budget
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[5]/input").clear()
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[5]/input").clear()
        # url
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[6]/input").clear()
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[6]/input").clear()
        # Objetive
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[7]/input").clear()
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[7]/input").clear()
        # Save
        driver.find_element_by_xpath("//div[@id='modal-edit-campaign']/div[1]/div[1]/div[3]/button[1]").click()
        # asserts name
        self.assertEqual("This field is empty",
                         driver.find_element_by_xpath('//*[@id="form-edit-campaign"]/div[1]/span').text, msg=None)
        # asserts Budget
        self.assertEqual("This field is empty.",
                         driver.find_element_by_xpath('//*[@id="form-edit-campaign"]/div[5]/span').text, msg=None)
        # asserts url
        self.assertEqual("This field is empty",
                         driver.find_element_by_xpath('//*[@id="form-edit-campaign"]/div[6]/span').text, msg=None)
        # asserts objetive
        self.assertEqual("This field is empty",
                         driver.find_element_by_xpath('//*[@id="form-edit-campaign"]/div[7]/span').text, msg=None)
        path = "clients/campaigns/screenshot/"
        screenshot(self, path)

    def test_min(self):
        driver = self.driver
        sleep(2)
        # name
        driver.find_element_by_css_selector('#form-edit-campaign #id_name').clear()
        driver.find_element_by_css_selector('#form-edit-campaign #id_name').send_keys(randoms(1, "letter"))
        # budget
        driver.find_element_by_css_selector('#form-edit-campaign #id_budget').clear()
        driver.find_element_by_css_selector('#form-edit-campaign #id_budget').send_keys(randoms(1, "number"))
        # url
        driver.find_element_by_css_selector('#form-edit-campaign #id_url').clear()
        driver.find_element_by_css_selector('#form-edit-campaign #id_url')\
            .send_keys("https://%s" % randoms(1, "letter")+".com")
        # objeive
        driver.find_element_by_css_selector('#form-edit-campaign #id_objetive').clear()
        driver.find_element_by_css_selector('#form-edit-campaign #id_objetive').send_keys(randoms(1, "number"))

    def test_max(self):
        driver = self.driver
        sleep(2)
        # name
        driver.find_element_by_css_selector('#form-edit-campaign #id_name').clear()
        driver.find_element_by_css_selector('#form-edit-campaign #id_name').send_keys(randoms(256, "letter"))
        # budget
        driver.find_element_by_css_selector('#form-edit-campaign #id_budget').clear()
        driver.find_element_by_css_selector('#form-edit-campaign #id_budget').send_keys(randoms(256, "number"))
        # url
        driver.find_element_by_css_selector('#form-edit-campaign #id_url').clear()
        driver.find_element_by_css_selector('#form-edit-campaign #id_url')\
            .send_keys("https://%s.com" % randoms(256, "letter"))
        # objeive
        driver.find_element_by_css_selector('#form-edit-campaign #id_objetive').clear()
        driver.find_element_by_css_selector('#form-edit-campaign #id_objetive').send_keys(randoms(256, "number"))
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
        driver.find_element_by_css_selector('#form-edit-campaign #id_name').clear()
        driver.find_element_by_css_selector('#form-edit-campaign #id_name').send_keys(randoms(100, "special"))
        # budget
        driver.find_element_by_css_selector('#form-edit-campaign #id_budget').clear()
        driver.find_element_by_css_selector('#form-edit-campaign #id_budget').send_keys(randoms(100, "special"))
        # url
        driver.find_element_by_css_selector('#form-edit-campaign #id_url').clear()
        driver.find_element_by_css_selector('#form-edit-campaign #id_url')\
            .send_keys("https://%s" % randoms(10, "special")+".com")
        # objeive
        driver.find_element_by_css_selector('#form-edit-campaign #id_objetive').clear()
        driver.find_element_by_css_selector('#form-edit-campaign #id_objetive').send_keys(randoms(100, "special"))
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
