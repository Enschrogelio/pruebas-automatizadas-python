import unittest
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from util.config import ModelConfig, root_files
from util.functions import login, logout, db_functions, screenshot, randoms

# Variables globales
types = [
    {"type": "IMAGE", "file": root_files + "creatives/png.png"},
    {"type": "GIF", "file": root_files + "creatives/gif.gif"},
    {"type": "VIDEO", "file": root_files + "creatives/video.mp4"},
    {"type": "HTML5", "file": root_files + "creatives/html5.html"},
]
list_creatives = [
    {"name": "Compra ahorra", "status": 1, "measure": "10x10", "url": "http://www.algo.com", "type": "IMAGE"},
    {"name": "Compra gasta", "status": 0, "measure": "5x15", "url": "http://www.compraalgo.com", "type": "HTML5"},
    {"name": "Promo 1", "status": 1, "measure": "3x18", "url": "http://www.promoalgo.com", "type": "GIF"}
]
browser_name: None = None
client: int = 2
campaign: int = 2
creative: None = None
type_modal: str = "add"


class ValidateCreative(unittest.TestCase):

    driver: None = None

    def go_to_creative(self):
        global types, client, campaign, creative
        driver = self.driver
        login(self)
        sleep(1)
        driver.find_element_by_css_selector('a[href*="/admin/client/detail/%d/"]' % client).click()
        sleep(1)
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
                        driver.execute_script("window.scrollTo(0, %d);" % (position["y"] + 110))
                        sleep(2)
            except NoSuchElementException:
                if browser_name == "chrome" or browser_name == "firefox" or browser_name == "edge":
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(2)
                driver.find_element_by_css_selector("#campaigntable_paginate > ul > li.next > a").click()
                sleep(1)
                band = 0
        driver.find_element_by_xpath('//a[@href="/admin/campaign/detail/%d/"]' % campaign).click()
        sleep(1)

    def select_test(self):
        driver = self.driver
        if type_modal == "edit":
            # ########################## EDIT #########################
            position = driver.find_element_by_xpath('//a[@href="/admin/campaign/detail/%d/creative/update/%s"]'
                                                    % (campaign, creative)).location_once_scrolled_into_view
            driver.execute_script("window.scrollTo(0, %d);" % (position["y"] + 110))
            sleep(2)
            driver.find_element_by_xpath('//a[@href="/admin/campaign/detail/%d/creative/update/%s"]'
                                         % (campaign, creative)).click()
            sleep(2)
            self.assertIn("%s/admin/campaign/detail/%d/creative/update/%s"
                          % (ModelConfig.base_url, campaign, creative), driver.current_url, msg=None)
            # ########################################################
        else:
            if type_modal == "add":
                # ########################## ADD #########################
                position = driver.find_element_by_css_selector('#btn-add-').location_once_scrolled_into_view
                driver.execute_script("window.scrollTo(0, %d);" % (position["y"] + 110))
                sleep(2)
                driver.find_element_by_css_selector('#btn-add-').click()
                # ########################################################
        sleep(1)
    
    @classmethod
    def setUpClass(cls):
        global browser_name, creative
        code = """
campaign = {1}
list_creatives = {0}
for creative in list_creatives:
    cur.execute("DELETE FROM creatives WHERE campaign_id = %d AND name = '%s';" % (campaign, creative["name"]))
rand = random.randint(0, len(list_creatives)-1)
cur.execute("INSERT INTO creatives (name, url, measure, type, status, created_at, updated_at, campaign_id) VALUES "
            "('%s','%s','%s','%s',%d,current_timestamp,current_timestamp,%d) RETURNING id;" 
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
        cls.driver = ModelConfig.driver_web
        browser_name = cls.driver.capabilities['browserName']
        if browser_name == "chrome":
            cls.driver.maximize_window()
        # noinspection PyCallByClass
        cls.go_to_creative(cls)

    def setUp(self):
        pass

    def test_empty_fields(self):
        driver = self.driver
        self.select_test()
        sleep(2)
        driver.find_element_by_css_selector('#form-%s-creative #id_name' % type_modal).clear()
        driver.find_element_by_css_selector('#form-%s-creative #id_measure' % type_modal).clear()
        driver.find_element_by_css_selector('#form-%s-creative #id_url' % type_modal).clear()
        driver.find_element_by_xpath('//*[@id="modal-%s-creative"]/div/div/div[3]/button' % type_modal).click()
        sleep(2)
        self.assertEqual("This field is empty", driver.
                         find_element_by_css_selector("#form-%s-creative > div:nth-child(2) > span" % type_modal).
                         get_attribute("innerText"), msg=None)
        self.assertEqual("This field is empty", driver.
                         find_element_by_css_selector("#form-%s-creative > div:nth-child(4) > span" % type_modal).
                         get_attribute("innerText"), msg=None)
        self.assertEqual("This field is empty.", driver.
                         find_element_by_css_selector("#form-%s-creative > div:nth-child(5) > span" % type_modal).
                         get_attribute("innerText"), msg=None)
        if type_modal == "add":
            self.assertEqual("THIS FIELD IS EMPTY", driver.
                             find_element_by_css_selector("#form-%s-creative > div.drag-drop > label > span.help-block"
                                                          % type_modal).get_attribute("innerText"), msg=None)
        path = "clients/campaigns/creatives/screenshot/test_url_format_"+type_modal+"_creative"
        screenshot(self, path)

    def test_max_min(self):
        driver = self.driver
        self.select_test()
        sleep(5)
        # ######################### Maximum #########################
        driver.find_element_by_css_selector('#form-%s-creative #id_name' % type_modal).clear()
        driver.find_element_by_css_selector('#form-%s-creative #id_name' % type_modal).send_keys(randoms(251, "letter"))
        driver.find_element_by_css_selector('#form-%s-creative #id_measure' % type_modal).clear()
        driver.find_element_by_css_selector('#form-%s-creative #id_measure' % type_modal).\
            send_keys(randoms(251, "number"))
        driver.find_element_by_css_selector('#form-%s-creative #id_url' % type_modal).clear()
        driver.find_element_by_css_selector('#form-%s-creative #id_url' % type_modal).\
            send_keys("http://"+randoms(244, "letter"))
        sleep(1)
        self.assertEqual(250, len(driver.find_element_by_css_selector('#form-%s-creative #id_name' % type_modal).
                                  get_attribute("value")), msg=None)
        self.assertEqual(250, len(driver.find_element_by_css_selector('#form-%s-creative #id_measure' % type_modal).
                                  get_attribute("value")), msg=None)
        self.assertEqual(250, len(driver.find_element_by_css_selector('#form-%s-creative #id_url' % type_modal).
                                  get_attribute("value")), msg=None)
        path = "clients/campaigns/creatives/screenshot/test_max_"+type_modal+"_creative"
        screenshot(self, path)
        # ###########################################################

        # ######################### Minimum #########################
        driver.find_element_by_css_selector('#form-%s-creative #id_url' % type_modal).clear()
        driver.find_element_by_css_selector('#form-%s-creative #id_url' % type_modal).send_keys("http:")
        driver.find_element_by_xpath('//*[@id="modal-%s-creative"]/div/div/div[3]/button' % type_modal).click()
        self.assertEqual("Enter a valid URL.",
                         len(driver.find_element_by_css_selector('#form-%s-creative .help-block' % type_modal).
                             get_attribute("innerText")), msg=None)
        path = "clients/campaigns/creatives/screenshot/test_min_"+type_modal+"_creative"
        screenshot(self, path)
        # ###########################################################

    def test_url_format(self):
        global type_modal
        driver = self.driver
        self.select_test()
        driver.find_element_by_css_selector('#form-%s-creative #id_name' % type_modal).clear()
        driver.find_element_by_css_selector('#form-%s-creative #id_measure' % type_modal).clear()
        driver.find_element_by_css_selector('#form-%s-creative #id_url' % type_modal).clear()
        driver.find_element_by_css_selector('#form-%s-creative #id_url' % type_modal).send_keys("www.algo.com")
        driver.find_element_by_xpath('//*[@id="modal-%s-creative"]/div/div/div[3]/button' % type_modal).click()
        self.assertEqual("Enter a valid URL.",
                         driver.find_element_by_css_selector('#form-%s-creative > div:nth-child(5) > span' % type_modal).
                             get_attribute("innerText"), msg=None)
        path = "clients/campaigns/creatives/screenshot/test_url_format_"+type_modal+"_creative"
        screenshot(self, path)

    def test_file_creative_validation(self):
        global types, type_modal
        driver = self.driver
        self.select_test()
        sleep(2)
        driver.find_element_by_css_selector('#form-%s-creative #id_name' % type_modal).clear()
        driver.find_element_by_css_selector('#form-%s-creative #id_name' % type_modal).send_keys("name")
        driver.find_element_by_css_selector('#form-%s-creative #id_status' % type_modal).click()
        sleep(1)
        driver.find_element_by_css_selector('#form-%s-creative #id_measure' % type_modal).clear()
        driver.find_element_by_css_selector('#form-%s-creative #id_measure' % type_modal).send_keys("10x5")
        driver.find_element_by_css_selector('#form-%s-creative #id_url' % type_modal).clear()
        driver.find_element_by_css_selector('#form-%s-creative #id_url' % type_modal).send_keys("http://www.algo.com")
        sleep(2)
        for position_file in range(4):
            print("\n<<<------ %s ------>>>\n" % types[position_file]["type"])
            driver.find_element_by_css_selector('#form-%s-creative #id_type' % type_modal).click()
            sleep(1)
            driver.find_element_by_css_selector('#form-%s-creative #id_type > option[value="%s"]'
                                                % (type_modal, types[position_file]["type"])).click()
            sleep(1)
            driver.find_element_by_css_selector('#form-%s-creative #id_type' % type_modal).click()
            sleep(1)
            sleep(2)
            if browser_name == "chrome" or browser_name == "firefox" or browser_name == "edge":
                position = driver.find_element_by_xpath('/html/body/div[13]/div/div/div[3]/button') \
                    .location_once_scrolled_into_view
                driver.execute_script("window.scrollTo(0, %d);" % (position["y"]))
            sleep(2)
            if position_file == len(types) - 1:
                image_path = types[0]["file"]
            else:
                image_path = types[position_file + 1]["file"]
            if position_file == 0:
                image_path = types[3]["file"]
            driver.find_element_by_css_selector('#form-%s-creative #id_file' % type_modal).send_keys(image_path)
            sleep(2)
            driver.find_element_by_xpath('//*[@id="modal-%s-creative"]/div/div/div[3]/button' % type_modal).click()
            sleep(3)
            try:
                while driver.find_element_by_css_selector('#form-%s-creative div div.loader-input-file.center span'
                                                          % type_modal):
                    print("Cargando %s ..." % types[position_file]["type"])
                    sleep(2)
            except NoSuchElementException:
                print("Archivo %s cargado" % types[position_file]["type"])
                sleep(2)
            if types[position_file]["type"] == "HTML5":
                self.assertEqual("The file must be a html or html compressed in zip format.",
                                 driver.find_element_by_xpath('//*[@id="form-%s-creative"]/div[6]/div[1]/span'
                                                              % type_modal).get_attribute("innerText"), msg=None)
            else:
                self.assertEqual("The file must be a: %s" % types[position_file]["type"],
                                 driver.find_element_by_xpath('//*[@id="form-%s-creative"]/div[6]/div[1]/span'
                                                              % type_modal).get_attribute("innerText"), msg=None)
            path = "clients/campaigns/creatives/screenshot/file_validation_"+type_modal+"_creative"
            screenshot(self, path)
        sleep(2)

    @classmethod
    def tearDownClass(cls):
        logout(cls)
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
