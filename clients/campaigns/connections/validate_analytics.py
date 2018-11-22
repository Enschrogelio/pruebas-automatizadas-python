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


class ValidateAnalytics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = ModelConfig.driver_web
        login(cls)

        # ENVIROMENT SETTING
        client1 = json.loads(clients)
        campaign1 = json.loads(campaigns)
        code = """
client = {0}
campaign = {1}
cur.execute("DELETE FROM clients WHERE email = '%s'" % client[0]['email'])
cur.execute("DELETE FROM campaigns WHERE name = '%s'" % campaign[0]['name'])
sql_clients = 'INSERT INTO clients (person_contact, cpm, budget, status, email, "createdAt", updated_at, ' \
'password, company_name, rfc, phone, address) ' \
'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)  RETURNING id' 
val_clients = (client[0]['name'], client[0]['cpm'], client[0]['budget'], 1, client[0]['email'],strftime("%Y/%m/%d"), \
strftime("%Y/%m/%d"), client[0]['password'], client[0]['company'], client[0]['rfc'], client[0]['phone'], \
client[0]['address'])
cur.execute(sql_clients, val_clients)
sql_campaign = 'INSERT INTO campaigns (url, cam_code, name, budget, objetive, industry, category, created_at, ' \
    'updated_at, redirect_url, script_snippet, status, ga_api_key, ga_api_secret,dbm_client_secret, dbm_client_id, ' \
    'client_id) ' \
    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s, %s, %s, %s, %s, %s, %s, %s)'
val_campaign = (campaign[0]['url'], campaign[0]['camcode'], campaign[0]['name'], campaign[0]['budget'], 
campaign[0]['objetive'], campaign[0]['industry'], campaign[0]['category'], strftime("%Y/%m/%d"), 
strftime("%Y/%m/%d"), '', '', 1, '', '', '', '', cur.fetchone()[0])
cur.execute(sql_campaign, val_campaign)""".format(client1, campaign1)
        db_functions(code)
        sleep(3)
        cls.driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
        cls.driver.find_element_by_id('search').send_keys(client[0]['rfc'])
        sleep(2)
        cls.driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr/td[6]/a[1]').click()
        sleep(2)
        cls.driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr/td[10]/a[1]').click()
        sleep(2)

    def test_analytics_data_required(self):
        path = path_screenshot + "test_analytics_data_required"
        sleep(2)
        driver = self.driver
        self.assertIn(ModelConfig.base_url+"/admin/campaign/detail/", driver.current_url, msg=None)
        self.assertEqual(campaign[0]['name'], driver.find_element_by_xpath('//*[@id="client-info-header"]/h2')
                         .text, msg=None)
        self.assertEqual("Google Analytics", driver.find_element_by_xpath('//*[@id="ga_link"]')
                         .text, msg=None)
        driver.find_element_by_xpath('//*[@id="ga_link"]/a').click()
        self.assertEqual("To improve your campaign, connect with Google Analytics. Check the connection guide",
                         driver.find_element_by_xpath('//*[@id="ga_tab"]/span').text, msg=None)
        self.assertEqual("API key",
                         driver.find_element_by_xpath('//*[@id="form-ga"]/div/div[1]/div/label').text, msg=None)
        self.assertEqual("API secret key",
                         driver.find_element_by_xpath('//*[@id="form-ga"]/div/div[2]/div/label').text, msg=None)
        self.assertEqual("CONNECT",
                         driver.find_element_by_css_selector('#form-ga > div > div:nth-child(3) > button')
                         .text.upper(), msg=None)
        driver.find_element_by_name('client_id').clear()
        driver.find_element_by_name('client_secret').clear()
        driver.find_element_by_css_selector('#form-ga > div > div:nth-child(3) > button').click()
        sleep(3)
        self.assertEqual("This field is empty",
                         driver.find_element_by_css_selector('#form-ga > div > div:nth-child(1) > div > span')
                         .text, msg=None)
        self.assertEqual("This field is empty",
                         driver.find_element_by_css_selector('#form-ga > div > div:nth-child(2) > div > span')
                         .text, msg=None)
        screenshot(self, path)

    def test_analytics_client_secret_error(self):
        path = path_screenshot + "test_analytics_client_secret_error"
        sleep(2)
        driver = self.driver
        self.assertIn(ModelConfig.base_url+"/admin/campaign/detail/", driver.current_url, msg=None)
        self.assertEqual(campaign[0]['name'], driver.find_element_by_xpath('//*[@id="client-info-header"]/h2')
                         .text, msg=None)
        self.assertEqual("Google Analytics", driver.find_element_by_xpath('//*[@id="ga_link"]')
                         .text, msg=None)
        driver.find_element_by_xpath('//*[@id="ga_link"]/a').click()
        self.assertEqual("To improve your campaign, connect with Google Analytics. Check the connection guide",
                         driver.find_element_by_xpath('//*[@id="ga_tab"]/span').text, msg=None)
        self.assertEqual("API key",
                         driver.find_element_by_xpath('//*[@id="form-ga"]/div/div[1]/div/label').text, msg=None)
        self.assertEqual("API secret key",
                         driver.find_element_by_xpath('//*[@id="form-ga"]/div/div[2]/div/label').text, msg=None)
        self.assertEqual("CONNECT",
                         driver.find_element_by_css_selector('#form-ga > div > div:nth-child(3) > button')
                         .text.upper(), msg=None)
        current_url = driver.current_url
        driver.find_element_by_name('client_id').send_keys(client_id_correct)
        driver.find_element_by_name('client_secret').send_keys(client_secret_error)
        driver.find_element_by_css_selector('#form-ga > div > div:nth-child(3) > button').click()
        sleep(3)
        self.assertEqual("Failed connection, check credentials and try again",
                         driver.find_element_by_xpath('//*[@id="ga_tab"]/span[2]').text, msg=None)
        sleep(2)
        screenshot(self, path)
        driver.get(current_url)

    def test_analytics_client_id_error(self):
        path = path_screenshot + "test_analytics_client_id_error"
        sleep(2)
        driver = self.driver
        self.assertIn(ModelConfig.base_url+"/admin/campaign/detail/", driver.current_url, msg=None)
        self.assertEqual(campaign[0]['name'], driver.find_element_by_xpath('//*[@id="client-info-header"]/h2')
                         .text, msg=None)
        self.assertEqual("Google Analytics", driver.find_element_by_xpath('//*[@id="ga_link"]')
                         .text, msg=None)
        driver.find_element_by_xpath('//*[@id="ga_link"]/a').click()
        self.assertEqual("To improve your campaign, connect with Google Analytics. Check the connection guide",
                         driver.find_element_by_xpath('//*[@id="ga_tab"]/span').text, msg=None)
        self.assertEqual("API key",
                         driver.find_element_by_xpath('//*[@id="form-ga"]/div/div[1]/div/label').text, msg=None)
        self.assertEqual("API secret key",
                         driver.find_element_by_xpath('//*[@id="form-ga"]/div/div[2]/div/label').text, msg=None)
        self.assertEqual("CONNECT",
                         driver.find_element_by_css_selector('#form-ga > div > div:nth-child(3) > button')
                         .text.upper(), msg=None)
        current_url = driver.current_url
        driver.find_element_by_name('client_id').send_keys(client_id_error)
        driver.find_element_by_name('client_secret').send_keys(client_secret_correct)
        driver.find_element_by_css_selector('#form-ga > div > div:nth-child(3) > button').click()
        sleep(3)
        self.assertEqual("401. That’s an error.",
                         driver.find_element_by_xpath('//*[@id="af-error-container"]/p[1]').text, msg=None)
        self.assertEqual("Error: invalid_client",
                         driver.find_element_by_xpath('//*[@id="errorCode"]/b').text, msg=None)
        self.assertEqual("The OAuth client was not found.",
                         driver.find_element_by_xpath('//*[@id="errorDescription"]').text, msg=None)
        screenshot(self, path)
        driver.get(current_url)

    def test_analytics_client_secret_client_id_error(self):
        path = path_screenshot + "test_analytics_client_secret_client_id_error"
        sleep(2)
        driver = self.driver
        self.assertIn(ModelConfig.base_url+"/admin/campaign/detail/", driver.current_url, msg=None)
        self.assertEqual(campaign[0]['name'], driver.find_element_by_xpath('//*[@id="client-info-header"]/h2')
                         .text, msg=None)
        self.assertEqual("Google Analytics", driver.find_element_by_xpath('//*[@id="ga_link"]')
                         .text, msg=None)
        driver.find_element_by_xpath('//*[@id="ga_link"]/a').click()
        self.assertEqual("To improve your campaign, connect with Google Analytics. Check the connection guide",
                         driver.find_element_by_xpath('//*[@id="ga_tab"]/span').text, msg=None)
        self.assertEqual("API key",
                         driver.find_element_by_xpath('//*[@id="form-ga"]/div/div[1]/div/label').text, msg=None)
        self.assertEqual("API secret key",
                         driver.find_element_by_xpath('//*[@id="form-ga"]/div/div[2]/div/label').text, msg=None)
        self.assertEqual("CONNECT",
                         driver.find_element_by_css_selector('#form-ga > div > div:nth-child(3) > button')
                         .text.upper(), msg=None)
        current_url = driver.current_url
        driver.find_element_by_name('client_id').send_keys(client_id_error)
        driver.find_element_by_name('client_secret').send_keys(client_secret_error)
        driver.find_element_by_css_selector('#form-ga > div > div:nth-child(3) > button').click()
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
