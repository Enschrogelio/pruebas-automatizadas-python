import json
import unittest
from time import sleep

from util.config import ModelConfig
from util.functions import db_functions, login, logout

# Variables
client = "arcapruebas2@gmail.com"
dashboard_success = '''
    [
        {"name" : "andres", "email":"pacheco_mendez1@gmail.com", "password" : "mendez123456"}    
    ]
    '''


class AddCampaign(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web

    def testuserempty(self):
        driver = self.driver
        info = json.loads(dashboard_success)
        code = """
info = {0}
cur.execute("SELECT du.user_id FROM dashboard_users AS du JOIN users ON du.user_id = users.id where name = '%s' "  
            "and email = '%s'" % (info[0]['name'], info[0]['email']))
try:
    id = cur.fetchone()[0]
    cur.execute("DELETE FROM users u USING dashboard_users du JOIN users u ON u.id = user_id JOIN 
                "admin_historicaluser hu ON history_user_id=u.id WHERE duser_id = u.id AND u.id = history_user_id AND "
                "u.id = %s" % id)
    # cur.execute("DELETE FROM admin_historicaluser WHERE history_user_id = %s" % id)
    # cur.execute("DELETE FROM users WHERE id = %s" % id)
except Exception as errorException:
    errorException
""".format(info)
        db_functions(code)
        login(self)
        driver.find_element_by_xpath('//*[@id="inputSrc"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(client)
        sleep(1)
        # view
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[5]/a[1]').click()
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

