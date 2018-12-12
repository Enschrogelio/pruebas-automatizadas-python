import time
import unittest

from util.config import ModelConfig
from util.functions import login, logout


class AddCampaign(unittest.TestCase):

    def setUp(self):
        self.driver = ModelConfig.driver_web

    def testdashboard_remove_succelful(self):
        driver = self.driver
        login(self)
        # view
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[4]/td[6]/a[1]/i').click()
        time.sleep(3)
        # delete
        driver.find_element_by_xpath('//*[@id="user-dashboard"]/div/div/div[4]/a[2]/i').click()
        time.sleep(4)
        # delete
        driver.find_element_by_xpath('//*[@id="modal-delete"]/div/div/div[3]/div[2]').click()
        time.sleep(2)
        # Enter the confirmation
        driver.find_element_by_xpath('//*[@id="input-email"]').send_keys("andres")
        time.sleep(3)
        # button
        driver.find_element_by_xpath('//*[@id="btn-submit"]').click()
        time.sleep(3)

        def tearDown(self):
            logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()