import datetime
import json
import unittest
import time


from util.functions import *
from util.dataCampaign import *
from util.functions import login

from util.config import ModelConfig
from util.functions import screenshot, logout

campaign='''
    [{"name" : "RogelioElim","budget":"2.00", "url":"https://www.google.com","objetive":"2","industry":"Automotriz","category":"llantas","camcode":"ENSCH-75"},
    {"name" : "Rogelio 2","budget":"4.0","url":"https://www.facebook.com/a","objetive":"4.0"}]'''


class AddClient(unittest.TestCase):
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


    def testAddClient(self):
        driver = self.driver
        #login
        login(self)
        time.sleep(2)
        #Click en clientes
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[6]/a[1]/i').click()
        time.sleep(1)
        #Click en view
        driver.find_element_by_xpath('//*[@id="client-camp-header"]/div/button').click()
        time.sleep(1)
        #llenado de Form
        #name
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').send_keys("dsasd")
        time.sleep(2)
        #Seleccionar Select contenedor ACTIVE
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[2]').click()
        time.sleep(2)
        #Seleccionar Active
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[2]/select/option[1]').click()
        time.sleep(2)
        #Seleccionar Select contenedor INDUSTRIA
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[3]').click()
        time.sleep(2)
        #Seleccionar AUTOMOTRIZ
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[3]/select/option[6]').click()
        time.sleep(2)
        #Seleccionar Select contenedor CATEGORY
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[4]').click()
        time.sleep(2)
        #Seleccionar CELULARES
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[4]/select/option[6]').click()
        #BUGET
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').send_keys(2)
        #URL
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').send_keys("https://www.g.com")
        #OBJETIVE
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').send_keys(100)
        #enter
        driver.find_element_by_xpath("//div[10]/div[1]/div[1]/div[3]/button[1]").click()
        mi_ruta="clients/campaigns/testCampaign/screenshot/"
        screenshot(self,mi_ruta)
        logout(self)



    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()