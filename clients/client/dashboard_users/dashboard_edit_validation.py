from time import sleep
import json
import unittest
from util.config import ModelConfig
from util.functions import login, logout, randoms

# Variables
client = "arcapruebas2@gmail.com"
dashboard_user = '''
    [
        {"name" : "andres", "email":"pacheco_mendez1@gmail.com", "password" : "mendez123456"},
        {"name" : "juan", "email":"pedraza_hernandez1@gmail.com", "password" : "mendez123456"},
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
        sleep(1)
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
cur.execute("SELECT du.user_id FROM dashboard_users AS du JOIN users ON du.user_id = users.id where name = '%s' "  
            "and email = '%s'" % (info[0]['name'], info[0]['email']))
try:
    id = cur.fetchone()[0]
    cur.execute("DELETE FROM dashboard_users WHERE user_id=%s" % id)
    cur.execute("DELETE FROM admin_historicaluser WHERE history_user_id = %s" % id)
    cur.execute("DELETE FROM users WHERE id = %s" % id)
except Exception as errorException:
    errorException

""".format(info)
        db_functions(code)
        cls.driver = ModelConfig.driver_web
        cls.dashboard_main(cls)

    def test_edit_min(self):
        driver = self.driver
        sleep(2)
        # email
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]').clear()
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]') \
            .send_keys(randoms(10, "alpha"))
        # name
        driver.find_element_by_xpath('//*[@id="edit-dash-user-name"]').clear()
        driver.find_element_by_xpath('//*[@id="edit-dash-user-name"]')\
            .send_keys(randoms(10, "alpha"))
        # active
        driver.find_element_by_xpath('//*[@id="edit-dash-user-status"]').click()
        # save
        driver.find_element_by_xpath('//*[@id="modal-edit-dashboard-user"]/div/div/div[3]/button').click()

    def test_edit_max(self):
        driver = self.driver
        # email
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]').clear()
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]') \
            .send_keys(randoms(100, "alpha"))
        # name
        driver.find_element_by_xpath('//*[@id="edit-dash-user-name"]').clear()
        driver.find_element_by_xpath('//*[@id="edit-dash-user-name"]') \
            .send_keys(randoms(100, "alpha"))
        # active
        driver.find_element_by_xpath('//*[@id="edit-dash-user-status"]').click()
        # save
        driver.find_element_by_xpath('//*[@id="modal-edit-dashboard-user"]/div/div/div[3]/button').click()

    def test_edit_special(self):
        driver = self.driver
        # email
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]').clear()
        driver.find_element_by_xpath('//*[@id="edit-dash-user-email"]') \
            .send_keys(randoms(100, "special"))
        sleep(3)
        # name
        driver.find_element_by_xpath('//*[@id="edit-dash-user-name"]').clear()
        driver.find_element_by_xpath('//*[@id="edit-dash-user-name"]') \
            .send_keys(randoms(100, "special"))
        # active
        driver.find_element_by_xpath('//*[@id="edit-dash-user-status"]').click()
        # save
        driver.find_element_by_xpath('//*[@id="modal-edit-dashboard-user"]/div/div/div[3]/button').click()

    @classmethod
    def tearDownClass(cls):
        logout(cls)
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
