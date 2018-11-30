import unittest
import time
import json
from random import randint
from util.config import ModelConfig
from util.functions import db_functions, logout, login
from util.functions import screenshot


class DeletedUser(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web

    def testDeletedUsersSuccess(self):
        users = '''
        [{"email": "carlos967@gmail.com", "password": "95654131", "confirm_password":  "95654131", 
          "name": "Carlos"},  
         {"email": "ricardo647@gmail.com", "password": "11122330", "confirm_password":  "11122330", 
          "name": "Ricardo"},  
         {"email": "irma9647@gmail.com", "password": "I9454648_?¡", "confirm_password":  "I9454648_?¡", 
           "name": "Irma"}               
        ]'''

        info = json.loads(users)
        driver = self.driver

        rand=randint(0, len(info)-1) # to send the JSON logs
        code = """
        
#declaraciones de variables
        
info = {0}
rand = {1}

#recorrer el JSON

for user in info: 
    cur.execute("DELETE FROM users WHERE email = '%s'" % user['email'])  
    
#print the returned value

print(cur.rowcount)
sql = 'INSERT INTO users (name, password, status, email, created_at, updated_at, is_active, is_client)' \   
      'VALUES (%s, %s, %s, %s, current_timestamp, current_timestamp, %s) returning email'    
val = (info[rand]['name'], info[rand]['password'], '1', info[rand]['email'], 'true', 'false') 
cur.execute(sql, val)
""".format(info, rand)
        db_functions(code)

        login(self)
        time.sleep(3)

        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[1]/a').click()
        time.sleep(2)

        # Find user

        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(info[rand]['email'])
        time.sleep(5)

        # Remove user

        driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr/td[4]/a[2]/i').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="modal-delete"]/div/div/div[3]/div[2]/button').click()
        time.sleep(4)
        driver.find_element_by_css_selector('#form-confirm #input-email').send_keys(info[rand]['email'])
        time.sleep(4)
        driver.find_element_by_xpath('//*[@id="btn-submit"]').click()
        time.sleep(4)

        # Screenshot

        path = "/users/screenshot/delete/"
        screenshot(self, path)

        driver.refresh()
        time.sleep(4)

        # Find user

        driver.find_element_by_id('inputSrc').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(info[rand]['email'])
        time.sleep(5)

        # Screenshot

        screenshot(self, path)

        # Compare

        # self.assertEqual(driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[1]/td[1]')
        #                  .get_attribute('innerHTML'),info[rand]['email'], msg=None)
        # time.sleep(5)
        # self.assertEqual(driver.find_element_by_xpath('//*[@id="usertable"]/tbody/tr[1]/td[2]')
        #                  .get_attribute('innerHTML'),info[rand]['name'], msg=None)
        # time.sleep(5)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

