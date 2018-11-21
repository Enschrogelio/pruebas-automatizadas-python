import json
import unittest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from util.functions import *
from util.config import *
from util.functions import login

campaign = '''
    [{"name" : "Coca-cola company", "budget":"2.00", "url":"https://www.google.com", "objetive":"2"},
    {"name" : "Rogelio 2", "budget":"5.0", "url":"https://www.facebook.com/", "objetive":"4.0"}]'''


class AddCampaignSuccess(unittest.TestCase):

    def setUp(self):
        global campaign
        self.driver = ModelConfig.driver_web
        self.driver.maximize_window()
        info = json.loads(campaign)
        code = """
info = {0}
cur.execute("DELETE FROM campaigns WHERE name = '%s' AND budget = '%s' AND objetive = '%s'" %(info[0]['name'], 
            info[0]['budget'], info[0]['objetive']))
    """.format(info)
        db_functions(code)
        # print("DELETE FROM campaigns WHERE name = '%s' AND budget = '%s' AND objetive = '%s' AND url =
        # '%s'%("+info[0]['name']+", "+info[0]['budget']+", "+info[0]['url']+", "+info[0]['objetive']+")")

    def test_campaign(self):
            global campaign
            driver = self.driver
            info = json.loads(campaign)
            # login
            login(self)
            sleep(2)
            # Click en clientes
            driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[6]/a[1]/i').click()
            sleep(1)
            # Click en view
            driver.find_element_by_xpath('//*[@id="client-camp-header"]/div/button').click()
            sleep(1)
            # llenado de Form
            # name
            driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').send_keys((info[0]['name']))

    def tearDown(self):
            logout(self)
            self.driver.close()


if __name__ == "__main__":
    unittest.main()