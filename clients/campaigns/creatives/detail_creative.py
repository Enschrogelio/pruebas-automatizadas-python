import os
import unittest
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from util.config import ModelConfig
import random
from util.functions import login, logout, db_functions, delete_file

# Variables globales
list_creatives = [
    {"name": "Compra ahorra", "status": 1, "measure": "10x10", "url": "http://www.algo.com", "type": "IMAGE"},
    {"name": "Compra gasta", "status": 0, "measure": "5x15", "url": "http://www.compraalgo.com", "type": "HTML5"},
    {"name": "Promo 1", "status": 1, "measure": "3x18", "url": "http://www.promoalgo.com", "type": "GIF"},
    {"name": "Promo pollo", "status": 0, "measure": "30x15", "url": "http://www.cerebro.com", "type": "VIDEO"}
]
browser_name = None
client = 4
campaign = 39
creative: None
rand = random.randint(0, len(list_creatives)-1)
file: None
if list_creatives[rand]["type"] == "IMAGE":
    file = "png.png"
elif list_creatives[rand]["type"] == "GIF":
    file = "gif.gif"
elif list_creatives[rand]["type"] == "HTML5":
    file = "gif.gif"
elif list_creatives[rand]["type"] == "VIDEO":
    file = "video.mp4"
file_path = ((os.getenv('USERPROFILE') or os.getenv('HOME'))+"\Downloads\%s" % file).replace("\\", "\\\\")


class DetailCreativeSuccess(unittest.TestCase):

    def setUp(self):
        global browser_name, creative

        delete_file(file_path)
        code = """
campaign = {1}
list_creatives = {0}
for creative in list_creatives:
    cur.execute("DELETE FROM creatives WHERE campaign_id = %d AND name = '%s';" % (campaign,creative["name"]))
rand = {2}
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
            % (list_creatives[rand]["name"].upper().replace(" ", "_"), id, id))
""".format(list_creatives, campaign, rand)
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
        position = driver.find_element_by_xpath('//a[@href="/admin/creative/detail/%s"]'
                                                % creative).location_once_scrolled_into_view
        driver.execute_script("window.scrollTo(0, %d);" % (position["y"]+110))
        sleep(2)
        driver.find_element_by_xpath('//a[@href="/admin/creative/detail/%s"]' % creative).click()
        sleep(2)

        self.assertIn("%s/admin/creative/detail/" % ModelConfig.base_url, driver.current_url, msg=None)
        sleep(1)
        self.assertEqual(str(creative), driver.find_element_by_xpath('//*[@id="client-info"]/div/div[1]/p')
                         .get_attribute("innerText").rstrip(), msg=None)
        self.assertEqual(str(campaign), driver.find_element_by_xpath('//*[@id="client-info"]/div/div[2]/p')
                         .get_attribute("innerText").rstrip(), msg=None)
        self.assertEqual(list_creatives[rand]["name"].upper().replace(" ", "_")+"-"+str(creative),
                         driver.find_element_by_xpath('//*[@id="client-info"]/div/div[3]/p')
                         .get_attribute("innerText").rstrip(), msg=None)
        self.assertEqual(list_creatives[rand]["name"],
                         driver.find_element_by_xpath('//*[@id="client-info"]/div/div[4]/p')
                         .get_attribute("innerText").rstrip(), msg=None)
        self.assertEqual(list_creatives[rand]["measure"],
                         driver.find_element_by_xpath('//*[@id="client-info"]/div/div[5]/p')
                         .get_attribute("innerText").rstrip(), msg=None)
        self.assertEqual(list_creatives[rand]["type"],
                         driver.find_element_by_xpath('//*[@id="client-info"]/div/div[6]/p')
                         .get_attribute("innerText").rstrip(), msg=None)
        status: None
        if list_creatives[rand]["status"] == 0:
            status = "Inactive"
        elif list_creatives[rand]["status"] == 1:
            status = "Active"
        elif list_creatives[rand]["status"] == 2:
            status = "Deleted"
        self.assertEqual(status, driver.find_element_by_xpath('//*[@id="client-info"]/div/div[7]/p')
                         .get_attribute("innerText").rstrip(), msg=None)
        preview = driver.find_element_by_xpath('//*[@id="client-info"]/div/div[8]/p').get_attribute("innerText").\
            rstrip()
        if preview == "Preview":
            # driver.find_element_by_link_text("Preview").click()
            driver.find_element_by_xpath('/html/body/div[1]/div/div[8]/p/a').click()
            sleep(6)
            self.assertTrue(os.path.exists(file_path), msg=None)
        else:
            print("No hay archivo para descargar")
        sleep(3)
        print("aquí")
        driver.find_element_by_xpath('//*[@id="btn-edit"]').click()
        sleep(3)
        self.assertEqual("http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/campaign/detail/%d/"
                         "creative/update/%s" % (campaign, creative), driver.current_url, msg=None)
        driver.find_element_by_xpath('//*[@id="modal-edit-creative"]/div/div/div[1]/button').click()

    def tearDown(self):
        logout(self)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
