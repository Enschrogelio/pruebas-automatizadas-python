import json
import unittest
from time import sleep
from util.config import ModelConfig
from util.functions import login, db_functions, screenshot, logout

client = "arcapruebas2@gmail.com"
campaign = '''
    [
        {"name" : "RogelioView", "budget":"2.00", "url":"https://www.google.com", "objetive":"2", 
         "industry":"Automotriz", "category":"llantas", "camcode":"ENSCH-75"},
        {"name" : "Rogelio 2", "budget":"4.0", "url":"https://www.facebook.com/a", "objetive":"4.0"}
    ]
'''
info = json.loads(campaign)


class EditCampaign(unittest.TestCase):

    def setUp(self):
        global campaign
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()
        code = """
info = {0}
cur.execute("DELETE FROM campaigns WHERE name = '%s' AND budget = %s AND objetive = %s"
            % (info[1]['name'], info[1]['budget'], info[1]['objetive']))
sql = 'INSERT INTO campaigns (url, cam_code, name, budget, objetive, industry, category, created_at, updated_at,' \
      'redirect_url, script_snippet, status, dbm_client_secret, dbm_client_id, client_id) ' \
      'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
val = (info[0]['url'], info[0]['camcode'], info[0]['name'], info[0]['budget'], info[0]['objetive'], info[0]['industry'],
       info[0]['category'], strftime("%Y/%m/%d"), strftime("%Y/%m/%d"), '', '', 1, '', '', 2)
cur.execute(sql, val)

""".format(info)
        db_functions(code)

    def test_campaign(self):
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
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[6]/a[1]/i').click()
        sleep(1)
        # Click en view
        driver.find_element_by_xpath("//tr[1]/td[10]/a[2]/i[1]").click()
        sleep(1)
        path = "clients/campaigns/screenshot/"
        screenshot(self, path)
        # name
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[1]/input").clear()
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[1]/input").send_keys((info[1]["name"]))
        # budget
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[5]/input").clear()
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[5]/input").send_keys((info[1]["budget"]))
        #  url
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[6]/input").clear()
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[6]/input").send_keys((info[1]["url"]))
        # Objetive
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[7]/input").clear()
        driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[7]/input")\
            .send_keys((info[1]["objetive"]))
        # Save
        driver.find_element_by_xpath("//div[@id='modal-edit-campaign']/div[1]/div[3]/button[1]").click()
        sleep(2)
        # asserts
        self.assertEqual(info[1]['name'], driver.find_element_by_xpath('//tr[1]/td[3]').text, msg=None)
        self.assertEqual(float(info[1]['budget']), float(driver.find_element_by_xpath('//tr[1]/td[6]').text),
                         msg=None)
        self.assertEqual(float(info[1]['objetive']), float(driver.find_element_by_xpath('//tr[1]/td[7]').text),
                         msg=None)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
