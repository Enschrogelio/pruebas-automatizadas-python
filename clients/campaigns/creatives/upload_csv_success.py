import unittest
from time import sleep
from util.config import modelConfig, root_files
from util.functions import db_functions, read_csv, login, logout

browser_name = None
# Specify ID client and ID campaign to run the test
client = 3
campaign = 10

class upload_csv_success(unittest.TestCase):

    def setUp(self):
        global browser_name,campaign
        csv_list = read_csv(root_files+'creatives/creatives1OK  - copia.csv')
        code = """
csv_list = {0}
campaign = {1}
for creative in csv_list:
    cur.execute("DELETE FROM creatives WHERE name = '%s' AND campaign_id = %d;" % (creative["name"],campaign))
""".format(csv_list,campaign)
        db_functions(code)
        self.driver = modelConfig.driver_web
        browser_name = self.driver.capabilities['browserName']
        if browser_name == "chrome":
            self.driver.maximize_window()

    def testUploadCsv(self):
        global client, campaign
        driver = self.driver
        login(self)
        sleep(2)

        self.assertIn("%s/admin/clients/" % modelConfig.base_url, driver.current_url)
        driver.find_element_by_css_selector('a[href*="/admin/client/detail/%d/"]' % client).click()
        sleep(1)

        self.assertIn("%s/admin/client/detail/" % modelConfig.base_url, driver.current_url)
        posicion = driver.find_element_by_xpath('//a[@href="/admin/campaign/detail/%d/"]' % campaign).\
            location_once_scrolled_into_view
        driver.execute_script("window.scrollTo(0, %d);" % (posicion["y"]+110))
        sleep(2)
        driver.find_element_by_xpath('//a[@href="/admin/campaign/detail/%d/"]' % campaign).click()
        sleep(2)

        self.assertIn("%s/admin/campaign/detail/" % modelConfig.base_url, driver.current_url)
        driver.find_element_by_xpath('//*[@id="dashboard-user"]/div/div[3]/button').click()
        sleep(1)
        imagepath = root_files+"creatives/creatives1OK  - copia.csv"
        driver.find_element_by_xpath('//*[@id="id_file"]').send_keys(imagepath)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-csv"]/div/div/div[3]/button').click()
        sleep(2)
        #self.assertEqual("Record successfully added",
        #                 driver.find_element_by_xpath('//*[@id="form-csv"]/div/div[1]/span').get_attribute('innerText'),
        #                 msg=None)
        #sleep(3)
        #driver.find_element_by_xpath('//*[@id="modal-csv"]/div/div/div[1]/button').click()
        #sleep(2)
        #driver.refresh()
        sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(4)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
