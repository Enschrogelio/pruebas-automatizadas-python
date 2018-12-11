import unittest
import json
from util.functions import ModelConfig, login, logout, db_functions, sleep, screenshot

# DATA SET
clients = '''
        [{ "email": "VERACRUZANA@gmail.com","name": "SANTIAGO CONRADO ALAMILLA CABRERA","password": "VERACRUZANA", 
        "cpm": "99", "budget": "0.08", "company": "CADENA COMERCIAL VERACRUZANA, S.A. DE C.V.", 
        "rfc": "CCV921218Q84", "address": "CARRET. PESQUERIA KM .600 LADRILLERA, PESQUERIA N.L CP 66650",
        "phone": "3121256985"
        }]'''

campaigns = '''
[{"name": "PUBLICIDAD EN MARQUESINAS", "budget": "2.00", "url": "https://youtu.be/_Uj-MMAys4M", "objetive": "2",
"industry": "Consumo", "category": "Telecomunicaciones", "camcode": "MARQUESINAS-75"}]'''
client = json.loads(clients)
campaign = json.loads(campaigns)
client_id_correct = "361084056659-tjo3kas6ftsijf99ejsejnk93cuecdo0.apps.googleusercontent.com"
client_secret_correct = "F7BcoQXmw9JX3nA4hGaSxzJl"
client_id_error = "361084056659-tjo3kas6ftsijf99ejsejnk93cuecdo0.apps.googleusercontent"
client_secret_error = "F7BcoQXmw9JX3nA4hGaSxzJl2"
path_screenshot = 'clients/campaigns/connections/screenshot/'


class ValidateDoubleClickManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = ModelConfig.driver_web
        browser_name = cls.driver.capabilities['browserName']
        if browser_name == "chrome":
            cls.driver.maximize_window()
        login(cls)

        # ENVIROMENT SETTING
        client1 = json.loads(clients)
        campaign1 = json.loads(campaigns)
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
        sleep(3)
        cls.driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
        cls.driver.find_element_by_id('search').send_keys(client[0]['rfc'])
        sleep(2)
        cls.driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr/td[6]/a[1]').click()
        sleep(2)
        cls.driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr/td[10]/a[1]').click()

    def test_manager_data_required(self):
        path = path_screenshot + "test_analytics_data_required"
        sleep(3)
        driver = self.driver
        self.assertIn(ModelConfig.base_url+"/admin/campaign/detail/", driver.current_url, msg=None)
        self.assertEqual(campaign[0]['name'], driver.find_element_by_xpath('//*[@id="client-info-header"]/h2')
                         .text, msg=None)
        self.assertEqual("DoubleClick Manager", driver.find_element_by_xpath('/html/body/div[4]/h2')
                         .text, msg=None)
        self.assertEqual("To improve your campaign, connect with DoubleClick Mannager. Check the connection guide",
                         driver.find_element_by_xpath('/html/body/div[4]/div/div/span').text, msg=None)
        self.assertEqual("Client ID",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[1]/div/label').text, msg=None)
        self.assertEqual("Client Secret",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[2]/div/label').text, msg=None)
        self.assertEqual("CONNECT",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[3]/div/button')
                         .text.upper(), msg=None)
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[1]/div/input').clear()
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[2]/div/input[1]').clear()
        current_url = driver.current_url
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[3]/div/button').click()
        sleep(3)
        self.assertEqual("This field is empty",
                         driver.find_element_by_css_selector('#form-dbm > div > div:nth-child(1) > div > span')
                         .text, msg=None)
        self.assertEqual("This field is empty",
                         driver.find_element_by_css_selector('#form-dbm > div > div:nth-child(2) > div > span')
                         .text, msg=None)
        screenshot(self, path)
        driver.get(current_url)

    def test_manager_client_secret_error(self):
        path = path_screenshot + "test_manager_client_secret_error"
        sleep(2)
        driver = self.driver
        self.assertIn(ModelConfig.base_url+"/admin/campaign/detail/", driver.current_url, msg=None)
        self.assertEqual(campaign[0]['name'], driver.find_element_by_xpath('//*[@id="client-info-header"]/h2')
                         .text, msg=None)
        self.assertEqual("DoubleClick Manager", driver.find_element_by_xpath('/html/body/div[4]/h2')
                         .text, msg=None)
        self.assertEqual("To improve your campaign, connect with DoubleClick Mannager. Check the connection guide",
                         driver.find_element_by_xpath('/html/body/div[4]/div/div/span').text, msg=None)
        self.assertEqual("Client ID",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[1]/div/label').text, msg=None)
        self.assertEqual("Client Secret",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[2]/div/label').text, msg=None)
        self.assertEqual("CONNECT",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[3]/div/button')
                         .text.upper(), msg=None)
        current_url = driver.current_url
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[1]/div/input').send_keys(client_id_correct)
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[2]/div/input[1]').send_keys(client_secret_error)
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[3]/div/button').click()
        sleep(3)
        self.assertEqual("Failed connection, check credentials and try again",
                         driver.find_element_by_xpath('//*[@id="dbm_tab"]/span[2]').text, msg=None)
        sleep(2)
        screenshot(self, path)
        driver.get(current_url)

    def test_manager_client_id_error(self):
        path = path_screenshot + "test_manager_client_id_error"
        sleep(2)
        driver = self.driver
        self.assertIn(ModelConfig.base_url+"/admin/campaign/detail/", driver.current_url, msg=None)
        self.assertEqual(campaign[0]['name'], driver.find_element_by_xpath('//*[@id="client-info-header"]/h2')
                         .text, msg=None)
        self.assertEqual("DoubleClick Manager", driver.find_element_by_xpath('/html/body/div[4]/h2')
                         .text, msg=None)
        self.assertEqual("To improve your campaign, connect with DoubleClick Mannager. Check the connection guide",
                         driver.find_element_by_xpath('/html/body/div[4]/div/div/span').text, msg=None)
        self.assertEqual("Client ID",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[1]/div/label').text, msg=None)
        self.assertEqual("Client Secret",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[2]/div/label').text, msg=None)
        self.assertEqual("CONNECT",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[3]/div/button')
                         .text.upper(), msg=None)
        current_url = driver.current_url
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[1]/div/input').send_keys(client_id_error)
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[2]/div/input[1]').send_keys(client_secret_correct)
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[3]/div/button').click()
        sleep(3)
        self.assertEqual("401. That’s an error.",
                         driver.find_element_by_xpath('//*[@id="af-error-container"]/p[1]').text, msg=None)
        self.assertEqual("Error: invalid_client",
                         driver.find_element_by_xpath('//*[@id="errorCode"]/b').text, msg=None)
        self.assertEqual("The OAuth client was not found.",
                         driver.find_element_by_xpath('//*[@id="errorDescription"]').text, msg=None)
        screenshot(self, path)
        driver.get(current_url)

    def test_manager_client_secret_client_id_error(self):
        path = path_screenshot + "test_manager_client_secret_client_id_error"
        sleep(2)
        driver = self.driver
        self.assertIn(ModelConfig.base_url+"/admin/campaign/detail/", driver.current_url, msg=None)
        self.assertEqual(campaign[0]['name'], driver.find_element_by_xpath('//*[@id="client-info-header"]/h2')
                         .text, msg=None)
        self.assertEqual("DoubleClick Manager", driver.find_element_by_xpath('/html/body/div[4]/h2')
                         .text, msg=None)
        self.assertEqual("To improve your campaign, connect with DoubleClick Mannager. Check the connection guide",
                         driver.find_element_by_xpath('/html/body/div[4]/div/div/span').text, msg=None)
        self.assertEqual("Client ID",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[1]/div/label').text, msg=None)
        self.assertEqual("Client Secret",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[2]/div/label').text, msg=None)
        self.assertEqual("CONNECT",
                         driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[3]/div/button')
                         .text.upper(), msg=None)
        current_url = driver.current_url
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[1]/div/input').send_keys(client_id_error)
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[2]/div/input[1]').send_keys(client_secret_error)
        driver.find_element_by_xpath('//*[@id="form-dbm"]/div/div[3]/div/button').click()
        sleep(3)
        self.assertEqual("401. That’s an error.",
                         driver.find_element_by_xpath('//*[@id="af-error-container"]/p[1]').text, msg=None)
        self.assertEqual("Error: invalid_client",
                         driver.find_element_by_xpath('//*[@id="errorCode"]/b').text, msg=None)
        self.assertEqual("The OAuth client was not found.",
                         driver.find_element_by_xpath('//*[@id="errorDescription"]').text, msg=None)
        sleep(2)
        screenshot(self, path)
        driver.get(current_url)

    @classmethod
    def tearDownClass(cls):
        logout(cls)
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
