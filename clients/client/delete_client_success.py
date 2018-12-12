import unittest
import json
from util.functions import ModelConfig, login, logout, db_functions, sleep, screenshot

# DATA SET
clients = '''
        [{ "email" : "ECOLOGICOS@gmail.com","name" : "PEDRO ALBERTO ARAMBURA CONTRERAS" ,"password" : "ARAMBURA", 
        "cpm" : "18", "budget" : "10000.52", "company" : "ASESORIA Y SERVICIOS ECOLOGICOS INTEGRALES S.A.", 
        "rfc" : "ASE0009266M0", "address" : "BRONCE #9326 CD INDUSTRIAL MITRAS GARCIA N.L. C.P. 66000",
        "phone" : "3128256987"
        },
        { "email" : "HUASTECAS@gmail.com","name" : "MOISES JOSUE ALCANTARA CABADILLA","password" : "ALCANTARA", 
        "cpm" : "1", "budget" : "15000.90", "company" : "AUTOTRANSPORTES RAPIDOS DOS HUASTECAS S A DE C V", 
        "rfc" : "ASS001002KX0", "address" : "2 DE ABRIL NUM 1022 ORIENTE COL INDEPENDENCIA MONTERREY N L",
        "phone" : "3125256987"
        }]'''


class DeleteClient(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()
        # ENVIROMENT SETTING
        info = json.loads(clients)
        code = """
info = {0}
cur.execute("DELETE FROM clients WHERE rfc = '%s'" % info[0]['rfc'])
sql = 'INSERT INTO clients (person_contact, cpm, budget, status, email, "created_at", updated_at, ' \
   'password, company_name, rfc, phone, address) ' \
   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)' 
val = (info[0]['name'], info[0]['cpm'], info[0]['budget'], 1, info[0]['email'], strftime("%Y/%m/%d"), \
   strftime("%Y/%m/%d"), info[0]['password'], info[0]['company'], info[0]['rfc'], info[0]['phone'], info[0]['address'])
cur.execute(sql, val)""".format(info)
        db_functions(code)

    def test_delete_client_success(self):
        info = json.loads(clients)
        path = "clients/client/screenshot/test_delete_client_success"
        # login
        login(self)
        sleep(3)
        driver = self.driver
        self.assertIn("http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/", driver.current_url,
                      msg=None)
        sleep(3)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[2]/a').click()
        sleep(1)
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
        self.assertEqual("active", driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[5]')
                         .text, msg=None)
        sleep(3)
        screenshot(self, path)
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[6]/a[3]').click()
        sleep(3)
        self.assertEqual("Deleting record", driver.find_element_by_xpath('//*[@id="modal-delete"]/div/div/div[2]/h2')
                         .text, msg=None)
        driver.find_element_by_xpath('//*[@id="modal-delete"]/div/div/div[3]/div[2]/button').click()
        sleep(3)
        self.assertEqual("Are you sure to delete this record:",
                         driver.find_element_by_xpath('//*[@id="modal-confirm"]/div/div/div[1]/h1').text, msg=None)
        self.assertEqual("Deleting this record, will eraser the campaigns and creative relating with it",
                         driver.find_element_by_xpath('//*[@id="modal-confirm"]/div/div/div[1]/p').text, msg=None)
        self.assertEqual("Enter the confirmation:",
                         driver.find_element_by_xpath('//*[@id="modal-confirm"]/div/div/div[2]/p').text, msg=None)
        driver.find_element_by_xpath('//*[@id="btn-submit"]').click()
        sleep(3)
        self.assertEqual("This field doesnt match with the record.",
                         driver.find_element_by_xpath('//*[@id="form-confirm"]/div/span').text.rstrip(' '), msg=None)
        screenshot(self, path)
        driver.find_element_by_xpath('//*[@id="input-email"]').clear()
        driver.find_element_by_xpath('//*[@id="input-email"]').send_keys("BATALLON@GMAIL")
        driver.find_element_by_xpath('//*[@id="btn-submit"]').click()
        sleep(3)
        self.assertEqual("This field doesnt match with the record.",
                         driver.find_element_by_xpath('//*[@id="form-confirm"]/div/span').get_attribute('innerHTML')
                         .rstrip(' '), msg=None)
        screenshot(self, path)
        driver.find_element_by_xpath('//*[@id="input-email"]').clear()
        driver.find_element_by_xpath('//*[@id="input-email"]').send_keys(info[0]['email'])
        driver.find_element_by_xpath('//*[@id="btn-submit"]').click()
        sleep(5)
        # driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
        # driver.find_element_by_id('search').send_keys(info[0]['rfc'])
        # sleep(3)
        self.assertEqual(info[0]['email'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[1]')
                         .text, msg=None)
        self.assertEqual(info[0]['name'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[2]')
                         .text, msg=None)
        self.assertEqual(info[0]['rfc'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[3]')
                         .text, msg=None)
        self.assertEqual(info[0]['cpm'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[4]')
                         .text, msg=None)
        self.assertEqual("deleted", driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[5]')
                         .text, msg=None)

        screenshot(self, path)
        sleep(3)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
