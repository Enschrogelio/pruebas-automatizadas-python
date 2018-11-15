import unittest
import time
from selenium import webdriver
import json
from random import randint
from util.config import *
from util.functions import db_functions, logout, login
from util.functions import screenshot

class AddUserBd(unittest.TestCase):
    def setUp(self):
        self.driver = ModelConfig.driver_web

    def testAddUsersSuccess(self):
        users = '''
        [{"email" : "fernanda222@gmail.com", "password" : "223344556677:", "confirm_password" : "223344556677:", "name" : "Fernanda Sánchez González"},
         {"email" : "cesar444@gmail.com", "password" : "46546554:", "confirm_password" : "46546554:", "name" : "César López Aguirre"},
         {"email" : "anita78@gmail.com", "password" : "97744552121?", "confirm_password" : "97744552121?", "name" : "Anita Becerra de la O"}
        ]'''

        info = json.loads(users)
        rand=randint(0, len(info)-1) #para mandar los registros del JSON
        code = """
        
info = {0}
#recorrer el JSON
for user in info: 
    cur.execute("DELETE FROM users WHERE email = '%s'" % user['email']) 
#imprime el valor retornado
print(cur.rowcount)
""".format(info)
        db_functions(code)

        driver = self.driver
        login(self)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)

        # agregar usuarios
        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="id_email"]').send_keys(info[rand]['email'])
        driver.find_element_by_xpath('//*[@id="id_password1"]').send_keys(info[rand]['password'])
        driver.find_element_by_xpath('//*[@id="id_password2"]').send_keys(info[rand]['confirm_password'])
        driver.find_element_by_xpath('//*[@id="id_name"]').send_keys(info[rand]['name'])

        # realizar lo del screenshot
        mi_ruta="/users/screenshot/agregar/"
        screenshot(self, mi_ruta)

        driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/button').click()
        time.sleep(2)

        # screenshot
        screenshot(self, mi_ruta)
        driver.refresh()

        # leer mensajes del modal
        assert "Record successfully added" not in driver.page_source
        time.sleep(3)

    def tearDown(self):
        logout(self)
        self.driver.close()

if __name__== "__main__":
    unittest.main()
