import json
import os
import unittest
from random import randint
from time import sleep

from util.config import ModelConfig
from util.functions import login, db_functions, logout, delete_file

client = "arcapruebas2@gmail.com"
campaign='''
    [{"name" : "Coca-cola company","budget":"2.00", "url":"https://www.google.com","objetive":"2"},
    {"name" : "Rogelio 2","budget":"5.0","url":"https://www.facebook.com/","objetive":"4.0"}]'''
info = json.loads(campaign)
file_path = ((os.getenv('USERPROFILE') or os.getenv('HOME'))+"\Downloads\config_ga_cerebrosm.pdf").replace("\\", "\\\\")


class AddCampaignSuccess(unittest.TestCase):

    def setUp(self):
        global campaign
        delete_file(file_path)
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()
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
        # login
        login(self)
        sleep(2)
        # Click en clientes
        driver.find_element_by_xpath('//*[@id="inputSrc"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(client)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[5]/a[1]').click()
        sleep(1)
        # Click en view
        driver.find_element_by_xpath('//*[@id="client-camp-header"]/div/button').click()
        sleep(1)
        # llenado de Form
        # name
        driver.find_element_by_css_selector('#add-camp-name').send_keys((info[0]['name']))
        sleep(2)
        # Seleccionar Select contenedor Status
        driver.find_element_by_css_selector('#add-camp-status').click()
        sleep(3)
        # Seleccionar estatus
        aleatorio = randint(1 , 3)
        driver.find_element_by_css_selector('#add-camp-status > option:nth-child(%d)' % aleatorio).click()
        sleep(2)
        # Seleccionar Select contenedor INDUSTRY
        driver.find_element_by_css_selector('#add-camp-industry').click()
        sleep(2)
        # Seleccionar AUTOMOTRIZ
        driver.find_element_by_css_selector('#add-camp-industry > option[value="automotriz"]').click()
        sleep(2)
        # Seleccionar Select contenedor CATEGORY
        driver.find_element_by_css_selector('#add-camp-category').click()
        sleep(2)
        # Seleccionar CELULARES
        driver.find_element_by_css_selector('#add-camp-category > option[value="celulares"]').click()
        # BUGET
        driver.find_element_by_css_selector('#add-camp-budget').send_keys((info[0]['budget']))
        # URL
        driver.find_element_by_css_selector('#add-camp-url').send_keys((info[0]['url']))
        # OBJETIVE
        driver.find_element_by_css_selector('#add-camp-objetive').send_keys((info[0]['objetive']))
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[9]/div/p/a').click()
        # enter
        driver.find_element_by_xpath("//div[10]/div[1]/div[1]/div[3]/button[1]").click()
        sleep(3)
        try:
            if driver.find_element_by_xpath('//tr[1]/td[3]').get_attribute("title") == info[0]['name']:
                True
        except Exception as error:
            print(error)
            driver.find_element_by_xpath('//*[@id="client-camp-links"]/a[2]').click()
            sleep(2)
        self.assertEqual(info[0]['name'], driver.find_element_by_xpath('//tr[1]/td[3]').text, msg=None)
        self.assertEqual(float(info[0]['budget']),
                         float(driver.find_element_by_xpath('//tr[1]/td[5]').text), msg=None)
        self.assertEqual(info[0]['objetive'], driver.find_element_by_xpath('//tr[1]/td[6]').text, msg=None)
        sleep(10)
        self.assertTrue(os.path.exists(file_path), msg=None)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
