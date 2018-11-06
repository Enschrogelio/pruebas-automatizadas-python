import unittest
import time
import json
from random import randint
from util.functions import db_functions, logout, login, screenshot
from util.config import modelConfig

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
        },
        { "email" : "RUIZ@gmail.com","name" : "OSCAR IGNACIO ALVAREZ CHAGOYA","password" : "ALVAREZ", "cpm" : "99",
        "budget" : "0.08", "company" : "AUTO TRANSPORTES DE CARGA RUIZ HERMANOS SA DE CV", "rfc" : "ATC900103NR1",
         "address" : "CARRET. PESQUERIA KM .600 LADRILLERA, PESQUERIA N.L CP 66650",
        "phone" : "3121256985"
        }]'''

class AddClient(unittest.TestCase):

    def setUp(self):
        global clients
        self.driver = modelConfig.driverWeb
        #Preaparación de ambiente
        info = json.loads(clients)
        code = """
info = {0}
for elemento in info:
    cur.execute("DELETE FROM clients WHERE rfc = '%s'" % elemento['rfc'])
""".format(info)
        db_functions(code)

    def test_add_client_success(self):
        global clients

        info = json.loads(clients)
        rand = randint(0, len(info) - 1)

        # login
        login(self)
        time.sleep(3)
        driver = self.driver
        self.assertIn("http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/", driver.current_url,
                      msg=None)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="id_email"]').send_keys(info[rand]['email'])
        driver.find_element_by_xpath('//*[@id="id_person_contact"]').send_keys(info[rand]['name'])
        driver.find_element_by_xpath('//*[@id="id_status"]').click()
        driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(info[rand]['password'])
        driver.find_element_by_xpath('//*[@id="id_cpm"]').send_keys(info[rand]['cpm'])
        driver.find_element_by_xpath('//*[@id="id_budget"]').send_keys(info[rand]['budget'])
        driver.find_element_by_xpath('//*[@id="id_company_name"]').send_keys(info[rand]['company'])
        driver.find_element_by_xpath('//*[@id="id_rfc"]').send_keys(info[rand]['rfc'])
        driver.find_element_by_xpath('//*[@id="id_address"]').send_keys(info[rand]['address'])
        driver.find_element_by_xpath('//*[@id="id_phone"]').send_keys(info[rand]['phone'])
        driver.find_element_by_xpath("//*[@id='modal-add']/div[1]/div[1]/div[3]/button[1 and @type='submit']").click()
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
        driver.find_element_by_id('search').send_keys(info[rand]['rfc'])
        time.sleep(5)
        self.assertEqual(info[rand]['email'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[1]')
                         .text, msg=None)
        self.assertEqual(info[rand]['name'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[2]')
                         .text, msg=None)
        self.assertEqual(info[rand]['rfc'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[3]')
                         .text, msg=None)
        self.assertEqual(info[rand]['cpm'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[4]')
                         .text, msg=None)
        self.assertEqual('active', driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[5]')
                         .text, msg=None)
        mi_ruta = "clients/client/screenshot/test_add_client_success"
        screenshot(self, mi_ruta)
        time.sleep(5)

    def tearDown(self):
        logout(self)
        self.driver.close()

if __name__ == "__main__":
    unittest.main()