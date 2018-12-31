import json
import unittest
from time import sleep
from util.config import ModelConfig
from util.functions import login, db_functions, screenshot, logout

client = "arcapruebas2@gmail.com"
campaign = '''
    [
        {"name" : "RogelioElim", "budget":"2.00", "url":"https://www.google.com", "objective":"2", "industry":"Automotriz",
         "category":"llantas", "camcode":"ENSCH-75"}
    ]'''


class EditCampaign(unittest.TestCase):

    def setUp(self):
        global campaign
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()
        info = json.loads(campaign)
        code = """
info = {0}
client = "{1}"
cur.execute("SELECT id FROM clients WHERE email = '%s'" % client)
id_client = cur.fetchone()[0]
cur.execute("DELETE FROM campaigns WHERE name = '%s' AND budget = %s AND objetive = %s"
            % (info[0]['name'], info[0]['budget'], info[0]['objective']))
sql = 'INSERT INTO campaigns (url, cam_code, name, budget, objetive, industry, category, created_at, updated_at,' \
      'redirect_url, script_snippet, status, dbm_client_secret, dbm_client_id, client_id) ' \
      'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
val = (info[0]['url'], info[0]['camcode'], info[0]['name'], info[0]['budget'], info[0]['objective'], info[0]['industry'],
       info[0]['category'], strftime("%Y/%m/%d"), strftime("%Y/%m/%d"), '', '', 1, '', '', id_client)
cur.execute(sql, val)
""".format(info, client)
        db_functions(code)

    def test_campaign(self):
        global campaign
        driver = self.driver
        info = json.loads(campaign)
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
        driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr[1]/td[8]/a[1]').click()
        # asserts
        self.assertEqual(info[0]['name'], 
                         driver.find_element_by_xpath('//*[@id="client-info"]/div/div[3]/p').text, msg=None)
        self.assertEqual(info[0]['industry'],
                         driver.find_element_by_xpath('//*[@id="client-info"]/div/div[4]/p').text, msg=None)
        self.assertEqual(info[0]['category'],
                         driver.find_element_by_xpath('//*[@id="client-info"]/div/div[5]/p').text, msg=None)
        self.assertEqual(float(info[0]['budget']), 
                         float(driver.find_element_by_xpath('//*[@id="client-info"]/div/div[6]/p').text), msg=None)
        self.assertEqual(float(info[0]['objective']), 
                         float(driver.find_element_by_xpath('//*[@id="client-info"]/div/div[7]/p').text), msg=None)
        path = "clients/campaigns/screenshot/"
        screenshot(self, path)
        sleep(2)
        # asserts

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
