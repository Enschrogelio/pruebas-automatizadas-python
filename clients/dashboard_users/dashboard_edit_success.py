import json
import unittest
from time import sleep
from util.functions import db_functions, login, logout
from util.config import ModelConfig

# Variables
client = "arcapruebas2@gmail.com"
dashboard_success = '''
    [
        {"name" : "andres", "email" : "pacheco_mendez1@gmail.com", "password" : "mendez123456", "status": 1},
        {"name" : "juan", "email" : "pedraza_hernandez1@gmail.com", "password" : "1a23456789", "status": 2}
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
client = "{1}"
for d_user in info:
    cur.execute("SELECT du.user_id FROM dashboard_users AS du JOIN users ON du.user_id = users.id WHERE "  
                "email = '%s'" % (d_user['email']))
    try:
        id = cur.fetchone()[0]
        cur.execute("DELETE FROM dashboard_users WHERE user_id=%s" % id)
        cur.execute("DELETE FROM admin_historicaluser WHERE history_user_id = %s" % id)
        cur.execute("DELETE FROM users WHERE id = %s" % id)
    except Exception as errorException:
        errorException
cur.execute("INSERT INTO users (name, password, status, email, created_at, updated_at, is_active, is_client) VALUES "
            "('%s', '%s', 1, '%s', current_timestamp, current_timestamp, true, true) RETURNING id;" % (info[1]['name'], 
            info[1]['password'], info[1]['email']))
id = cur.fetchone()[0]

cur.execute("SELECT id FROM clients WHERE email = '%s'" % client)
id_client = cur.fetchone()[0]
cur.execute("INSERT INTO dashboard_users (client_id, user_id) VALUES (%s, %s)" % (id_client, id))
""".format(info, client)
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
        driver.find_element_by_xpath('//*[@id="user-dashboard"]/div/div/div[4]/a[1]').click()
        sleep(3)
        # email
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]').clear()
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]').send_keys((info[0]["email"]))
        # name
        driver.find_element_by_xpath('//*[@id="edit-dash-user-name"]').clear()
        driver.find_element_by_xpath('//*[@id="edit-dash-user-name"]').send_keys((info[0]["name"]))
        sleep(3)
        # password
        driver.find_element_by_xpath('//*[@id="edit-dash-user-status"]').click()
        driver.find_element_by_xpath('//*[@id="edit-dash-user-status"]').send_keys((info[0]["status"]))
        # confirmation de password
        # save
        driver.find_element_by_xpath('//*[@id="modal-edit-dashboard-user"]/div/div/div[3]/button').click()
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

