import unittest
import time
from selenium import webdriver
import json
from random import randint
from util.config import *
from util.functions import db_functions, logout, login
from util.functions import screenshot

class DeletedUser(unittest.TestCase):
    def setUp(self):
        self.driver = ModelConfig.driver_web

    def testDeletedUsersSuccess(self):
        users = '''
        [{"email" : "carlos967@gmail.com", "password" : "956541313187", "confirm_password" :  "956541313187", "name" : "Carlos González Acuña"},  
         {"email" : "ricardo647@gmail.com", "password" : "1112233584546?:", "confirm_password" :  "1112233584546?:", "name" : "Ricardo Mora Ortíz"},  
         {"email" : "irma9647@gmail.com", "password" : "I9454648_?¡:", "confirm_password" :  "I9454648_?¡:", "name" : "Irma González Mora"}               
        ]'''

        info = json.loads(users)
        rand=randint(0, len(info)-1)  #para mandar los registros del JSON
        code = """
        
#declaraciones de variables        
info = {0}
rand = {1}

#recorrer el JSON
for user in info: 
    cur.execute("DELETE FROM users WHERE email = '%s'" % user['email'])  
#imprime el valor retornado
print(cur.rowcount)
sql = 'INSERT INTO users (name, password, status, email, created_at, updated_at, is_active) VALUES (%s, %s, %s, %s, current_timestamp, current_timestamp, %s) returning email'  
val = (info[rand]['name'], info[rand]['password'], '1', info[rand]['email'], 'true')
cur.execute(sql, val)
""".format(info, rand)
        db_functions(code)

        driver = self.driver
        login(self)

        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)

        # búsqueda de usuario
        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(info[rand]['email'])
        time.sleep(5)

        # eliminar usuario
        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr/td[4]/a[2]/i').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="modal-delete"]/div/div/div[3]/div[2]/button').click()
        time.sleep(4)
        driver.find_element_by_css_selector('#form-confirm #input-email').send_keys(info[rand]['email'])
        time.sleep(4)
        #assert "Deleting record" not in driver.page_source
        driver.find_element_by_xpath('//*[@id="btn-submit"]').click()
        time.sleep(4)

        # realizar lo delscreenshot
        mi_ruta="/users/screenshot/eliminar/"
        screenshot(self, mi_ruta)

        driver.refresh()
        time.sleep(4)

        # búsqueda de usuario
        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(info[rand]['email'])
        time.sleep(5)

        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr/td[4]/a[2]/i').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="modal-delete"]/div/div/div[3]/div[1]/button').click()
        time.sleep(4)

        # screenshot
        screenshot(self, mi_ruta)

    def tearDown(self):
        self.driver.close()

if __name__== "__main__":
    unittest.main()
