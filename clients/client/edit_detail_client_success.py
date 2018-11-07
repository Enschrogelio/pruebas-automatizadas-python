import unittest
import json
from util.functions import *
from util.config import modelConfig
from selenium.webdriver.support.ui import Select

clients = '''
        [{ "email" : "HUASTECAS@gmail.com","name" : "MOISES JOSUE ALCANTARA CABADILLA","password" : "ALCANTARA", "cpm" : "1",
        "budget" : "15000.90", "company" : "AUTOTRANSPORTES RAPIDOS DOS HUASTECAS S A DE C V", "rfc" : "ASS001002KX0",
        "address" : "2 DE ABRIL NUM 1022 ORIENTE COL INDEPENDENCIA MONTERREY N L",
        "phone" : "3125256987"
        },
        { "email" : "ECOLOGICOS@gmail.com","name" : "PEDRO ALBERTO ARAMBURA CONTRERAS" ,"password" : "ARAMBURA", "cpm" : "18",
        "budget" : "10000.52", "company" : "ASESORIA Y SERVICIOS ECOLOGICOS INTEGRALES S.A.", "rfc" : "ASE0009266M0",
        "address" : "BRONCE #9326 CD INDUSTRIAL MITRAS GARCIA N.L. C.P. 66000",
        "phone" : "3128256987"
        }]'''

