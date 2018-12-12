import json
import unittest
from util.functions import *
from util.config import *

dashboard_succes = '''
    [
        {"name" : "andres", "email":"pacheco_mendez1@gmail.com", "password" : "mendez123456"}    
    ]
    '''


class AddCampaign(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web

    def testuserempty(self):
        driver = self.driver
        info = json.loads(dashboard_succes)
        code = """
info = {0}
cur.execute("DELETE FROM public.dashboard_users WHERE user_id=(select dashboard_users.user_id from dashboard_users join "
            "users on dashboard_users.user_id = users.id where name='%s' and email='%s') ;"  
            %(info[0]['name'], info[0]['email']))
print(cur.rowcount)
cur.execute("DELETE FROM public.admin_historicaluser WHERE history_user_id=(select users.id from "
            "admin_historicaluser join users on admin_historicaluser.history_user_id = users.id where users.name='%s'"
            " and users.email='%s');"  
            %(info[0]['name'], info[0]['email']))
print(cur.rowcount)
cur.execute("DELETE FROM users WHERE name='%s' and email='%s';" %(info[0]['name'], info[0]['email']))            
print(cur.rowcount)
""".format(info)
        db_functions(code)
        login(self)

        # view
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[4]/td[6]/a[1]/i').click()
        sleep(3)
        # button_dashboard
        driver.find_element_by_xpath('//*[@id="btn-add-"]').click()
        sleep(3)
        # email
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]')\
            .send_keys((info[0]["email"]))
        # name
        driver.find_element_by_xpath('//*[@id="add-dash-user-name"]')\
            .send_keys((info[0]["name"]))
        sleep(3)
        # password
        driver.find_element_by_xpath('//*[@id="add-dash-user-password1"]')\
            .send_keys((info[0]["password"]))
        # confirmation de password
        driver.find_element_by_xpath('//*[@id="add-dash-user-password2"]')\
            .send_keys((info[0]["password"]))
        # save
        driver.find_element_by_xpath('//*[@id="modal-add-dashboard-user"]/div/div/div[3]/button').click()
        sleep(3)
        # asser
        self.assertEqual(info[0]["name"], driver.find_element_by_xpath('//*[@id="user-dashboard"]/div/div/div[2]')
                         .text, msg=None)
        self.assertEqual(info[0]["email"], driver.find_element_by_xpath('//*[@id="user-dashboard"]/div/div/div[1]')
                         .text, msg=None)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

