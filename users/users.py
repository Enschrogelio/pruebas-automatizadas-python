import unittest
import time
from selenium import webdriver
import json
from random import randint

class adduser(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('C:/Users/janet/Desktop/chromedriver.exe')

    def testAddUsersSuccess(self):
        users = '''
        [{"email" : "Pedro64@gmail.com", "password" : "Pedro987654", "confirm_password" :  "Pedro987654", "name" : "Pedro Cruz Ortíz"},  
         {"email" : "Juan4678@gmail.com", "password" : "Juan63547878?¡:", "confirm_password" :  "Juan63547878?¡:", "name" : "Juan Gómez Gómez"},  
         {"email" : "Javier36@gmail.com", "password" : "Javier65465987987:", "confirm_password" :  "Javier65465987987:", "name" : "Javier Aguirre Aguirre"}               
        ]'''

        info = json.loads(users)
        rand=randint(0, len(info)-1)  #para mandar los registros del JSON

        driver = self.driver
        driver.get("http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/login/")
        driver.find_element_by_xpath('//*[@id="id_username"]').send_keys("admin@admin.com")
        driver.find_element_by_xpath('//*[@id="id_password"]').send_keys("admin")
        driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()
        # assert "http://aismartads.com/admin/users/" in driver.current_url
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)

        #agregar usuarios

        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="id_email"]').send_keys(info[rand]['email'])
        driver.find_element_by_xpath('//*[@id="id_password1"]').send_keys(info[rand]['password'])
        driver.find_element_by_xpath('//*[@id="id_password2"]').send_keys(info[rand]['confirm_password'])
        driver.find_element_by_xpath('//*[@id="id_name"]').send_keys(info[rand]['name'])
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        time.sleep(2)
        # assert info[rand]['email'] in driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[1]').text

        driver.refresh()

        #leer mensajes del modal

        assert "Record successfully added" not in driver.page_source
        # assert "texto" in driver.page_source

        #Errores de validación

        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="id_email"]').clear()
        driver.find_element_by_xpath('//*[@id="id_password1"]').clear()
        driver.find_element_by_xpath('//*[@id="id_password2"]').clear()
        driver.find_element_by_xpath('//*[@id="id_name"]').clear()
        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        assert "This field is empty" in driver.find_element_by_xpath('//*[@id="form-add"]/div[1]/span').get_attribute('innerText')
        assert "This field is empty" in driver.find_element_by_xpath('//*[@id="form-add"]/div[2]/span').get_attribute('innerText')
        assert "This field is empty" in driver.find_element_by_xpath('//*[@id="form-add"]/div[3]/span').get_attribute('innerText')
        assert "This field is empty" in driver.find_element_by_xpath('//*[@id="form-add"]/div[4]/span').get_attribute('innerText')
        time.sleep(5)

        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[1]/button').click()
        time.sleep(3)

        # editar usuarios

        for j in range(0,3):
            print (j)
            if j==0:
                driver.find_element_by_xpath('//*[@id="usertable_paginate"]/ul/li[2]/a').click()
            # Ver si se encuentra el registro desplegado en la pantalla, actúa como una validación
                try:
                    if(driver.find_element_by_xpath('//a[@href="/admin/user/update/13/"]').is_displayed()):
                        bandera=0

                except (Exception):
                    driver.find_element_by_xpath('//*[@id="usertable_paginate"]/ul/li[3]/a').click()
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
                    try:
                        if(driver.find_element_by_xpath('//a[@href="/admin/user/update/14/"]').is_displayed()):
                            bandera=0
                    except (Exception):
                        driver.find_element_by_xpath('//*[@id="usertable_paginate"]/ul/li[3]/a').click()
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
                    try:
                        if(driver.find_element_by_xpath('//a[@href="/admin/user/update/6/"]/i').is_displayed()):
                            bandera=2
                    except (Exception):
                        driver.find_element_by_xpath('//*[@id="usertable_paginate"]/ul/li[3]/a').click()
                    time.sleep(3)
                    driver.find_element_by_xpath('//a[@href="/admin/user/update/6/"]/i').click()
                    time.sleep(1)
                    driver.find_element_by_css_selector('#form-edit #id_status').click()
                    aleatorio=randint(0,2)
                    driver.find_element_by_css_selector('#form-edit #id_status > option[value="%d"]' %aleatorio).click()
                    driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()
                    time.sleep(3)
                    print(driver.find_element_by_xpath('//*[@id="form-edit"]/span').get_attribute('innerHTML'))

                    # búsqueda de usuario
                    driver.find_element_by_id('inputSrc').click()
                    time.sleep(2)
                    driver.find_element_by_xpath('//*[@id="search"]').send_keys("Javier36@gmail.com")
                    time.sleep(5)

                    #eliminar usuario

                    driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr/td[4]/a[2]/i').click()
                    time.sleep(5)
                    driver.find_element_by_xpath('//*[@id="modal-delete"]/div/div/div[3]/div[2]/button').click()
                    time.sleep(4)
                    driver.find_element_by_css_selector('#form-confirm #input-email').send_keys("Javier36@gmail.com")
                    time.sleep(4)
                    driver.find_element_by_xpath('//*[@id="btn-submit"]').click()
                    time.sleep(4)
                    #assert "Deleting record" not in driver.page_source
                    driver.refresh()

    def tearDown(self):
        self.driver.close()

if __name__== "__main__":
    unittest.main()





















