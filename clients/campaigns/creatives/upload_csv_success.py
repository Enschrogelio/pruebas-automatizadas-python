import unittest
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from util.config import ModelConfig, root_files
from util.functions import db_functions, read_csv, login, logout

browser_name = None
# Specify ID client and ID campaign to run the test
client = 2
campaign = 3


class UploadCsvSuccess(unittest.TestCase):

    def setUp(self):
        global browser_name,campaign
        csv_list = read_csv(root_files+'creatives/creativesSuccess.csv')
        code = """
csv_list = {0}
campaign = {1}
for creative in csv_list:
    cur.execute("DELETE FROM creatives WHERE name = '%s' AND campaign_id = %d;" % (creative["name"],campaign))
""".format(csv_list,campaign)
        db_functions(code)
        self.driver = ModelConfig.driver_web
        browser_name = self.driver.capabilities['browserName']
        if browser_name == "chrome":
            self.driver.maximize_window()

    def testUploadCsv(self):
        global client, campaign
        driver = self.driver
        login(self)
        sleep(2)

        self.assertIn("%s/admin/clients/" % ModelConfig.base_url, driver.current_url)
        driver.find_element_by_css_selector('a[href*="/admin/client/detail/%d/"]' % client).click()
        sleep(1)

        self.assertIn("%s/admin/client/detail/" % ModelConfig.base_url, driver.current_url)
        band = 0
        while band == 0:
            try:
                if driver.find_element_by_xpath('//a[@href="/admin/campaign/detail/%d/"]' % campaign):
                    band = 1
                    if browser_name == "internet explorer":
                        print(browser_name)
                    if browser_name == "chrome" or browser_name == "firefox" or browser_name == "edge":
                        position = driver.find_element_by_xpath('//a[@href="/admin/campaign/detail/%d/"]' % campaign) \
                            .location_once_scrolled_into_view
                        driver.execute_script("window.scrollTo(0, %d);" % (position["y"]+110))
                        sleep(2)
            except NoSuchElementException:
                if browser_name == "chrome" or browser_name == "firefox" or browser_name == "edge":
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(2)
                driver.find_element_by_css_selector("#campaigntable_paginate > ul > li.next > a").click()
                sleep(2)
                band = 0
        driver.find_element_by_xpath('//a[@href="/admin/campaign/detail/%d/"]' % campaign).click()
        sleep(2)

        self.assertIn("%s/admin/campaign/detail/" % ModelConfig.base_url, driver.current_url, msg=None)
        driver.find_element_by_xpath('//*[@id="dashboard-user"]/div/div[3]/button').click()
        sleep(1)
        image_path = root_files+"creatives/Success.csv"
        driver.find_element_by_xpath('//*[@id="id_file"]').send_keys(image_path)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-csv"]/div/div/div[3]/button').click()
        sleep(2)
        # self.assertEqual("Record successfully added",
        #                  driver.find_element_by_xpath('//*[@id="form-csv"]/div/div[1]/span').get_attribute('innerText'),
        #                  msg=None)
        # sleep(3)
        # driver.find_element_by_xpath('//*[@id="modal-csv"]/div/div/div[1]/button').click()
        # sleep(2)
        # driver.refresh()
        sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(4)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
