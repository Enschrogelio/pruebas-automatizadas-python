import json
import unittest

from util.functions import ModelConfig, login, logout, db_functions, sleep, screenshot

# DATA SET
clients = '''
        [{ "email": "VERACRUZANA@gmail.com","name": "SANTIAGO CONRADO ALAMILLA CABRERA", "password": "VERACRUZANA", 
        "cpm": "99", "budget": "0.08", "company": "CADENA COMERCIAL VERACRUZANA, S.A. DE C.V.", 
        "rfc": "CCV921218Q84", "address": "CARRET. PESQUERIA KM .600 LADRILLERA, PESQUERIA N.L CP 66650",
        "phone": "3121256985"
        }]'''
campaign = '''
[{"name": "PUBLICIDAD EN MARQUESINAS", "budget": "2.00", "url": "https://youtu.be/_Uj-MMAys4M", "objetive": "2",
"industry": "Consumo", "category": "Telecomunicaciones", "camcode": "MARQUESINAS-75"}]'''
client = json.loads(clients)
campaign = json.loads(campaign)
client_id = "361084056659-tjo3kas6ftsijf99ejsejnk93cuecdo0.apps.googleusercontent.com"
client_secret = "F7BcoQXmw9JX3nA4hGaSxzJl"
path_screenshot = 'clients/campaigns/connections/screenshot/'


class ConnectionDoubleClickManager(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web
        browser_name = self.driver.capabilities['browserName']
        if browser_name == "chrome":
            self.driver.maximize_window()
        # login
        login(self)

        # ENVIROMENT SETTING
        code = """
client = {0}
campaign = {1}
cur.execute("DELETE FROM clients WHERE email = '%s'" % client[0]['email'])
cur.execute("DELETE FROM campaigns WHERE name = '%s'" % campaign[0]['name'])
sql_clients = 'INSERT INTO clients (person_contact, cpm, budget, status, email, "created_at", updated_at, ' \
'password, company_name, rfc, phone, address) ' \
'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)  RETURNING id' 
val_clients = (client[0]['name'], client[0]['cpm'], client[0]['budget'], 1, client[0]['email'],strftime("%Y/%m/%d"), \
strftime("%Y/%m/%d"), client[0]['password'], client[0]['company'], client[0]['rfc'], client[0]['phone'], \
client[0]['address'])
cur.execute(sql_clients, val_clients)
sql_campaign = 'INSERT INTO campaigns (url, cam_code, name, budget, objetive, industry, category, created_at, ' \
    'updated_at, redirect_url, script_snippet, status, dbm_client_secret, dbm_client_id, ' \
    'client_id) ' \
    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
val_campaign = (campaign[0]['url'], campaign[0]['camcode'], campaign[0]['name'], campaign[0]['budget'], 
campaign[0]['objetive'], campaign[0]['industry'], campaign[0]['category'], strftime("%Y/%m/%d"), 
strftime("%Y/%m/%d"), '', '', 1, '', '', cur.fetchone()[0])
cur.execute(sql_campaign, val_campaign)""".format(client, campaign)
        db_functions(code)

    def test_double_click_manager(self):
        path = path_screenshot + "test_double_click_manager"
        sleep(3)
        driver = self.driver
        self.assertIn(ModelConfig.base_url+"/admin/clients/", driver.current_url, msg=None)
        sleep(3)
        driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
        driver.find_element_by_id('search').send_keys(client[0]['rfc'])
        sleep(2)
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr/td[5]/a[1]').click()
        sleep(3)
        self.assertIn(ModelConfig.base_url+"/admin/client/detail/", driver.current_url, msg=None)
        driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr/td[8]/a[1]').click()
        sleep(3)
        self.assertIn(ModelConfig.base_url+"/admin/campaign/detail/", driver.current_url, msg=None)
        self.assertEqual(campaign[0]['name'], driver.find_element_by_xpath('//*[@id="client-info-header"]/h2')
                         .text, msg=None)
        self.assertEqual("DoubleClick Manager", driver.find_element_by_xpath('/html/body/div[4]/h2')
                         .text, msg=None)
        self.assertEqual("To improve your campaign, connect with DoubleClick Manager. Check the connection guide",
                         driver.find_element_by_xpath('/html/body/div[4]/div/div/span').text, msg=None)
        self.assertEqual("Client ID",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[1]/div/label').text, msg=None)
        self.assertEqual("Client Secret",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[2]/div/label').text, msg=None)
        self.assertEqual("CONNECT",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[3]/div/button')
                         .text.upper(), msg=None)
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[1]/div/input').send_keys(client_id)
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[2]/div/input').send_keys(client_secret)
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[3]/div/button').click()
        # ESTE TEXTO SE COMENTÓ DEBIDO A QUE NO PUEDE REALIZARSE LA CONEXIÓN EN STAGE
        #self.assertEqual("Successful connection",
        #                 driver.find_element_by_css_selector('//*[@id="dbm_tab"]/span[2]').text.upper(), msg=None)
        screenshot(self, path)
        driver.refresh()
        sleep(2)
        driver.find_element_by_xpath('//*[@id="client-info-header"]/a[1]').click()
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[1]/div/input')
                         .get_attribute("value"), client_id, msg=None)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[2]/div/input')
                         .get_attribute("value"), client_secret, msg=None)
        screenshot(self, path)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
