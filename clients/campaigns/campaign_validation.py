import unittest
from time import sleep

from util.config import ModelConfig
from util.functions import login, randoms, logout

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
        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[5]/a[1]/i').click()
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
        driver.find_element_by_css_selector("#add-camp-name").clear()
        driver.find_element_by_css_selector("#add-camp-budget").clear()
        driver.find_element_by_css_selector("#add-camp-url").clear()
        driver.find_element_by_css_selector("#add-camp-objetive").clear()
        # validación name
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[2]/span')
                         .get_attribute('innerHTML'), 'This field is empty', msg=None)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/span')
                         .get_attribute('innerHTML'), 'This field is empty', msg=None)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/span')
                         .get_attribute('innerHTML'), 'This field is empty', msg=None)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[8]/span')
                         .get_attribute('innerHTML'), 'This field is empty', msg=None)
        sleep(2)
        self.assertEqual(driver.find_element_by_xpath("//div[@class='modal fade in']/div/div/div/h1")
                         .get_attribute('innerHTML'), 'Add Campaign', msg=None)
        # placesHolder
        self.assertEqual(driver.find_element_by_css_selector("#add-camp-name").get_attribute("placeholder"), 
                         'Name', msg=None)
        self.assertEqual(driver.find_element_by_css_selector("#add-camp-budget").get_attribute("placeholder"), 
                         'Budget', msg=None)
        self.assertEqual(driver.find_element_by_css_selector("#add-camp-url").get_attribute("placeholder"), 
                         'Url', msg=None)
        self.assertEqual(driver.find_element_by_css_selector("#add-camp-objetive").get_attribute("placeholder"), 
                         'Objetive', msg=None)

    def test_min(self):
        driver = self.driver
        sleep(2)
        # name
        driver.find_element_by_css_selector('#add-camp-name').clear()
        driver.find_element_by_css_selector('#add-camp-name').send_keys(randoms(1, "letter"))
        # budget
        driver.find_element_by_css_selector('#add-camp-budget').clear()
        driver.find_element_by_css_selector('#add-camp-budget').send_keys(randoms(1, "number"))
        # url
        driver.find_element_by_css_selector('#add-camp-url').clear()
        driver.find_element_by_css_selector('#add-camp-url').send_keys("https://.com")
        # objeive
        driver.find_element_by_css_selector('#add-camp-objetive').clear()
        driver.find_element_by_css_selector('#add-camp-objetive').send_keys(randoms(1, "number"))
        # click Save
        driver.find_element_by_xpath('//div[10]/div[1]/div[1]/div[3]/button[1]').click()
        sleep(1)
        self.assertEqual('Enter a valid URL.', driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[7]/span')
                         .get_attribute('innerHTML'))

    def test_max(self):
        driver = self.driver
        sleep(2)
        # name
        driver.find_element_by_css_selector('#add-camp-name').clear()
        driver.find_element_by_css_selector('#add-camp-name').send_keys(randoms(250, "letter"))
        # Máximo 99999999999999999.99
        driver.find_element_by_css_selector('#add-camp-budget').clear()
        driver.find_element_by_css_selector('#add-camp-budget').send_keys(randoms(18, 'number'))
        driver.find_element_by_css_selector('#add-camp-url').clear()
        driver.find_element_by_css_selector('#add-camp-url').send_keys("https://%s" % randoms(501, "letter")+".com")
        driver.find_element_by_css_selector('#add-camp-objetive').clear()
        driver.find_element_by_css_selector('#add-camp-objetive').send_keys('21474836488')
        driver.find_element_by_xpath('//div[10]/div[1]/div[1]/div[3]/button[1]').click()
        sleep(2)
        # asserts
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/span')
                         .get_attribute('innerHTML'), "Enter a valid budget. Maximum allowed decimals: 2", msg=None)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[8]/span')
                         .get_attribute('innerHTML'), "Please input a value between 0-2147483647.", msg=None)
        self.assertEqual(len(driver.find_element_by_css_selector('#add-camp-name').get_attribute("value")),
                         250, msg=None)
        self.assertEqual(len(driver.find_element_by_css_selector('#add-camp-url').get_attribute("value")),
                         500, msg=None)

    def test_special(self):
        driver = self.driver
        sleep(4)
        # name
        driver.find_element_by_css_selector('#add-camp-name').clear()
        driver.find_element_by_css_selector('#add-camp-name').send_keys(randoms(100, "special"))
        # budget
        driver.find_element_by_css_selector('#add-camp-budget').clear()
        driver.find_element_by_css_selector('#add-camp-budget').send_keys(randoms(100, "special"))
        # url
        driver.find_element_by_css_selector('#add-camp-url').clear()
        driver.find_element_by_css_selector('#add-camp-url').send_keys("https://%s" %
                                                                       randoms(10, "special")+".com")
        # objetive
        driver.find_element_by_css_selector('#add-camp-objetive').clear()
        driver.find_element_by_css_selector('#add-camp-objetive').send_keys(randoms(100, "special"))
        # click Save
        driver.find_element_by_xpath('//div[10]/div[1]/div[1]/div[3]/button[1]').click()
        sleep(2)
        # asserts Budget
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[6]/span')
                         .get_attribute('innerHTML'), "Enter a valid budget. Maximum allowed decimals: 2", msg=None)
        # asserts objetive
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-add-campaign"]/div[8]/span')
                         .get_attribute('innerHTML'), "This field is empty", msg=None)


    # noinspection PyUnresolvedReferences
    @classmethod
    def tearDownClass(cls):
        logout(cls)
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
