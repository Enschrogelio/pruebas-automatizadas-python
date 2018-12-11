import unittest
from time import sleep
from util.config import ModelConfig, root_files
from util.functions import db_functions, read_csv, login, logout

browser_name = None
# Specify ID client and ID campaign to run the test
client = 2
campaign = 3
creative_name = "editado3"


class UploadCsvValidation(unittest.TestCase):

    def setUp(self):
        global browser_name,campaign
        csv_list = read_csv(root_files+'creatives/creatives1OK .csv')
        code = """
csv_list = {0}
campaign = {1}
creative_name = {2}
cur.execute("DELETE FROM creatives WHERE campaign_id = %d AND name = '%s';" % (campaign,creative_name))
for creative in csv_list:
    if creative[name] == creative_name:
        cur.execute("INSERT INTO creatives (name, url, measure, type, status, created_at, updated_at, campaign_id,"
            "creative_code, file_url, redirect_url, script_snippet) VALUES "
            "('%s', '%s', '%s', '%s', %d, current_timestamp, current_timestamp, %d, '', '', '', '') RETURNING id;"
            % (creative["name"],creative["url"],creative["measure"],creative["type"],campaign))
""".format(csv_list,campaign,creative_name)
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

        assert "%s/admin/clients/" % ModelConfig.base_url in driver.current_url
        driver.find_element_by_css_selector('a[href*="/admin/client/detail/%d/"]' % client).click()
        sleep(1)

        assert "%s/admin/client/detail/" % ModelConfig.base_url in driver.current_url
        position = driver.find_element_by_xpath('//a[@href="/admin/campaign/detail/%d/"]' % campaign).\
            location_once_scrolled_into_view
        driver.execute_script("window.scrollTo(0, %d);" % (position["y"]+110))
        sleep(2)
        driver.find_element_by_xpath('//a[@href="/admin/campaign/detail/%d/"]' % campaign).click()
        sleep(2)

        assert "%s/admin/campaign/detail/" % ModelConfig.base_url in driver.current_url
        driver.find_element_by_xpath('//*[@id="dashboard-user"]/div/div[3]/button').click()
        sleep(1)

        image_path = root_files+"creatives/creatives1OK .csv"
        driver.find_element_by_xpath('//*[@id="id_file"]').send_keys(image_path)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-csv"]/div/div/div[3]/button').click()
        sleep(2)
        self.assertEqual("In row #1: Repeated\n"
                         "In row #2: NAME: This field cannot be blank.\n"
                         "URL: Enter a valid URL.\n"
                         "TYPE: Value 'OTRACOSA' is not a valid choice.\n"
                         "In row #3: URL: This field cannot be blank.\n"
                         "In row #4: NAME: This field cannot be blank.\n"
                         "In row #5: URL: Enter a valid URL.",
                         driver.find_element_by_xpath('//*[@id="form-csv"]/div/div[1]/span').get_attribute('innerText'),
                         msg=None)
        sleep(3)
        driver.find_element_by_xpath('//*[@id="modal-csv"]/div/div/div[1]/button').click()
        sleep(2)
        driver.refresh()
        sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(4)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
