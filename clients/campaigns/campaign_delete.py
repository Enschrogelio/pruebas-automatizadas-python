import json
from time import sleep
import unittest
from util.functions import login, db_functions
from util.config import ModelConfig
from util.functions import screenshot, logout

campaign = '''
    [
        {"name" : "Rogelio 2", "budget":"4.00", "url":"https://www.google.com", "objetive":"4", "industry":"Automotriz",
         "category":"llantas", "camcode":"ENSCH-75"}
    ]
'''
value = ""
client = "arcapruebas2@gmail.com"
info = json.loads(campaign)


class DeleteCampaign(unittest.TestCase):

    def setUp(self):
        global campaign, value
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()
        code = """
info = {0}
client = "{1}"
cur.execute("SELECT id FROM clients WHERE email = '%s'" % client)
id_client = cur.fetchone()[0]
cur.execute("DELETE FROM campaigns WHERE name = '%s' AND budget = %s AND objetive = %s"
            % (info[0]['name'], info[0]['budget'], info[0]['objetive']))
sql = "INSERT INTO campaigns (cam_code, name, industry, category, budget, url, redirect_url, script_snippet, " \
      "objetive, status, dbm_client_secret, dbm_client_id, created_at, updated_at, client_id, utm_campaign, " \
      "utm_source, ga_id, token_access_google_dbm) VALUES (%s, %s, %s, %s, %s, %s, '', '', %s, 1, '', '', %s, %s, " \
      "%s, '', '', '', '') RETURNING name, industry, objetive"
val = (info[0]['camcode'], info[0]['name'], info[0]['industry'], info[0]['category'], info[0]['budget'], info[0]['url'],
       info[0]['objetive'], strftime("%Y/%m/%d"), strftime("%Y/%m/%d"), id_client)
cur.execute(sql, val)
""".format(info, client)
        value = db_functions(code)[0]

    def test_add_client(self):
        global campaign, value
        driver = self.driver
        # login
        login(self)
        sleep(2)
        # Click en clientes
        driver.find_element_by_xpath('//*[@id="inputSrc"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(client)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[5]/a[1]').click()
        sleep(2)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr/td[@title="%s"]' % value[0])
                         .get_attribute("innerText").replace("\t", ""), info[0]['name'], msg=None)
        self.assertEqual("%s" % value[1], driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr[1]/td[4]')
                         .get_attribute("innerText").replace("\t", ""), msg=None)
        self.assertEqual("%s" % value[2], driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr[1]/td[6]')
                         .get_attribute("innerText").replace("\t", ""), msg=None)
        sleep(3)
        driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr[1]/td[8]/a[3]').click()
        path = "clients/campaigns/screenshot/"
        sleep(2)
        # message "Deleting record"
        driver.find_element_by_xpath("//button[@class='btn-green text-uppercase col-sm-12']").click()
        # message confirmation
        sleep(2)
        driver.find_element_by_xpath('//*[@id="input-confirmation"]').send_keys((info[0]['name']))
        sleep(2)
        driver.find_element_by_xpath("//button[@id='btn-submit']").click()
        screenshot(self, path)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
