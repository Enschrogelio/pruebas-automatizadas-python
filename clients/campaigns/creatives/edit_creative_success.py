import random
import unittest
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from util.config import ModelConfig, root_files
from util.functions import login, logout, db_functions

# Variables globales
types = [
    {"type": "IMAGE", "file": root_files+"creatives\png.png"},
    {"type": "GIF", "file": root_files+"creatives\gif.gif"},
    {"type": "VIDEO", "file": root_files+r"creatives\video.mp4"},
    {"type": "HTML5", "file": root_files+"creatives\html5.html"}
]
list_creatives = [
    {"name": "Compra ahorra", "status": 1, "measure": "10x10", "url": "http://www.algo.com", "type": "IMAGE"},
    {"name": "Compra gasta", "status": 0, "measure": "5x15", "url": "http://www.compraalgo.com", "type": "HTML5"},
    {"name": "Promo 1", "status": 1, "measure": "3x18", "url": "http://www.promoalgo.com", "type": "GIF"}
]
browser_name = None
client = 4
campaign = 39
rand = random.randint(0, len(list_creatives)-1)
creative: None


class EditCreativeSuccessful(unittest.TestCase):

    def setUp(self):
        global browser_name, creative
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

    def test_edit_creative_success(self):
        global types, client, campaign, creative, rand_creative, position_file
        driver = self.driver
        login(self)
        self.assertIn("%s/admin/clients/" % ModelConfig.base_url, driver.current_url, msg=None)
        sleep(1)
        driver.find_element_by_css_selector('a[href*="/admin/client/detail/%d/"]' % client).click()
        sleep(1)

        self.assertIn("%s/admin/client/detail/" % ModelConfig.base_url, driver.current_url, msg=None)
        sleep(2)
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
        for position_file in range(4):
            rand_creative = random.randint(0, len(list_creatives)-1)
            print("\n<<<------ %s ------>>>\n" % types[position_file]["type"])
            position = driver.find_element_by_xpath('//a[@href="/admin/campaign/detail/%d/creative/update/%s"]'
                                                    % (campaign, creative)).location_once_scrolled_into_view
            driver.execute_script("window.scrollTo(0, %d);" % (position["y"]+110))
            sleep(2)
            driver.find_element_by_xpath('//a[@href="/admin/campaign/detail/%d/creative/update/%d"]'
                                         % (campaign, creative)).click()
            sleep(2)
            self.assertIn("%s/admin/campaign/detail/%d/creative/update/%d"
                          % (ModelConfig.base_url, campaign, creative), driver.current_url, msg=None)
            sleep(2)
            driver.find_element_by_css_selector('#form-edit-creative #edit-creative-name').clear()
            driver.find_element_by_css_selector('#form-edit-creative #edit-creative-name')\
                .send_keys(list_creatives[rand_creative]["name"])
            driver.find_element_by_css_selector('#form-edit-creative #edit-creative-status').click()
            sleep(1)
            driver.find_element_by_css_selector('#form-edit-creative #edit-creative-status > option[value="%d"]'
                                                % list_creatives[rand_creative]["status"]).click()
            sleep(1)
            driver.find_element_by_css_selector('#form-edit-creative #edit-creative-measure').clear()
            driver.find_element_by_css_selector('#form-edit-creative #edit-creative-measure')\
                .send_keys(list_creatives[rand_creative]["measure"])
            driver.find_element_by_css_selector('#form-edit-creative #edit-creative-url').clear()
            driver.find_element_by_css_selector('#form-edit-creative #edit-creative-url')\
                .send_keys(list_creatives[rand_creative]["url"])
            driver.find_element_by_css_selector('#form-edit-creative #edit-creative-type').click()
            sleep(1)
            driver.find_element_by_css_selector('#form-edit-creative #edit-creative-type > option[value="%s"]'
                                                % types[position_file]["type"]).click()
            sleep(1)
            driver.find_element_by_css_selector('#form-edit-creative #edit-creative-type').click()
            sleep(1)
            driver.find_element_by_xpath('/html/body/div[13]/div/div/div[2]/form/div[6]/div[2]/p/a').click()
            sleep(5)
            driver.switch_to_window(driver.window_handles[0])
            sleep(2)
            if browser_name == "chrome" or browser_name == "firefox" or browser_name == "edge":
                position = driver.find_element_by_xpath('/html/body/div[13]/div/div/div[3]/button') \
                    .location_once_scrolled_into_view
                driver.execute_script("window.scrollTo(0, %d);" % (position["y"]))
            # for i in range(0,10):
            #     sleep(1)
            #     driver.find_element_by_css_selector('html').send_keys(Keys.ARROW_DOWN)
            sleep(2)
            image_path = types[position_file]["file"]
            driver.find_element_by_css_selector('#form-edit-creative #id_file').send_keys(image_path)
            sleep(2)
            driver.find_element_by_xpath('//*[@id="modal-edit-creative"]/div/div/div[3]/button').click()
            sleep(3)
            try:
                while driver.find_element_by_css_selector('# form-edit-creative div div.loader-input-file.center span'):
                    print("Cargando %s ..." % types[position_file]["type"])
                    sleep(2)
            except NoSuchElementException:
                print("Archivo %s cargado" % types[position_file]["type"])

        position = driver.find_element_by_xpath('//a[@href="/admin/creative/detail/%s"]' % creative)\
            .location_once_scrolled_into_view
        driver.execute_script("window.scrollTo(0, %d);" % (position["y"]+110))
        sleep(2)
        driver.find_element_by_xpath('//a[@href="/admin/creative/detail/%s"]' % creative).click()
        sleep(2)

        self.assertEqual(str(creative), driver.find_element_by_xpath('//*[@id="client-info"]/div/div[1]/p').
                         get_attribute("innerText").rstrip(), msg=None)
        self.assertEqual(str(campaign), driver.find_element_by_xpath('//*[@id="client-info"]/div/div[2]/p').
                         get_attribute("innerText").rstrip(), msg=None)
        self.assertEqual(list_creatives[rand]["name"].upper().replace(" ", "_")+"-"+str(creative),
                         driver.find_element_by_xpath('//*[@id="client-info"]/div/div[3]/p').
                         get_attribute("innerText").rstrip(), msg=None)
        self.assertEqual(list_creatives[rand_creative]["name"],
                         driver.find_element_by_xpath('//*[@id="client-info"]/div/div[4]/p').
                         get_attribute("innerText").rstrip(), msg=None)
        self.assertEqual(list_creatives[rand_creative]["measure"],
                         driver.find_element_by_xpath('//*[@id="client-info"]/div/div[5]/p').
                         get_attribute("innerText").rstrip(), msg=None)
        self.assertEqual(types[position_file]["type"],
                         driver.find_element_by_xpath('//*[@id="client-info"]/div/div[6]/p').
                         get_attribute("innerText").rstrip(), msg=None)
        status: None
        if list_creatives[rand_creative]["status"] == 0:
            status = "Inactive"
        elif list_creatives[rand_creative]["status"] == 1:
            status = "Active"
        elif list_creatives[rand_creative]["status"] == 2:
            status = "Deleted"
        self.assertEqual(status, driver.find_element_by_xpath('//*[@id="client-info"]/div/div[7]/p').
                         get_attribute("innerText").rstrip(), msg=None)
        sleep(1)

    def tearDown(self):
        logout(self)
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
