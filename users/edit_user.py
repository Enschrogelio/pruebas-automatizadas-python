import unittest
import time
from selenium import webdriver
import json
from random import randint
from cerebro.util.config import *
from cerebro.util.login import Login

class edituser(unittest.TestCase):
    def setUp(self):
        self.driver = modelConfig.driverWeb

    def testEditUsersSuccess(self):
        users = '''
        [{"email" : "Pedro64@gmail.com", "password" : "Pedro987654", "confirm_password" :  "Pedro987654", "name" : "Pedro Cruz Ortíz"},  
         {"email" : "Juan4678@gmail.com", "password" : "Juan63547878?¡:", "confirm_password" :  "Juan63547878?¡:", "name" : "Juan Gómez Gómez"},  
         {"email" : "Javier36@gmail.com", "password" : "Javier65465987987:", "confirm_password" :  "Javier65465987987:", "name" : "Javier Aguirre Aguirre"}               
        ]'''

        info = json.loads(users)
        rand=randint(0, len(info)-1)  #para mandar los registros del JSON

        driver = self.driver
        Login.testlogin(self)

        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)

        # editar usuarios

        for j in range(0,3):
            print (j)
            if j==0:
                driver.find_element_by_xpath('//*[@id="usertable_paginate"]/ul/li[2]/a').click()
                # Ver si se encuentra el registro desplegado en la pantalla, actúa como una validación
                bandera =0
                x=3

            #while bandera ==0:
                try:
                    print (x)
                    if driver.find_element_by_xpath('//a[@href="/admin/user/update/13/"]'):
                        bandera=1
                except (Exception):
                        bandera=0
                        driver.find_element_by_xpath('//*[@id="usertable_paginate"]/ul/li[%d]/a'%x).click()
                        x = x+1
                time.sleep(3)
                driver.find_element_by_xpath('//a[@href="/admin/user/update/13/"]').click()
                time.sleep(1)
                driver.find_element_by_css_selector('#form-edit #id_email').clear()
                driver.find_element_by_css_selector('#form-edit #id_email').send_keys("Jorge3987@gmail.com")
                driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
                time.sleep(2)

            else:
                if j==1:
                    driver.find_element_by_xpath('//*[@id="usertable_paginate"]/ul/li[2]/a').click()
                    time.sleep(1)
                    bandera =0
                    m=3
                #while bandera ==0:
                    try:
                        print (m)
                        if driver.find_element_by_xpath('//a[@href="/admin/user/update/14/"]'):
                            bandera=1
                    except (Exception):
                            bandera=0
                            driver.find_element_by_xpath('//*[@id="usertable_paginate"]/ul/li[%d]/a'%m).click()
                            m = m+1
                    time.sleep(3)
                    driver.find_element_by_xpath('//a[@href="/admin/user/update/14/"]').click()
                    time.sleep(1)
                    driver.find_element_by_css_selector('#form-edit #id_name').clear()
                    driver.find_element_by_css_selector('#form-edit #id_name').send_keys("Javier Ortíz Cruz")
                    driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
                    time.sleep(2)

                if j==2:
                    driver.find_element_by_xpath('//*[@id="usertable_paginate"]/ul/li[2]/a').click()
                    time.sleep(1)
                    bandera =0
                    i=3

                    #while bandera ==0:
                    try:
                        print(i)
                        if driver.find_element_by_xpath('//a[@href="/admin/user/update/6/"]/i'):
                            bandera=2
                    except (Exception):
                            bandera=0
                            driver.find_element_by_xpath('//*[@id="usertable_paginate"]/ul/li[%d]/a'%i).click()
                            i = i+1
                    time.sleep(3)
                    driver.find_element_by_xpath('//a[@href="/admin/user/update/6/"]/i').click()
                    time.sleep(1)
                    driver.find_element_by_css_selector('#form-edit #id_status').click()
                    aleatorio=randint(0,2)
                    driver.find_element_by_css_selector('#form-edit #id_status > option[value="%d"]' %aleatorio).click()
                    print(driver.find_element_by_xpath('//*[@id="form-edit"]/span').get_attribute('innerHTML'))

                    assert "Raw passwords are not stored, so there is no way to see this user's password, but you can change the password using this" in driver.find_element_by_xpath('//*[@id="form-edit"]/span').get_attribute('innerHTML')
                    time.sleep(3)
                    driver.find_element_by_css_selector('#form-edit > span > a').click()
                    time.sleep(3)

                    driver.find_element_by_css_selector('#form-change #id_password1').clear()
                    driver.find_element_by_css_selector('#form-change #id_password1').send_keys("Jany123456?")
                    time.sleep(3)
                    driver.find_element_by_css_selector('#form-change #id_password2').clear()
                    driver.find_element_by_css_selector('#form-change #id_password2').send_keys("Jany123456?")
                    time.sleep(3)
                    driver.find_element_by_xpath('//*[@id="modal-change-pwd"]/div/div/div[3]/button').click()

                    assert "Record successfully updated" not in driver.page_source
                    time.sleep(3)
                    #driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()

    def tearDown(self):
        self.driver.close()

if __name__== "__main__":
    unittest.main()
