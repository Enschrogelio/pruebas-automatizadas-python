import json
from time import sleep
import re
import unittest
from util.config import ModelConfig
from util.functions import login, logout, db_functions, randoms

dashboard_user = '''
    [   
        {"name" : "andresss", "email":"andres@pacheco.com", "password" : "p802zsdr45"},
        {"name" : "andres pacheco1", "email":"andres1@mendez.com", "password" : "mario1234A"}    
    ]
    '''
client = "arcapruebas2@gmail.com"


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
        # add
        driver.find_element_by_xpath('//*[@id="btn-add-"]').click()
        sleep(1)

    # noinspection PyCallByClass,PyTypeChecker
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
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-name"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-password1"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-password2"]').clear()
        driver.find_element_by_xpath('//*[@id="modal-add-dashboard-user"]/div/div/div[3]/button').click()
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-dashboard-user"]/div[2]/span')
                         .get_attribute('innerHTML'), "This field is empty", msg=None)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-dashboard-user"]/div[3]/span')
                         .get_attribute('innerHTML'), "This field is empty", msg=None)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-dashboard-user"]/div[4]/span')
                         .get_attribute('innerHTML'), "This field is empty", msg=None)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-dashboard-user"]/div[5]/span')
                         .get_attribute('innerHTML'), "This field is empty", msg=None)
    
    def test_add_min(self):
        driver = self.driver
        sleep(2)
        # email
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]').clear()
        email_format = re.compile(r'\b[\w.%+-]+@([\w.-]{1,64})+\.[a-zA-Z]{2,64}\b')
        email = "%s@%s.%s" % (randoms(3, "alpha"), randoms(4, "alpha"), randoms(1, "alpha"))
        self.assertFalse(email_format.match(email), msg=None)
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]').send_keys(email)
        driver.find_element_by_xpath('//*[@id="modal-add-dashboard-user"]/div/div/div[3]/button').click()
        sleep(1)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-dashboard-user"]/div[2]/span')
                         .get_attribute('innerHTML'), "Enter a valid email address.", msg=None)
    
    def test_add_max(self):
        driver = self.driver
        sleep(2)
        # email
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]').send_keys(randoms(260, "alpha"))
        self.assertEqual(len(driver.find_element_by_xpath('//*[@id="add-dash-user-email"]').get_attribute("value")),
                         255, msg=None)
        email_format = re.compile(r'\b[\w.%+-]+(@[\w.-]{1,64})+\.[a-zA-Z]{2,64}\b')
        # email platform
        email = "%s@%s.%s" % (randoms(3, "alpha"), randoms(65, "alpha"), randoms(2, "alpha"))
        self.assertFalse(email_format.match(email), msg=None)
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]').send_keys(email)
        driver.find_element_by_xpath('//*[@id="modal-add-dashboard-user"]/div/div/div[3]/button').click()
        sleep(1)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-dashboard-user"]/div[2]/span')
                         .get_attribute('innerHTML'), "Enter a valid mail", msg=None)
        # email extension
        email = "%s@%s.%s" % (randoms(3, "alpha"), randoms(2, "alpha"), randoms(65, "alpha"))
        self.assertFalse(email_format.match(email), msg=None)
        driver.find_element_by_xpath('//*[@id="add-dash-user-email"]').send_keys(email)
        driver.find_element_by_xpath('//*[@id="modal-add-dashboard-user"]/div/div/div[3]/button').click()
        sleep(1)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-dashboard-user"]/div[2]/span')
                         .get_attribute('innerHTML'), "Enter a valid mail", msg=None)
        driver.find_element_by_xpath('//*[@id="add-dash-user-name"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-name"]').send_keys(randoms(260, "alpha"))
        self.assertEqual(len(driver.find_element_by_xpath('//*[@id="add-dash-user-name"]').get_attribute("value")),
                         255, msg=None)
        driver.find_element_by_xpath('//*[@id="add-dash-user-password1"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-password1"]').send_keys(randoms(260, "alpha"))
        self.assertEqual(len(driver.find_element_by_xpath('//*[@id="add-dash-user-name"]').get_attribute("value")),
                         255, msg=None)
        driver.find_element_by_xpath('//*[@id="add-dash-user-password2"]').clear()
        driver.find_element_by_xpath('//*[@id="add-dash-user-password2"]').send_keys(randoms(260, "alpha"))
        self.assertEqual(len(driver.find_element_by_xpath('//*[@id="add-dash-user-name"]').get_attribute("value")),
                         255, msg=None)
        # save
        driver.find_element_by_xpath('//*[@id="modal-add-dashboard-user"]/div/div/div[3]/button').click()

    # noinspection PyUnresolvedReferences
    @classmethod
    def tearDownClass(cls):
        logout(cls)
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
