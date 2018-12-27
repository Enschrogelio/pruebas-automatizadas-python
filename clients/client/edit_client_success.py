import unittest
import json
from selenium.webdriver.support.ui import Select
from util.functions import ModelConfig, login, logout, db_functions, sleep, screenshot

# DATA SET
clients = '''
        [{ "email" : "ACARREOS@gmail.com","name" : "MOISES JOSUE ALCANTARA CABADILLA","password" : "ALCANTARA", 
        "cpm" : "1", "budget" : "15000.90", "company" : "ACARREOS ESPECIALIZADOS DE LIQUIDOS, S.A.DE C.V", 
        "rfc" : "AEL850215R87", "address" : "2 DE ABRIL NUM 1022 ORIENTE COL INDEPENDENCIA MONTERREY N L",
        "phone" : "3125256987"
        },
        { "email" : "KAMELLOS@gmail.com","name" : "ALBERTO ARAMBURA CONTRERAS" ,"password" : "ARAMBURA", 
        "cpm" : "18", "budget" : "10000.52", "company" : "AUTOTRANSPORTES DE CARGA LOS KAMELLOS, S.A. DE C.V", 
        "rfc" : "ACK001003D50", "address" : "BRONCE #9326 CD INDUSTRIAL MITRAS GARCIA N.L. C.P. 66000",
        "phone" : "3128256987"
        }]'''


class EditClient(unittest.TestCase):

    def setUp(self):
        global clients
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()
        # ENVIROMENT SETTING
        info = json.loads(clients)
        code = """
info = {0}
cur.execute("SELECT id FROM clients WHERE email = '%s'" % info[1]['email'])
try:
    id = cur.fetchone()[0]
    if id is not None:
        cur.execute("DELETE FROM campaigns WHERE client_id = '%d';" % id)
        cur.execute("DELETE FROM clients WHERE id = '%d';" % id)
except Exception as errorFetch:
    errorFetch
sql = 'INSERT INTO clients (person_contact, cpm, budget, status, email, "created_at", updated_at, ' \
'password, company_name, rfc, phone, address) ' \
'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)' 
val = (info[0]['name'], info[0]['cpm'], info[0]['budget'], 1, info[0]['email'], strftime("%Y/%m/%d"), \
strftime("%Y/%m/%d"), info[0]['password'], info[0]['company'], info[0]['rfc'], info[0]['phone'], info[0]['address'])
cur.execute(sql, val)""".format(info)
        db_functions(code)

    def test_edit_client_success(self):
        global clients
        path = "clients/client/screenshot/test_edit_client_success"

        info = json.loads(clients)
        # login
        login(self)
        sleep(3)
        driver = self.driver

        self.assertIn("http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/", driver.current_url,
                      msg=None)
        sleep(3)
        driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
        driver.find_element_by_id('search').send_keys(info[0]['rfc'])
        sleep(8)
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[5]/a[2]').click()
        sleep(5)
        driver.find_element_by_css_selector('#edit-form-email').clear()
        driver.find_element_by_css_selector('#edit-form-email').send_keys(info[1]['email'])
        driver.find_element_by_css_selector('#edit-form-person_contact').clear()
        driver.find_element_by_css_selector('#edit-form-person_contact').send_keys(info[1]['name'])
        select = Select(driver.find_element_by_css_selector("#edit-form-status"))
        select.select_by_index(1)
        driver.find_element_by_css_selector('#edit-form-password').clear()
        driver.find_element_by_css_selector('#edit-form-password').send_keys(info[1]['password'])
        driver.find_element_by_css_selector('#edit-form-cpm').clear()
        driver.find_element_by_css_selector('#edit-form-cpm').send_keys(info[1]['cpm'])
        driver.find_element_by_css_selector('#edit-form-budget').clear()
        driver.find_element_by_css_selector('#edit-form-budget').send_keys(info[1]['budget'])
        driver.find_element_by_css_selector('#edit-form-company_name').clear()
        driver.find_element_by_css_selector('#edit-form-company_name').send_keys(info[1]['company'])
        driver.find_element_by_css_selector('#edit-form-rfc').clear()
        driver.find_element_by_css_selector('#edit-form-rfc').send_keys(info[1]['rfc'])
        driver.find_element_by_css_selector('#edit-form-address').clear()
        driver.find_element_by_css_selector('#edit-form-address').send_keys(info[1]['address'])
        driver.find_element_by_css_selector('#edit-form-phone').clear()
        driver.find_element_by_css_selector('#edit-form-phone').send_keys(info[1]['phone'])
        screenshot(self, path)
        sleep(3)
        driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
        # self.assertIn("Record successfully updated", driver.page_source)
        sleep(5)
        driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
        driver.find_element_by_id('search').send_keys(info[1]['rfc'])
        sleep(3)
        self.assertEqual(info[1]['email'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[1]')
                         .text, msg=None)
        self.assertEqual(info[1]['name'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[2]')
                         .text, msg=None)
        self.assertEqual(info[1]['rfc'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[3]')
                         .text, msg=None)
        self.assertEqual('inactive', driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[4]')
                         .text, msg=None)
        screenshot(self, path)
        sleep(3)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()