import unittest
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from util.config import ModelConfig
from util.functions import login, logout, db_functions

# Variables globales
list_creatives = [
    {"name": "Compra ahorra", "status": 1, "measure": "10x10", "url": "http://www.algo.com", "type": "IMAGE"},
    {"name": "Compra gasta", "status": 0, "measure": "5x15", "url": "http://www.compraalgo.com", "type": "HTML5"},
    {"name": "Promo 1", "status": 1, "measure": "3x18", "url": "http://www.promoalgo.com", "type": "GIF"}
]
browser_name = None
client = 2
campaign = 3
creative: None


class DeleteCreativeSuccess(unittest.TestCase):

    def setUp(self):
        global browser_name, creative
        code = """
campaign = {1}
list_creatives = {0}
for creative in list_creatives:
    cur.execute("DELETE FROM creatives WHERE campaign_id = %d AND name = '%s';" % (campaign,creative["name"]))
rand = random.randint(0, len(list_creatives)-1)
cur.execute("INSERT INTO creatives (name, url, measure, type, status, created_at, updated_at, campaign_id,"
            "creative_code, file_url, redirect_url, script_snippet) VALUES "
            "('%s', '%s', '%s', '%s', %d, current_timestamp, current_timestamp, %d, '', '', '', '') RETURNING id;" 
            % (list_creatives[rand]["name"], list_creatives[rand]["url"], list_creatives[rand]["measure"],
               list_creatives[rand]["type"], list_creatives[rand]["status"], campaign))
id = cur.fetchone()[0]
cur.execute("UPDATE creatives SET creative_code = '%s-%d', "
            "redirect_url = 'https://hnz3ccup03.execute-api.us-west-2.amazonaws.com/stage/"
            "redirect?ca=PRUEBA-2&ct=CESAR-17&adUrl=http://www.arca-stage.vjdbsvf9qh.us-west-2.elasticbeanstalk.com"
            "/customer/dashboard', script_snippet = '<script id=cer-tracking src=https://d260gejhgij5g1.cloudfront.net/"
            "js/libs/cer.min.js?ca=PRUEBA-2&ct=CESAR-17></script>' "
            "WHERE ID = %d RETURNING id;"
            % (list_creatives[rand]["name"].upper(), id, id))
""".format(list_creatives, campaign)
        creative = db_functions(code)[0][0]
        self.driver = ModelConfig.driver_web
        browser_name = self.driver.capabilities['browserName']
        if browser_name == "chrome":
            self.driver.maximize_window()

    def test_detail_creative_success(self):
        driver = self.driver
        login(self)
        self.assertIn("%s/admin/clients/" % ModelConfig.base_url, driver.current_url, msg=None)
        sleep(1)
        driver.find_element_by_css_selector('a[href*="/admin/client/detail/%d/"]' % client).click()
        sleep(1)

        self.assertIn("%s/admin/client/detail/" % ModelConfig.base_url, driver.current_url, msg=None)
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
        position = driver.find_element_by_xpath('//a[@data-id="%s" and @data-target="#modal-delete"]'
                                                % creative).location_once_scrolled_into_view
        driver.execute_script("window.scrollTo(0, %d);" % (position["y"]+110))
        sleep(2)
        confirm = driver.find_element_by_xpath('//a[@data-id="%s" and @data-target="#modal-delete"]' % creative)\
            .get_property("dataset")['confirm']
        driver.find_element_by_xpath('//a[@data-id="%s" and @data-target="#modal-delete"]' % creative).click()
        sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-delete"]/div/div/div[3]/div[2]/button').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="input-email"]').send_keys(confirm)
        driver.find_element_by_xpath('//*[@id="btn-submit"]').click()
        sleep(2)
        driver.find_element_by_xpath('//a[@href="/admin/creative/detail/%s"]' % creative).click()
        sleep(2)
        self.assertIn("%s/admin/creative/detail/" % ModelConfig.base_url, driver.current_url, msg=None)
        self.assertEqual("Deleted", driver.find_element_by_xpath('//*[@id="client-info"]/div/div[7]/p')
                         .get_attribute("innerText").rstrip(), msg=None)

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
