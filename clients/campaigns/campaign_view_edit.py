import json
import os
import unittest
from time import sleep

from util.config import ModelConfig
from util.functions import login, db_functions, screenshot, logout, delete_file

client = "arcapruebas2@gmail.com"
campaign = '''
    [{"name" : "RogelioElim", "budget":"2.00", "url":"https://www.google.com", "objetive":"2", "industry":"Automotriz",
      "category":"llantas", "camcode":"ENSCH-75"},
    {"name" : "Rogelio 2", "budget":"4.0", "url":"https://www.facebook.com/a", "objetive":"4.0"}]'''
file_path = ((os.getenv('USERPROFILE') or os.getenv('HOME'))+"\Downloads\config_ga_cerebrosm.pdf").replace("\\", "\\\\")


class EditCampaign(unittest.TestCase):

    def setUp(self):
        global campaign
        delete_file(file_path)
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()
        info = json.loads(campaign)
        code = """
info = {0}
client = "{1}"
cur.execute("SELECT id FROM clients WHERE email = '%s'" % client)
id_client = cur.fetchone()[0]
cur.execute("DELETE FROM campaigns WHERE name = '%s' AND budget = %s AND objetive = %s"
            % (info[1]['name'], info[1]['budget'], info[1]['objetive']))
sql = 'INSERT INTO campaigns (url, cam_code, name, budget, objetive, industry, category, created_at, updated_at,' \
      'redirect_url, script_snippet, status,dbm_client_secret, dbm_client_id, client_id) ' \
      'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
val = (info[0]['url'], info[0]['camcode'], info[0]['name'], info[0]['budget'], info[0]['objetive'], info[0]['industry'],
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
        driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr[1]/td[8]/a[1]/i').click()
        #view edit
        driver.find_element_by_xpath('//*[@id="green-edit"]').click()
        sleep(1)
        # name
        driver.find_element_by_css_selector("#mod-camp-name").clear()
        driver.find_element_by_css_selector("#mod-camp-name").send_keys((info[1]["name"]))
        # budget
        driver.find_element_by_css_selector("#mod-camp-budget").clear()
        driver.find_element_by_css_selector("#mod-camp-budget").send_keys((info[1]["budget"]))
        #  url
        driver.find_element_by_css_selector("#mod-camp-url").clear()
        driver.find_element_by_css_selector("#mod-camp-url").send_keys((info[1]["url"]))
        # Objetive
        driver.find_element_by_css_selector("#mod-camp-objetive").clear()
        driver.find_element_by_css_selector("#mod-camp-objetive").send_keys((info[1]["objetive"]))
        driver.find_element_by_xpath('//*[@id="form-edit-campaign"]/div[9]/div/p/a').click()
        # Save
        driver.find_element_by_xpath("//*[@id='modal-edit-campaign']/div/div/div[3]/button").click()
        path = "clients/campaigns/screenshot/view_edit"
        screenshot(self, path)
        sleep(2)
        # asserts
        self.assertEqual(info[1]['name'], driver.find_element_by_xpath('//tr[1]/td[3]').text, msg=None)
        self.assertEqual(float(info[1]['budget']), float(driver.find_element_by_xpath('//tr[1]/td[5]').text),
                         msg=None)
        self.assertEqual(float(info[1]['objetive']), float(driver.find_element_by_xpath('//tr[1]/td[6]').text),
                         msg=None)
        sleep(2)
        self.assertTrue(os.path.exists(file_path), msg=None)


    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
