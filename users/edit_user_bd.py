import unittest
import time
from selenium import webdriver
import json
from random import randint
from util.config import *
from util.functions import db_functions, logout, login
from util.functions import screenshot
from selenium.webdriver.support.ui import Select

users = '''
        [  
         {"email" : "ricardo647@gmail.com", "password" : "1112233584546?:", "confirm_password" :  "1112233584546?:", "name" : "Ricardo Mora Ortíz"},  
         {"email" : "irma9647@gmail.com", "password" : "I9454648_?¡:", "confirm_password" :  "I9454648_?¡:", "name" : "Irma González Mora"}               
        ]'''

class EditUserBd(unittest.TestCase):
    def setUp(self):
        global users
        self.driver = ModelConfig.driver_web

        # Preparación de ambiente
        info = json.loads(users)
        #rand=randint(0, len(info)-1)  #para mandar los registros del JSON
        code = """
                
info = {0}
cur.execute("DELETE FROM users WHERE email = '%s'" % info[0]['email'])
sql = 'INSERT INTO users (name, password, status, email, created_at, updated_at, is_active) VALUES (%s, %s, %s, %s, current_timestamp, current_timestamp, %s) returning email'  
val = (info[0]['name'], info[0]['password'], '1', info[0]['email'], 'true')
cur.execute(sql, val)
#imprime el valor retornado
print(cur.fetchone()[0])
""".format(info)
        db_functions(code)

    def test_edit_user_bd(self):
        global users

        info = json.loads(users)
        driver = self.driver

        # login
        login(self)
        time.sleep(3)

        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)

        # búsqueda de usuario
        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(info[0]['email'])
        time.sleep(5)

        #editar usuario
        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr/td[4]/a[1]/i').click()
        time.sleep(5)

        # editar estatus
        driver.find_element_by_css_selector('#form-edit #id_status').click()
        aleatorio=randint(0,2)
        driver.find_element_by_css_selector('#form-edit #id_status > option[value="%d"]' %aleatorio).click()
        print(driver.find_element_by_xpath('//*[@id="form-edit"]/span').get_attribute('innerHTML'))

        assert "Raw passwords are not stored, so there is no way to see this user's password, but you can change the password using this" in driver.find_element_by_xpath('//*[@id="form-edit"]/span').get_attribute('innerHTML')
        time.sleep(3)
        driver.find_element_by_css_selector('#form-edit > span > a').click()
        time.sleep(3)
        driver.find_element_by_css_selector('#form-change #id_password1').clear()
        driver.find_element_by_css_selector('#form-change #id_password1').send_keys(info[0]["password"])
        time.sleep(3)
        driver.find_element_by_css_selector('#form-change #id_password2').clear()
        driver.find_element_by_css_selector('#form-change #id_password2').send_keys(info[0]["password"])
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="modal-change-pwd"]/div/div/div[3]/button').click()

        assert "Record successfully updated" not in driver.page_source
        time.sleep(3)

        # realizar lo del screenshot
        mi_ruta="/users/screenshot/editar/"
        screenshot(self, mi_ruta)
        time.sleep(2)

        # búsqueda de usuario
        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(info[0]['email'])
        time.sleep(5)

        #driver.find_element_by_xpath('//*[@id="modal-edit"]/div/div/div[3]/button').click()

    def tearDown(self):
        logout(self)
        self.driver.close()

if __name__== "__main__":
    unittest.main()