import json
import unittest
from util.functions import *
from util.config import *
from util.functions import login

campaign = '''
    [{"name" : "RogelioElim", "budget":"2.00", "url":"https://www.google.com", "objetive":"2", "industry":"Automotriz",
      "category":"llantas", "camcode":"ENSCH-75"},
    {"name" : "Rogelio 2", "budget":"4.0", "url":"https://www.facebook.com/a", "objetive":"4.0"}]'''


class EditCampaign(unittest.TestCase):

    def setUp(self):
        global campaign
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()
        info = json.loads(campaign)
        code = """
info = {0}
cur.execute("DELETE FROM campaigns WHERE name = '%s' AND budget = %s AND objetive = %s"
            % (info[0]['name'], info[0]['budget'], info[0]['objetive']))
sql = 'INSERT INTO campaigns (url, cam_code, name, budget, objetive, industry, category, created_at, updated_at,' \
      'redirect_url, script_snippet, status, ga_api_key, ga_api_secret, dbm_client_secret, dbm_client_id, client_id) ' \
      'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
val = (info[0]['url'], info[0]['camcode'], info[0]['name'], info[0]['budget'], info[0]['objetive'], info[0]['industry'],
       info[0]['category'], strftime("%Y/%m/%d"), strftime("%Y/%m/%d"), '', '', 1, '', '', '', '', 2)
cur.execute(sql, val)
""".format(info)
        db_functions(code)

    def test_campaign(self):
        global campaign
        driver = self.driver
        info = json.loads(campaign)
        # login
        login(self)
        sleep(2)
        # Click en clientes
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[6]/a[1]/i').click()
        sleep(2)
        # view campaign
        driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr[1]/td[10]/a[1]/i').click()
        # asserts
        self.assertEqual(info[0]['name'], driver.find_element_by_xpath('//*[@id="client-info"]'
                                                                       '/div/div[4]/p').text, msg=None)
        self.assertEqual(float(info[0]['budget']), float(driver.find_element_by_xpath('//*[@id="client-info"]'
                                                                                      '/div/div[7]/p').text),
                         msg=None)
        self.assertEqual(float(info[0]['objetive']), float(driver.find_element_by_xpath('//*[@id="client-info"]'
                                                                                        '/div/div[8]/p').text),
                         msg=None)
        mi_ruta="clients/campaigns/screenshot/"
        screenshot(self, mi_ruta)
        sleep(2)
        # asserts

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
