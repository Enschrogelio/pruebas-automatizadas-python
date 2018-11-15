import unittest
from time import sleep
from util.config import ModelConfig
from util.functions import login, logout

# Variables globales
browser_name = None

class DetailCreativeSuccess(unittest.TestCase):

    def setUp(self):
        global browser_name
        self.driver = ModelConfig.driver_web
        browser_name = self.driver.capabilities['browserName']
        if browser_name == "chrome":
            self.driver.maximize_window()

    def test_detail_creative_success(self):
        driver = self.driver
        login(self)
        self.assertIn("%s/admin/clients/" % ModelConfig.base_url, driver.current_url, msg=None)
        sleep(1)
        # driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[2]/td[6]/a[1]/i').click()
        driver.find_element_by_css_selector('a[href*="/admin/client/detail/2/"]').click()
        sleep(1)

        self.assertIn("%s/admin/client/detail/" % ModelConfig.base_url, driver.current_url, msg=None)

        if browser_name == "internet explorer":
            print(browser_name)
        if browser_name == "chrome" or browser_name == "firefox" or browser_name == "edge":
            position=driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr[3]/td[10]/a[1]/i')\
                .location_once_scrolled_into_view
            driver.execute_script("window.scrollTo(0, %d);" %(position["y"]+110))

        sleep(2)
        driver.find_element_by_xpath('//*[@id="campaigntable"]/tbody/tr[3]/td[10]/a[1]/i').click()
        sleep(2)

        self.assertIn("%s/admin/campaign/detail/" % ModelConfig.base_url, driver.current_url,msg=None)
        position=driver.find_element_by_xpath('//*[@id="user-dashboard"]/div[1]/div/div[4]/a[1]')\
            .location_once_scrolled_into_view
        driver.execute_script("window.scrollTo(0, %d);" %(position["y"]+110))
        sleep(2)
        driver.find_element_by_xpath('//*[@id="user-dashboard"]/div[1]/div/div[4]/a[1]').click()
        sleep(2)

        self.assertIn("%s/admin/creative/detail/" % ModelConfig.base_url, driver.current_url, msg=None)
        idCreativo=driver.find_element_by_xpath('//*[@id="client-info"]/div/div[1]/p').get_attribute("innerText") \
            .rstrip()
        sleep(1)
        preview = driver.find_element_by_xpath('//*[@id="client-info"]/div/div[8]/p').get_attribute("innerText") \
            .rstrip()
        if (preview == "Preview"):
            # driver.find_element_by_link_text("Preview").click()
            driver.find_element_by_xpath('/html/body/div[1]/div/div[8]/p/a').click()
            sleep(6)
        else:
            print("No hay archivo para descargar")
        sleep(1)
        driver.find_element_by_xpath('//*[@id="btn-edit"]').click()
        sleep(3)
        self.assertEqual("http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/campaign/detail/2/"
                         "creative/update/%s" %idCreativo, driver.current_url,msg=None)
        driver.find_element_by_xpath('//*[@id="modal-edit-creative"]/div/div/div[1]/button').click()
        # position=driver.find_element_by_xpath('//a[@href="/admin/creative/detail/%s"]' %idCreativo)\
        #     .location_once_scrolled_into_view
        # driver.execute_script("window.scrollTo(0, %d);" %(position["y"]+110))
        # sleep(2)
        # driver.find_element_by_xpath('//a[@href="/admin/creative/detail/%s"]' %idCreativo).click()

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
