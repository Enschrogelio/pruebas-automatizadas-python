import datetime
import unittest
import time

from selenium import webdriver
from util.config import *
from util.functions import *


class CampaignValiadation(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = ModelConfig.driverWeb
        self.driver.maximize_window()

    def test_campaign_validation(self):
        driver = self.driver
    #login
        login(self)
        time.sleep(2)
        #Click en clientes
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[6]/a[1]/i').click()
        time.sleep(1)
    #Click en view
        driver.find_element_by_xpath('//*[@id="client-camp-header"]/div/button',).click()
        time.sleep(1)
        #self.screenshot()
        #save
        driver.find_element_by_xpath('//*[@id="modal-add-campaign"]/div/div/div[3]/button').click()
        time.sleep(2)


    def test_assert_campaign(self):
        driver = self.driver
        time.sleep(2)

        #validación name
        validName=driver.find_element_by_xpath("//div[1]/span[@class='help-block help-block--bottom' and 1]").text
        print(validName,"name")
        self.assertEqual(validName,'This field is empty')

        #validación budget
        validBudget=driver.find_element_by_xpath("//div[5]/span[@class='help-block help-block--bottom' and 1]").text
        print(validBudget,"budget")
        self.assertEqual(validBudget,'This field is empty.')

        #validación url
        validUrl=driver.find_element_by_xpath("//div[6]/span[@class='help-block help-block--bottom' and 1]").text
        print(validUrl,"url")
        self.assertEqual(validUrl,'This field is empty')

        #validación url
        validUrl=driver.find_element_by_xpath("//div[6]/span[@class='help-block help-block--bottom' and 1]").text
        print(validUrl,"url")
        self.assertEqual(validUrl,'This field is empty')

        #validación Objetive
        validObjetive=driver.find_element_by_xpath("//div[7]/span[@class='help-block help-block--bottom' and 1]").text
        print(validObjetive,"Objetive")
        self.assertEqual(validObjetive,'This field is empty')
        time.sleep(2)

        #titulo
        titleModalCampaign=driver.find_element_by_xpath("//div[@class='modal fade in']/div[@class='modal-dialog box']/div[@class='modal-box']/div[@class='modal-header']/h1").text
        print(titleModalCampaign,"Add Campaign")
        self.assertEqual(titleModalCampaign,'Add Campaign')

        #placesHolder
        #name
        titleModalCampaign=driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').get_attribute("placeholder")
        print(titleModalCampaign,"name")
        self.assertEqual(titleModalCampaign,'Name')
        #Budget
        titleModalCampaign=driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').get_attribute("placeholder")
        print(titleModalCampaign,"budget")
        self.assertEqual(titleModalCampaign,'Budget')
        #url
        titleModalCampaign=driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').get_attribute("placeholder")
        print(titleModalCampaign,"url")
        self.assertEqual(titleModalCampaign,'Url')
        #Objetive
        titleModalCampaign=driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').get_attribute("placeholder")
        print(titleModalCampaign,"objetive")
        self.assertEqual(titleModalCampaign,'Objetive')


    def test_max(self):
        driver = self.driver
        #name
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').clear(randoms(5,"letter"))
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').send_keys()
        time.sleep(1)
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
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').send_keys(randoms(5,"number"))
        #URL
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').send_keys("https://WWW."+randoms(5,"number")+".com")
        #OBJETIVE
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').send_keys(randoms(5,"number"))
        #enter
        #self.screenshot()
        driver.find_element_by_xpath("//div[10]/div[1]/div[1]/div[3]/button[1]").click()

    def test_special(self):
        driver = self.driver
        #llenado de Form
        #name
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').send_keys(randoms(5,"special"))
        time.sleep(1)
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
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').send_keys(randoms(5,"special"))
        #URL
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').send_keys("http://www.google.com")
        #OBJETIVE
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').send_keys(randoms(5,"special"))
        #enter
        driver.find_element_by_xpath("//div[10]/div[1]/div[1]/div[3]/button[1]").click()
        time.sleep(2)
        #self.screenshot()

    def test_min(self):
        driver = self.driver
        #llenado de Form
        #name
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').send_keys(randoms(1,"letter"))
        time.sleep(1)
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
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').send_keys(randoms(1,"number"))
        #URL
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').send_keys("http://www.google.com")
        #OBJETIVE
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').send_keys(randoms(1,"number"))
        #enter
        driver.find_element_by_xpath("//div[10]/div[1]/div[1]/div[3]/button[1]").click()
        mi_ruta="clients/campaigns/testCampaign/screenshot/"
        screenshot(self,mi_ruta)
        logout(self)



if __name__ == "__main__":
    unittest.main()