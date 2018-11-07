import unittest
import json
from util.functions import *
from util.config import modelConfig

clients = '''
        [{ "email" : "RUIZ@gmail.com","name" : "OSCAR IGNACIO ALVAREZ CHAGOYA","password" : "ALVAREZ", "cpm" : "99",
        "budget" : "0.08", "company" : "AUTO TRANSPORTES DE CARGA RUIZ HERMANOS SA DE CV", "rfc" : "ATC900103NR1",
         "address" : "CARRET. PESQUERIA KM .600 LADRILLERA, PESQUERIA N.L CP 66650",
        "phone" : "3121256985"
        }]'''

class DeatailClient(unittest.TestCase):

    def setUp(self):
        self.driver = modelConfig.driverWeb
        #Preaparación de ambiente
        info = json.loads(clients)
        code = """
info = {0}
cur.execute("DELETE FROM clients WHERE rfc = '%s'" % info[0]['rfc'])
sql = 'INSERT INTO clients (person_contact, cpm, budget, status, email, "createdAt", updated_at, ' \
   'password, company_name, rfc, phone, address) ' \
   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)' 
val = (info[0]['name'], info[0]['cpm'], info[0]['budget'], 1, info[0]['email'], strftime("%Y/%m/%d"), \
   strftime("%Y/%m/%d"), info[0]['password'], info[0]['company'], info[0]['rfc'], info[0]['phone'], info[0]['address'])
cur.execute(sql, val)""".format(info)
        db_functions(code)

    def test_detail_client_success(self):
        browserName = self.driver.capabilities['browserName']
        #print(browserName)
        mi_ruta = "clients/client/screenshot/test_detail_client_success"
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
        driver.find_element_by_xpath('//*[@id="client-info-header"]/a[1]').click()
        self.assertIn(modelConfig.baseUrl+"/admin/clients", driver.current_url, msg=None)
        screenshot(self, mi_ruta)
        sleep(3)

    def tearDown(self):
        logout(self)
        self.driver.close()

if __name__ == "__main__":
    unittest.main()