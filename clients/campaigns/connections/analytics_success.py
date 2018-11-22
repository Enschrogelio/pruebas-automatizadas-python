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

class ConnectionGoogelAnalytics(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web
        # login
        login(self)

        # ENVIROMENT SETTING
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
cur.execute(sql_campaign, val_campaign)""".format(client, campaign)
        db_functions(code)

    def test_google_analytics(self):
        path = path_screenshot + "test_google_analytics"
        sleep(3)
        driver = self.driver
        self.assertIn(ModelConfig.base_url+"/admin/clients/", driver.current_url, msg=None)
        sleep(3)
        driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
        driver.find_element_by_id('search').send_keys(client[0]['rfc'])
        sleep(3)
        self.assertEqual(client[0]['email'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[1]')
                         .text, msg=None)
        self.assertEqual(client[0]['name'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[2]')
                         .text, msg=None)
        self.assertEqual(client[0]['rfc'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[3]')
                         .text, msg=None)
        self.assertEqual(client[0]['cpm'], driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[4]')
                         .text, msg=None)
        screenshot(self, path)
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr/td[6]/a[1]').click()
        sleep(3)
        self.assertIn(ModelConfig.base_url+"/admin/client/detail/", driver.current_url, msg=None)
        self.assertEqual(client[0]['company'], driver.find_element_by_xpath('//*[@id="client-info-header"]/h2')
                         .text, msg=None)
        sleep(3)
        self.assertEqual(campaign[0]['camcode'],
                         driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr/td[2]').text, msg=None)
        self.assertEqual(campaign[0]['name'],
                         driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr/td[3]').text, msg=None)
        self.assertEqual(campaign[0]['industry'],
                         driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr/td[4]').text, msg=None)
        self.assertEqual(campaign[0]['category'],
                         driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr/td[5]').text, msg=None)
        screenshot(self, path)
        driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr/td[10]/a[1]').click()
        sleep(3)
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
        driver.find_element_by_name('client_id').send_keys(client_id)
        driver.find_element_by_name('client_secret').send_keys(client_secret)
        driver.find_element_by_css_selector('#form-ga > div > div:nth-child(3) > button').click()
        # self.assertEqual("Successful connection",
        #                  driver.find_element_by_css_selector('//*[@id="ga_tab"]/span[2]').text msg=None)
        screenshot(self, path)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
