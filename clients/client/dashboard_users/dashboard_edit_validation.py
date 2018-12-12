import time
import unittest
from util.config import ModelConfig
from util.functions import login, logout, randoms


# noinspection PyTypeChecker
class AddCampaign(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = ModelConfig.driver_web
        cls.dashboar_main(cls)

    def dashboar_main(self):
        driver = self.driver
        login(self)
        # view
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[4]/td[6]/a[1]/i').click()
        time.sleep(3)
        # edit
        driver.find_element_by_xpath('//*[@id="user-dashboard"]/div/div/div[4]/a[1]/i').click()
        time.sleep(2)

    def testEdit_min(self):
        driver = self.driver
        time.sleep(2)
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
        time.sleep(3)
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
