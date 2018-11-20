import unittest
from util.functions import *


class CampaignValiadation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = ModelConfig.driver_web
        cls.driver.maximize_window()
        cls.campaign_main(cls)

    def campaign_main(self):
        driver = self.driver
        # login
        login(self)
        sleep(2)
        # Click en clientes
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[6]/a[1]/i').click()
        sleep(1)
        # Click en view
        driver.find_element_by_xpath('//*[@id="client-camp-header"]/div/button',).click()
        sleep(1)
        # self.screenshot()
        # save
        driver.find_element_by_xpath('//*[@id="modal-add-campaign"]/div/div/div[3]/button').click()
        sleep(2)

    def test_assert_campaign(self):
        driver = self.driver
        sleep(2)
        # validación name
        validName=driver.find_element_by_xpath("//div[1]/span[@class='help-block help-block--bottom' and 1]").text
        self.assertEqual(validName, 'This field is empty')
        # validación budget
        validBudget=driver.find_element_by_xpath("//div[5]/span[@class='help-block help-block--bottom' and 1]").text
        print(validBudget, "Budget")
        self.assertEqual(validBudget, 'This field is empty.')
        # validación url
        validUrl=driver.find_element_by_xpath("//div[6]/span[@class='help-block help-block--bottom' and 1]").text
        print(validUrl, "url")
        self.assertEqual(validUrl, 'This field is empty')
        # validación url
        validUrl=driver.find_element_by_xpath("//div[6]/span[@class='help-block help-block--bottom' and 1]").text
        print(validUrl, "url")
        self.assertEqual(validUrl, 'This field is empty')
        # validación Objetive
        validObjetive=driver.find_element_by_xpath("//div[7]/span[@class='help-block help-block--bottom' and 1]").text
        print(validObjetive, "Objetive")
        self.assertEqual(validObjetive, 'This field is empty')
        sleep(2)
        # titulo
        titleModalCampaign=driver.find_element_by_xpath("//div[@class='modal fade in']/div[@class='modal-dialog box']"
                                                        "/div[@class='modal-box']/div[@class='modal-header']/h1").text
        print(titleModalCampaign, "Add Campaign")
        self.assertEqual(titleModalCampaign, 'Add Campaign')
        # placesHolder
        # name
        titleModalCampaign=driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').get_attribute\
            ("placeholder")
        print(titleModalCampaign, "name")
        self.assertEqual(titleModalCampaign, 'Name')
        # Budget
        titleModalCampaign=driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').get_attribute\
            ("placeholder")
        print(titleModalCampaign, "budget")
        self.assertEqual(titleModalCampaign, 'Budget')
        # url
        titleModalCampaign=driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').get_attribute\
            ("placeholder")
        print(titleModalCampaign, "url")
        self.assertEqual(titleModalCampaign, 'Url')
        # Objetive
        titleModalCampaign=driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').get_attribute\
            ("placeholder")
        print(titleModalCampaign, "objetive")
        self.assertEqual(titleModalCampaign, 'Objetive')

    def test_max(self):
        driver = self.driver
        # name
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').send_keys((randoms(5, "letter")))
        sleep(1)
        # BUGET
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').send_keys(randoms(5, "number"))
        # URL
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').send_keys("https://WWW."+
                                                                                        randoms(5, "number")+".com")
        # OBJETIVE
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').send_keys(randoms(5, "number"))
        # enter
        # self.screenshot()
        # driver.find_element_by_xpath("//div[10]/div[1]/div[1]/div[3]/button[1]").click()

    def test_special(self):
        driver = self.driver
        # llenado de Form
        # name
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[1]/input').send_keys(randoms(5, "special"))
        sleep(2)
        # BUGET
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').send_keys(randoms(5, "special"))
        # URL
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').send_keys("http://www.google.com")
        # OBJETIVE
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
        # BUGET
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[5]/input').send_keys(randoms(1, "number"))
        # URL
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/input').send_keys("http://www.google.com")
        # OBJETIVE
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').clear()
        driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/input').send_keys(randoms(1, "number"))
        # enter
        driver.find_element_by_xpath("//div[10]/div[1]/div[1]/div[3]/button[1]").click()
        mi_ruta="clients/campaigns/testCampaign/screenshot/"
        screenshot(self, mi_ruta)

    @classmethod
    def tearDownClass(cls):
        logout(cls)
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()