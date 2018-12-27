import unittest
from time import sleep
from util.config import ModelConfig
from util.functions import login, randoms, screenshot, logout

client = "arcapruebas2@gmail.com"


class CampaignValidation(unittest.TestCase):

    def campaign_main(self):
        driver = self.driver
        # login
        login(self)
        sleep(2)
        # Click en clientes
        driver.find_element_by_xpath('//*[@id="inputSrc"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="search"]').send_keys(client)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[6]/a[1]/i').click()
        sleep(1)
        # Click en view
        driver.find_element_by_xpath('//*[@id="client-camp-header"]/div/button').click()
        sleep(1)
        # self.screenshot()
        # save
        driver.find_element_by_xpath('//*[@id="modal-add-campaign"]/div/div/div[3]/button').click()
        sleep(2)

    # noinspection PyCallByClass,PyTypeChecker
    @classmethod
    def setUpClass(cls):
        cls.driver = ModelConfig.driver_web
        cls.driver.maximize_window()
        cls.campaign_main(cls)

    def test_assert_campaign(self):
        driver = self.driver
        sleep(2)
        # validación name
        self.assertEqual(driver.find_element_by_xpath("//div[1]/span[1]").text, 'This field is empty')
        # validación budget
        self.assertEqual(driver.find_element_by_xpath("//div[5]/span[1]").text, 'This field is empty.', msg=None)
        # validación url
        self.assertEqual(driver.find_element_by_xpath("//div[6]/span[1]").text, 'This field is empty', msg=None)
        # validación url
        self.assertEqual(driver.find_element_by_xpath("//div[6]/span[1]").text, 'This field is empty', msg=None)
        # validación Objetivo
        self.assertEqual(driver.find_element_by_xpath("//div[7]/span[1]").text, 'This field is empty', msg=None)
        sleep(2)
        self.assertEqual(driver.find_element_by_xpath("//div[@class='modal fade in']/div/div/div/h1").text,
                         'Add Campaign', msg=None)
        # placesHolder
        # name
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input')
                         .get_attribute("placeholder"), 'Name', msg=None)
        # Budget
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input')
                         .get_attribute("placeholder"), 'Budget')
        # url
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input')
                         .get_attribute("placeholder"), 'Url')
        # Objetive
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input')
                         .get_attribute("placeholder"), 'Objective')

    def test_max(self):
        driver = self.driver
        # name
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').send_keys((randoms(256, "letter")))
        sleep(1)
        # BUGET
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').send_keys(randoms(256, "number"))
        # URL
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input')\
            .send_keys("https://WWW.%s" % randoms(256, "number")+".com")
        # OBJECTIVE
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').send_keys(randoms(256, "number"))

    def test_special(self):
        driver = self.driver
        # llenado de Form
        # name
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').send_keys(randoms(5, "special"))
        sleep(2)
        # BUDGET
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').send_keys(randoms(5, "special"))
        # URL
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').send_keys("http://www.google.com")
        # OBJECTIVE
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').send_keys(randoms(5, "special"))
        # enter
        driver.find_element_by_xpath("//div[10]/div[1]/div[1]/div[3]/button[1]").click()
        sleep(2)
        #  self.screenshot()

    def test_min(self):
        driver = self.driver
        # llenado de Form
        # name
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').send_keys(randoms(1, "letter"))
        sleep(1)
        # BUDGET
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').send_keys(randoms(1, "number"))
        # URL
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').send_keys("http://www.google.com")
        # OBJECTIVE
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').send_keys(randoms(1, "number"))
        # enter
        driver.find_element_by_xpath("//div[10]/div[1]/div[1]/div[3]/button[1]").click()
        path = "clients/campaigns/testCampaign/screenshot/"
        screenshot(self, path)

    # noinspection PyUnresolvedReferences
    @classmethod
    def tearDownClass(cls):
        logout(cls)
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
