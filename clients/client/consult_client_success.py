import unittest
import time
import json
from util.functions import db_functions, logout, login
from util.config import modelConfig

clients = '''
        [{ "email" : "RUIZ@gmail.com","name" : "OSCAR IGNACIO ALVAREZ CHAGOYA","password" : "ALVAREZ", "cpm" : "99",
        "budget" : "0.08", "company" : "AUTO TRANSPORTES DE CARGA RUIZ HERMANOS SA DE CV", "rfc" : "ATC900103NR1",
         "address" : "CARRET. PESQUERIA KM .600 LADRILLERA, PESQUERIA N.L CP 66650",
        "phone" : "3121256985"
        }]'''
rfcinexist="AEAS860120H3A"

class ConsultClient(unittest.TestCase):

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

    def test_consult_client_success(self):
        browserName = self.driver.capabilities['browserName']
        #print(browserName)
        info = json.loads(clients)

        #login
        login(self)
        time.sleep(3)
        driver = self.driver
        self.assertIn("http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/", driver.current_url,
                      msg=None)
        # time.sleep(3)
        # driver.find_element_by_xpath('//*[@id="sections-access"]/div[2]/a').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
        driver.find_element_by_id('search').send_keys(rfcinexist)
        time.sleep(3)
        self.assertEqual("No record found", driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr/td')
                         .text, msg=None)
        time.sleep(3)
        driver.find_element_by_id('search').clear()
        if browserName == 'internet explorer':
            driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
        driver.find_element_by_id('search').send_keys(info[0]['rfc'])
        time.sleep(3)
        self.assertEqual(info[0]['email'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[1]')
                         .text, msg=None)
        self.assertEqual(info[0]['name'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[2]')
                         .text, msg=None)
        self.assertEqual(info[0]['rfc'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[3]')
                         .text, msg=None)
        self.assertEqual(info[0]['cpm'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[4]')
                         .text, msg=None)
        time.sleep(3)

    def tearDown(self):
        logout(self)
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
