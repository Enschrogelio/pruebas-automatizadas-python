from time import sleep
import re
import json
import unittest
from util.config import ModelConfig
from util.functions import login, logout, randoms, db_functions

# Variables
client = "arcapruebas2@gmail.com"
dashboard_user = '''
    [
        {"name" : "andres", "email":"pacheco_mendez1@gmail.com", "password" : "mendez123456"},
        {"name" : "juan", "email":"pedraza_hernandez1@gmail.com", "password" : "1a23456789"}
    ]
    '''


# noinspection PyCallByClass,PyTypeChecker,PyUnresolvedReferences
class AddCampaign(unittest.TestCase):

    def dashboard_main(self):
        driver = self.driver
        login(self)
        driver.find_element_by_xpath('//*[@id="inputSrc"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(client)
        sleep(3)
        # view
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[5]/a[1]').click()
        sleep(3)
        # edit
        driver.find_element_by_xpath('//*[@id="user-dashboard"]/div/div/div[4]/a[1]').click()
        sleep(2)

    @classmethod
    def setUpClass(cls):
        info = json.loads(dashboard_user)
        code = """
info = {0}
client = "{client}"
for d_user in info:
    cur.execute("SELECT du.user_id FROM dashboard_users AS du JOIN users ON du.user_id = users.id where name = '%s' "  
                "and email = '%s'" % (d_user['name'], d_user['email']))
    try:
        id = cur.fetchone()[0]
        cur.execute("DELETE FROM dashboard_users WHERE user_id=%s" % id)
        cur.execute("DELETE FROM admin_historicaluser WHERE history_user_id = %s" % id)
        cur.execute("DELETE FROM users WHERE id = %s" % id)
    except Exception as errorException:
        errorException
cur.execute("INSERT INTO users (name, password, status, email, created_at, updated_at, is_active, is_client) VALUES "
            "('%s', '%s', 1, '%s', current_timestamp, current_timestamp, true, true) RETURNING id;" % (info[0]['name'], 
            info[0]['password'], info[0]['email']))
id = cur.fetchone()[0]

cur.execute("SELECT id FROM clients WHERE email = '%s'" % client)
id_client = cur.fetchone()[0]
cur.execute("INSERT INTO dashboard_users (client_id, user_id) VALUES (%s, %s)" % (id_client, id))
""".format(info, client=client)
        db_functions(code)
        cls.driver = ModelConfig.driver_web
        cls.dashboard_main(cls)

    def test_empty_field(self):
        driver = self.driver
        sleep(2)
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]').clear()
        driver.find_element_by_xpath('//*[@id="edit-dash-user-name"]').clear()
        driver.find_element_by_xpath('//*[@id="modal-edit-dashboard-user"]/div/div/div[3]/button').click()
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-edit-dashboard-user"]/div[1]/span')
                         .get_attribute('innerHTML'), "This field is empty", msg=None)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-edit-dashboard-user"]/div[3]/span')
                         .get_attribute('innerHTML'), "This field is empty", msg=None)
        driver.find_element_by_xpath('//*[@id="form-edit-dashboard-user"]/span/a').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="modal-change-pwd"]/div/div/div[3]/button').click()
        sleep(1)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-change"]/div[1]/span').get_attribute('innerHTML'),
                         "This field is empty", msg=None)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-change"]/div[2]/span').get_attribute('innerHTML'),
                         "This field is empty", msg=None)
        driver.find_element_by_xpath('//*[@id="modal-change-pwd"]/div/div/div[1]/button').click()

    def test_edit_min(self):
        driver = self.driver
        sleep(2)
        # email
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]').clear()
        email_format = re.compile(r'\b[\w.%+-]+@([\w.-]{1,64})+\.[a-zA-Z]{2,64}\b')
        email = "%s@%s.%s" % (randoms(3, "alpha"), randoms(4, "alpha"), randoms(1, "alpha"))
        self.assertFalse(email_format.match(email), msg=None)
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]').send_keys(email)
        driver.find_element_by_xpath('//*[@id="modal-edit-dashboard-user"]/div/div/div[3]/button').click()
        sleep(1)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-edit-dashboard-user"]/div[1]/span')
                         .get_attribute('innerHTML'), "Enter a valid email address.", msg=None)

    def test_edit_max(self):
        driver = self.driver
        sleep(2)
        # email
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]').clear()
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]').send_keys(randoms(260, "alpha"))
        self.assertEqual(len(driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]').get_attribute("value")),
                         255, msg=None)
        email_format = re.compile(r'\b[\w.%+-]+(@[\w.-]{1,64})+\.[a-zA-Z]{2,64}\b')
        # email platform
        email = "%s@%s.%s" % (randoms(3, "alpha"), randoms(65, "alpha"), randoms(2, "alpha"))
        self.assertFalse(email_format.match(email), msg=None)
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]').send_keys(email)
        driver.find_element_by_xpath('//*[@id="modal-edit-dashboard-user"]/div/div/div[3]/button').click()
        sleep(1)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-edit-dashboard-user"]/div[1]/span')
                         .get_attribute('innerHTML'), "Enter a valid mail", msg=None)
        # email extension
        email = "%s@%s.%s" % (randoms(3, "alpha"), randoms(2, "alpha"), randoms(65, "alpha"))
        self.assertFalse(email_format.match(email), msg=None)
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]').send_keys(email)
        driver.find_element_by_xpath('//*[@id="modal-edit-dashboard-user"]/div/div/div[3]/button').click()
        sleep(1)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-edit-dashboard-user"]/div[1]/span')
                         .get_attribute('innerHTML'), "Enter a valid mail", msg=None)
        driver.find_element_by_xpath('//*[@id="edit-dash-user-name"]').clear()
        driver.find_element_by_xpath('//*[@id="edit-dash-user-name"]').send_keys(randoms(260, "alpha"))
        self.assertEqual(len(driver.find_element_by_xpath('//*[@id="edit-dash-user-name"]').get_attribute("value")),
                         255, msg=None)
        # save
        driver.find_element_by_xpath('//*[@id="modal-edit-dashboard-user"]/div/div/div[3]/button').click()

    @classmethod
    def tearDownClass(cls):
        logout(cls)
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