class EditDetailClient(unittest.TestCase):

    def setUp(self):
        self.driver = modelConfig.driverWeb
        #Preaparación de ambiente
        info = json.loads(clients)
        code = """
info = {0}
cur.execute("DELETE FROM clients WHERE rfc = '%s'" % info[1]['rfc'])
sql = 'INSERT INTO clients (person_contact, cpm, budget, status, email, "createdAt", updated_at, password, company_name, rfc, phone, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)'
val = (info[0]['name'], info[0]['cpm'], info[0]['budget'], 1, info[0]['email'], strftime("%Y/%m/%d"), strftime("%Y/%m/%d"), info[0]['password'], info[0]['company'], info[0]['rfc'], info[0]['phone'],info[0]['address'])
cur.execute(sql, val)
""".format(info)
        db_functions(code)

    def test_edit_detail_client_success(self):
        browserName = self.driver.capabilities['browserName']
        #print(browserName)
        mi_ruta = "clients/client/screenshot/test_edit_detail_client_success"
        info = json.loads(clients)

        #login
        login(self)
        sleep(3)
        driver = self.driver
        self.assertIn(modelConfig.baseUrl+"/admin/clients/", driver.current_url, msg=None)
        sleep(3)
        driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
        driver.find_element_by_id('search').send_keys(info[0]['rfc'])
        sleep(3)
        self.assertEqual(info[0]['email'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[1]')
                         .text, msg=None)
        self.assertEqual(info[0]['name'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[2]')
                         .text, msg=None)
        self.assertEqual(info[0]['rfc'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[3]')
                         .text, msg=None)
        self.assertEqual(info[0]['cpm'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[4]')
                         .text, msg=None)
        screenshot(self, mi_ruta)
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr/td[6]/a[1]').click()
        self.assertIn(modelConfig.baseUrl+"/admin/client/detail", driver.current_url, msg=None)
        self.assertEqual(info[0]['company'], driver.find_element_by_xpath('//*[@id="client-info-header"]/h2')
                         .text, msg=None)
        self.assertEqual("Clients /", driver.find_element_by_xpath('//*[@id="client-info-header"]/a[1]')
                         .text, msg=None)
        self.assertEqual(info[0]['company'], driver.find_element_by_xpath('//*[@id="client-info-header"]/a[2]')
                         .text, msg=None)
        self.assertEqual("Email", driver.find_element_by_xpath('//*[@id="client-info"]/div/div[1]/label')
                         .text, msg=None)
        self.assertEqual(info[0]['email'], driver.find_element_by_xpath('//*[@id="client-info"]/div/div[1]/p')
                         .text, msg=None)
        self.assertEqual("Password", driver.find_element_by_xpath('//*[@id="client-info"]/div/div[2]/label')
                         .text, msg=None)
        self.assertEqual("**************", driver.find_element_by_xpath('//*[@id="client-info"]/div/div[2]/p')
                         .text, msg=None)
        self.assertEqual("Company", driver.find_element_by_xpath('//*[@id="client-info"]/div/div[3]/label')
                         .text, msg=None)
        self.assertEqual(info[0]['company'], driver.find_element_by_xpath('//*[@id="client-info"]/div/div[3]/p')
                         .text, msg=None)
        self.assertEqual("RFC", driver.find_element_by_xpath('//*[@id="client-info"]/div/div[4]/label')
                         .text, msg=None)
        self.assertEqual(info[0]['rfc'], driver.find_element_by_xpath('//*[@id="client-info"]/div/div[4]/p')
                         .text, msg=None)
        self.assertEqual("Address", driver.find_element_by_xpath('//*[@id="client-info"]/div/div[5]/label')
                         .text, msg=None)
        self.assertEqual(info[0]['address'], driver.find_element_by_xpath('//*[@id="client-info"]/div/div[5]/p')
                         .text, msg=None)
        self.assertEqual("Contact", driver.find_element_by_xpath('//*[@id="client-info"]/div/div[6]/label')
                         .text, msg=None)
        self.assertEqual(info[0]['name'], driver.find_element_by_xpath('//*[@id="client-info"]/div/div[6]/p')
                         .text, msg=None)
        self.assertEqual("Phone", driver.find_element_by_xpath('//*[@id="client-info"]/div/div[7]/label')
                         .text, msg=None)
        self.assertEqual(info[0]['phone'], driver.find_element_by_xpath('//*[@id="client-info"]/div/div[7]/p')
                         .text, msg=None)
        self.assertEqual("Budget", driver.find_element_by_xpath('//*[@id="client-info"]/div/div[8]/label')
                         .text, msg=None)
        self.assertEqual(info[0]['budget'], driver.find_element_by_xpath('//*[@id="client-info"]/div/div[8]/p')
                         .text, msg=None)
        self.assertEqual("Cpm", driver.find_element_by_xpath('//*[@id="client-info"]/div/div[9]/label')
                         .text, msg=None)
        self.assertEqual(info[0]['cpm'], driver.find_element_by_xpath('//*[@id="client-info"]/div/div[9]/p')
                         .text, msg=None)
        screenshot(self, mi_ruta)
        driver.find_element_by_xpath('//*[@id="btn-edit"]').click()
        screenshot(self, mi_ruta)
        sleep(5)
        driver.find_element_by_css_selector('#form-edit #id_email').clear()
        driver.find_element_by_css_selector('#form-edit #id_email').send_keys(info[1]['email'])
        driver.find_element_by_css_selector('#form-edit #id_person_contact').clear()
        driver.find_element_by_css_selector('#form-edit #id_person_contact').send_keys(info[1]['name'])
        select = Select(driver.find_element_by_css_selector("#form-edit #id_status"))
        select.select_by_index(1)
        driver.find_element_by_css_selector('#form-edit #id_password').clear()
        driver.find_element_by_css_selector('#form-edit #id_password').send_keys(info[1]['password'])
        driver.find_element_by_css_selector('#form-edit #id_cpm').clear()
        driver.find_element_by_css_selector('#form-edit #id_cpm').send_keys(info[1]['cpm'])
        driver.find_element_by_css_selector('#form-edit #id_budget').clear()
        driver.find_element_by_css_selector('#form-edit #id_budget').send_keys(info[1]['budget'])
        driver.find_element_by_css_selector('#form-edit #id_company_name').clear()
        driver.find_element_by_css_selector('#form-edit #id_company_name').send_keys(info[1]['company'])
        driver.find_element_by_css_selector('#form-edit #id_rfc').clear()
        driver.find_element_by_css_selector('#form-edit #id_rfc').send_keys(info[1]['rfc'])
        driver.find_element_by_css_selector('#form-edit #id_address').clear()
        driver.find_element_by_css_selector('#form-edit #id_address').send_keys(info[1]['address'])
        driver.find_element_by_css_selector('#form-edit #id_phone').clear()
        driver.find_element_by_css_selector('#form-edit #id_phone').send_keys(info[1]['phone'])
        screenshot(self, mi_ruta)
        driver.find_element_by_css_selector("#modal-edit > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > button:nth-child(1)").click()
        sleep(5)
        driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
        driver.find_element_by_id('search').send_keys(info[1]['rfc'])
        sleep(5)
        self.assertEqual(info[1]['email'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[1]')
                         .text, msg=None)
        self.assertEqual(info[1]['name'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[2]')
                         .text, msg=None)
        self.assertEqual(info[1]['rfc'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[3]')
                         .text, msg=None)
        self.assertEqual(info[1]['cpm'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[4]')
                         .text, msg=None)
        self.assertEqual('inactive', driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[5]')
                         .text, msg=None)
        screenshot(self, mi_ruta)
        sleep(5)

    def tearDown(self):
        logout(self)
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
