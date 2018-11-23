import json
import unittest

from selenium.common.exceptions import NoSuchElementException

from util.functions import *
from util.config import *
from util.functions import login

campaign='''
    [{"name" : "Coca-cola company","budget":"2.00", "url":"https://www.google.com","objetive":"2"},
    {"name" : "Rogelio 2","budget":"5.0","url":"https://www.facebook.com/","objetive":"4.0"}]'''


class AddCampaignSuccess(unittest.TestCase):

    def setUp(self):
        global campaign
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()
        info = json.loads(campaign)
        code = """
info = {0}
cur.execute("DELETE FROM campaigns WHERE name = '%s' AND budget = '%s' AND objetive = '%s'" %(info[0]['name'], 
            info[0]['budget'], info[0]['objetive']))
    """.format(info)
        db_functions(code)
        # print("DELETE FROM campaigns WHERE name = '%s' AND budget = '%s' AND objetive = '%s' AND url =
        # '%s'%("+info[0]['name']+", "+info[0]['budget']+", "+info[0]['url']+", "+info[0]['objetive']+")")

    def test_campaign(self):
        global campaign
        driver = self.driver
        info = json.loads(campaign)
        # login
        login(self)
        sleep(2)
        # Click en clientes
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[6]/a[1]/i').click()
        sleep(1)
        # Click en view
        driver.find_element_by_xpath('//*[@id="client-camp-header"]/div/button').click()
        sleep(1)
        # llenado de Form
        # name
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').send_keys((info[0]['name']))
        sleep(2)
        # Seleccionar Select contenedor ACTIVE
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[2]').click()
        sleep(3)
        # Seleccionar Active
        aleatorio = random.randint(1 , 3)
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[2]/select/option[%d]' % aleatorio).click()
        #driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[2]/select/option[2]').click()
        sleep(2)
        # Seleccionar Select contenedor INDUSTRIA
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[3]').click()
        sleep(2)
        # Seleccionar AUTOMOTRIZ
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[3]/select/option[6]').click()
        sleep(2)
        # Seleccionar Select contenedor CATEGORY
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[4]').click()
        sleep(2)
        # Seleccionar CELULARES
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[4]/select/option[6]').click()
        # BUGET
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').send_keys((info[0]['budget']))
        # URL
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').send_keys((info[0]['url']))
        # OBJETIVE
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').send_keys((info[0]['objetive']))
        # enter
        driver.find_element_by_xpath("//div[10]/div[1]/div[1]/div[3]/button[1]").click()
        sleep(3)
        try:
            while driver.find_element_by_xpath('//tr[1]/td[3]').get_attribute(info[0]['name']):
                self.assertEqual(info[0]['name'], driver.find_element_by_xpath('//tr[1]/td[3]').text, msg=None)
                self.assertEqual(info[0]['budget'], driver.find_element_by_xpath('//tr[1]/td[6]').text, msg=None)
                self.assertEqual(info[0]['objetive'], driver.find_element_by_xpath('//tr[1]/td[7]').text, msg=None)
                sleep(2)
        except Exception:
            driver.find_element_by_xpath('//*[@id="client-camp-links"]/a[2]').click()
            sleep(2)
            self.assertEqual(info[0]['name'], driver.find_element_by_xpath('//tr[1]/td[3]').text, msg=None)
            self.assertEqual(info[0]['budget'], driver.find_element_by_xpath('//tr[1]/td[6]').text, msg=None)
            self.assertEqual(info[0]['objetive'], driver.find_element_by_xpath('//tr[1]/td[7]').text, msg=None)
            sleep(2)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()