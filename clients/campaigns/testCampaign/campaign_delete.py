import datetime
import json
import unittest
import time
from tkinter.tix import Select
from util.functions import *

from selenium import webdriver
from self import self

from util.functions import *
from util.config import *
from util.dataCampaign import *
import psycopg2 as psycopg2

campaign=[
    {"name" : "Rogelio","budget":"2","url":"https://www.google.es/","objetive":"2"},
    {"name" : "Rogelio 2","budget":"4","url":"https://www.facebook.com/","objetive":"4"}]

global campaign


class AddClient(unittest.TestCase):
    def setUp(self):
        self.driver = modelConfig.driverWeb
        info = json.loads(campaign)
        self.driver.maximize_window()
        code = """
info={0}
cur.execute("DELETE FROM campaigns WHERE id = '%'" info[1]['id'])
sql = 'INSERT INTO campaigns (name, budget,url,objetive) VALUES (%s, %s, %s, %s)'
val = (info[0]['name'],info[0]['budget'],info[0]['url',info[0]['objetive'])
cur.execute(sql,val)
""".format(info)
        db_functions(code)

    def testAddClient(self):
        driver = self.driver
        info = json.loads(campaign)
    #login
        login(self)
        time.sleep(2)
        #Click en clientes
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[6]/a[1]/i').click()
        time.sleep(1)
        #Click en view
        driver.find_element_by_xpath('//*[@id="client-camp-header"]/div/button').click()
        time.sleep(1)
        #llenado de Form
        #name
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').send_keys(dataCampign.name)
        time.sleep(2)
        #Seleccionar Select contenedor ACTIVE
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[2]').click()
        time.sleep(2)
        #Seleccionar Active
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[2]/select/option[1]').click()
        time.sleep(2)
        #Seleccionar Select contenedor INDUSTRIA
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[3]').click()
        time.sleep(2)
        #Seleccionar AUTOMOTRIZ
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[3]/select/option[6]').click()
        time.sleep(2)
        #Seleccionar Select contenedor CATEGORY
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[4]').click()
        time.sleep(2)
        #Seleccionar CELULARES
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[4]/select/option[6]').click()
        #BUGET
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').send_keys(dataCampign.budget)
        #URL
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').send_keys(dataCampign.url)
        #OBJETIVE
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').send_keys(dataCampign.objetive)
        #enter
        driver.find_element_by_xpath("//div[10]/div[1]/div[1]/div[3]/button[1]").click()




    # def screenshot(self):
    #     driver = self.driver
    #     now = datetime.datetime.now()
    #     hour = now.hour
    #     min = now.min
    #     second = now.second
    #     today = datetime.date.today()
    #     driver.save_screenshot(modelConfig.screen+"testCampaign/screenshot/empty%s-hora-%s-seg_%s.png" %(today,hour,second))

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()