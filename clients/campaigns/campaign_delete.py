import json
import unittest
from util.functions import *
from util.functions import login
from util.config import ModelConfig
from util.functions import screenshot, logout

campaign = '''
    [{"name" : "Rogelio 2","budget":"4.00", "url":"https://www.google.com","objetive":"4","industry":"Automotriz",
    "category":"llantas","camcode":"ENSCH-75"},
    {"name" : "Rogelio 2","budget":"4.0","url":"https://www.facebook.com/a","objetive":"4.0"}]'''
valor = ""


class DeleteCampaign(unittest.TestCase):

    def setUp(self):
        global campaign, valor
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()
        info = json.loads(campaign)
        code = """
info = {0}
cur.execute("DELETE FROM campaigns WHERE name = '%s' AND budget = '%s' AND objetive = '%s'" 
            % (info[0]['name'], info[0]['budget'], info[0]['objetive']))
sql = 'INSERT INTO campaigns (url, cam_code, name, budget, objetive, industry, category, created_at, updated_at,' \
      'redirect_url, script_snippet, status, ga_api_key,ga_api_secret,dbm_client_secret,dbm_client_id, client_id) ' \
      'VALUES (%s,%s, %s, %s, %s, %s, %s, %s,%s,%s, %s, %s,%s,%s,%s,%s,%s) returning name, budget, objetive'
val = (info[0]['url'], info[0]['camcode'],info[0]['name'], info[0]['budget'], info[0]['objetive'],info[0]['industry'],
       info[0]['category'], strftime("%Y/%m/%d"), strftime("%Y/%m/%d"),'','',1,'','','','',2)
cur.execute(sql, val)
""".format(info)
        valor = db_functions(code)[0]
        # print(valor)

    def test_add_client(self):
        global campaign, valor
        info = json.loads(campaign)
        driver = self.driver
        # login
        login(self)
        sleep(2)
        # Click en clientes
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[6]/a[1]/i').click()
        sleep(2)
        self.assertEqual(info[0]['name'], driver
                         .find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr/td[@title="%s"]'
                                                % valor[0]).get_attribute("innerText").replace("\t",""), msg=None)
        self.assertEqual("%s" % valor[1],
                         driver.find_element_by_xpath('//tr[1]/td[6]')
                         .get_attribute("innerText").replace("\t",""), msg=None)
        self.assertEqual("%s" % valor[2], driver.find_element_by_xpath('//tr[1]/td[7]')
                         .get_attribute("innerText").replace("\t",""), msg=None)
        sleep(3)
        driver.find_element_by_xpath("//tr[1]/td[10]/a[@class='to-delete' and 3]"
                                     "/i[@class='glyphicon glyphicon-trash' and 1]").click()
        mi_ruta = "clients/campaigns/screenshot/"
        sleep(2)
        # message "Deleting record"
        driver.find_element_by_xpath("//button[@class='btn-green text-uppercase col-sm-12']").click()
        # message confirmaion
        sleep(2)
        driver.find_element_by_xpath('//*[@id="input-email"]').send_keys((info[0]['name']))
        sleep(2)
        driver.find_element_by_xpath("//button[@id='btn-submit']").click()
        screenshot(self, mi_ruta)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()