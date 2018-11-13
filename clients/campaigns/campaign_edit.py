import datetime
import json
import unittest
import time

import xmlrunner

from util.functions import *
from util.config import *
from util.functions import login

campaign='''
    [{"name" : "RogelioElim","budget":"2.00", "url":"https://www.google.com","objetive":"2","industry":"Automotriz","category":"llantas","camcode":"ENSCH-75"},
    {"name" : "Rogelio 2","budget":"4.0","url":"https://www.facebook.com/a","objetive":"4.0"}]'''

class EditCampaign(unittest.TestCase):
    def setUp(self):
        global campaign
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()
        info = json.loads(campaign)
        code = """
info = {0}
cur.execute("DELETE FROM campaigns WHERE name = '%s' AND budget = '%s' AND objetive = '%s'" %(info[0]['name'], info[0]['budget'], info[0]['objetive']))
sql = 'INSERT INTO campaigns (url, cam_code, name, budget, objetive, industry, category, created_at, updated_at, redirect_url, script_snippet, status, ga_api_key,ga_api_secret,dbm_client_secret,dbm_client_id, client_id) VALUES (%s,%s, %s, %s, %s, %s, %s, %s,%s,%s, %s, %s,%s,%s,%s,%s,%s)'
val = (info[0]['url'], info[0]['camcode'],info[0]['name'], info[0]['budget'], info[0]['objetive'],info[0]['industry'], info[0]['category'], strftime("%Y/%m/%d"), strftime("%Y/%m/%d"),'','',1,'','','','',2)
cur.execute(sql, val)
""".format(info)
        db_functions(code)
        #print("DELETE FROM campaigns WHERE name = '%s' AND budget = '%s' AND objetive = '%s' AND url = '%s'%("+info[0]['name']+", "+info[0]['budget']+", "+info[0]['url']+", "+info[0]['objetive']+")")


    def test_campaign(self):
            global campaign
            driver = self.driver
            info = json.loads(campaign)
        #login
            login(self)
            time.sleep(2)
            #Click en clientes
            driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[6]/a[1]/i').click()
            time.sleep(1)
            #Click en view
            driver.find_element_by_xpath("//tr[1]/td[10]/a[2]/i[@class='glyphicon glyphicon-pencil' and 1]").click()
            time.sleep(1)
            mi_ruta="clients/campaigns/screenshot/"
            screenshot(self,mi_ruta)

            #name
            driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[@class='form-group' and 1]/input[@id='id_name' and @class='form-control' and 1]").clear()
            driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[@class='form-group' and 1]/input[@id='id_name' and @class='form-control' and 1]").send_keys((info[1]["name"]))
            #budget
            driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[@class='form-group' and 5]/input[@id='id_budget' and @class='form-control' and 1]").clear()
            driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[@class='form-group' and 5]/input[@id='id_budget' and @class='form-control' and 1]").send_keys((info[1]["budget"]))
            #url
            driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[@class='form-group' and 6]/input[@id='id_url' and @class='form-control' and 1]").clear()
            driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[@class='form-group' and 6]/input[@id='id_url' and @class='form-control' and 1]").send_keys((info[1]["url"]))
            #Objetive
            driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[@class='form-group' and 7]/input[@id='id_objetive' and @class='form-control' and 1]").clear()
            driver.find_element_by_xpath("//form[@id='form-edit-campaign']/div[@class='form-group' and 7]/input[@id='id_objetive' and @class='form-control' and 1]").send_keys((info[1]["objetive"]))
            #Save
            driver.find_element_by_xpath("//div[@id='modal-edit-campaign']/div[@class='modal-dialog box' and 1]/div[@class='modal-box' and 1]/div[@class='modal-footer col-md-12' and 3]/button[1]").click()
            sleep(2)
            #asserts
            self.assertEqual(info[1]['name'], driver.find_element_by_xpath('//tr[1]/td[3]').text, msg=None)
            self.assertEqual(info[1]['budget'], driver.find_element_by_xpath('//tr[1]/td[6]').text, msg=None)
            self.assertEqual(info[1]['objetive'], driver.find_element_by_xpath('//tr[1]/td[7]').text, msg=None)

    def tearDown(self):
            logout(self)
            self.driver.close()

if __name__ == "__main__":
    unittest.main()