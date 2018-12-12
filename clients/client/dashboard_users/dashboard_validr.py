import json
import time
import unittest

import self

from util.config import ModelConfig
from util.functions import login, logout, db_functions, randoms

dashboard_edit_succes_ful = '''
    [   
        {"name" : "andresss", "email":"andres@pacheco.com", "password" : "p802zsdr45"},
        {"name" : "andres pacheco1", "email":"andres1@mendez.com", "password" : "mario1234A"}    
    ]
    '''


class AddCampaign(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = ModelConfig.driver_web
        info = json.loads(dashboard_edit_succes_ful)

        code = """
    info = {0}
    cur.execute("DELETE FROM public.dashboard_users WHERE user_id=(select dashboard_users.user_id from dashboard_users " \
                "join users on dashboard_users.user_id = users.id where " \
                "name='%s' and email='%s') ;"  %(info[1]['name'], 
                info[1]['email']))
    sql = 'INSERT INTO dashboard_users (email, name, password, created_at, updated_at) ' \
          'VALUES (%s, %s, %s, %s, %s)'
    val = (info[0]['email'], info[0]['name'], info[0]['password'], strftime("%Y/%m/%d"), strftime("%Y/%m/%d"))
    cur.execute(sql, val)
    
        """.format(info)
        db_functions(code)
        cls.dasboard_main(cls)

    def dasboard_main(self):
        driver = self.driver
        login(self)
        # view
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[4]/td[6]/a[1]/i').click()
        time.sleep(3)
        # edit
        driver.find_element_by_xpath('//*[@id="btn-add-"]').click()
        time.sleep(1)

    def testdasboard_main(self):
        driver = self.driver
        info = json.loads(dashboard_edit_succes_ful)
    # email
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]') \
            .send_keys((info[1]["email"]))
        # name
        driver.find_element_by_xpath('//*[@id="add-dash-user-name"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-name"]') \
            .send_keys((info[1]["name"]))
        # password
        driver.find_element_by_xpath('//*[@id="add-dash-user-password1"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-password1"]') \
            .send_keys((info[1]["password"]))
        # password confirmacion
        driver.find_element_by_xpath('//*[@id="add-dash-user-password2"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-password2"]') \
            .send_keys((info[1]["password"]))
        # save
        driver.find_element_by_xpath('//*[@id="modal-add-dashboard-user"]/div/div/div[3]/button').click()
        time.sleep(2)


    def testEdit_min(self):
        driver = self.driver
        # email
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]')\
            .send_keys(randoms(1, "alpa"))
        # name
        driver.find_element_by_xpath('//*[@id="add-dash-user-name"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-name"]')\
            .send_keys(randoms(1, "alpha"))
        # password
        driver.find_element_by_xpath('//*[@id="add-dash-user-password1"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-password1"]')\
            .send_keys(randoms(1, "alpha"))
        # password confirmacion
        driver.find_element_by_xpath('//*[@id="add-dash-user-password2"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-password2"]')\
            .send_keys(randoms(1, "alpha"))
        # save
        driver.find_element_by_xpath('//*[@id="modal-add-dashboard-user"]/div/div/div[3]/button').click()

    def testEdit_max(self):
        driver = self.driver
        # email
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]') \
            .send_keys(randoms(100, "alpha"))
        # name
        driver.find_element_by_xpath('//*[@id="add-dash-user-name"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-name"]') \
            .send_keys(randoms(100, "alpha"))
        # password
        driver.find_element_by_xpath('//*[@id="add-dash-user-password1"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-password1"]') \
            .send_keys(randoms(100, "alpha"))
        # password confirmacion
        driver.find_element_by_xpath('//*[@id="add-dash-user-password2"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-password2"]') \
            .send_keys(randoms(100, "alpha"))
        # save
        driver.find_element_by_xpath('//*[@id="modal-add-dashboard-user"]/div/div/div[3]/button').click()

    def testEdit_special(self):
        driver = self.driver
        # email
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]')\
            .send_keys(randoms(10, "special"))
        # name
        driver.find_element_by_xpath('//*[@id="add-dash-user-name"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-name"]')\
            .send_keys(randoms(10, "special"))
        # password
        driver.find_element_by_xpath('//*[@id="add-dash-user-password1"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-password1"]')\
            .send_keys(randoms(10, "special"))
        # password confirmacion
        driver.find_element_by_xpath('//*[@id="add-dash-user-password2"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-password2"]')\
            .send_keys(randoms(10, "special"))
        # save
        driver.find_element_by_xpath('//*[@id="modal-add-dashboard-user"]/div/div/div[3]/button').click()

    @classmethod
    def tearDownClass(cls):
        logout(cls)
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
