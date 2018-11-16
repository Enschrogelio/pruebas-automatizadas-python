import unittest
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from util.config import modelConfig, root_files
from util.functions import login, logout, db_functions

#Variables globales
types = [
    {"type": "IMAGE", "file": root_files+"creatives/png.png"},
    {"type": "GIF", "file": root_files+"creatives/gif.gif"},
    {"type": "VIDEO", "file": root_files+"creatives/video.mp4"},
    {"type": "HTML5", "file": root_files+"creatives/html5.html"}
]
list_creatives = [
    {"name": "Prueba IMAGEN", "status": 1, "measure": "10x10", "url": "http://www.algo.com", "type": "IMAGE"},
    {"name": "Prueba HTML", "status": 0, "measure": "5x15", "url": "http://www.compraalgo.com", "type": "HTML5"},
    {"name": "Prueba GIF", "status": 1, "measure": "3x18", "url": "http://www.promoalgo.com", "type": "GIF"},
    {"name": "Prueba Video", "status": 0, "measure": "30x15", "url": "http://www.cerebro.com", "type": "VIDEO"}
]
browser_name = None
client = 2
campaign = 2

class AddCreativeSuccessful(unittest.TestCase):

    def setUp(self):
        global browser_name,creative
        code = """
campaign = {1}
list_creatives = {0}
for creative in list_creatives:
    cur.execute("DELETE FROM creatives WHERE campaign_id = %d AND name = '%s';" % (campaign,creative["name"]))
""".format(list_creatives,campaign)
        creative = db_functions(code)
        self.driver = modelConfig.driver_web
        browser_name=self.driver.capabilities['browserName']
        if browser_name == "chrome":
            self.driver.maximize_window()

    def test_add_creative_success(self):
        global types, client, campaign, creative
        driver = self.driver
        login(self)
        self.assertIn("%s/admin/clients/" %modelConfig.base_url, driver.current_url, msg=None)
        sleep(1)
        driver.find_element_by_css_selector('a[href*="/admin/client/detail/%d/"]' % client).click()
        sleep(1)

        self.assertIn("%s/admin/client/detail/" %modelConfig.base_url, driver.current_url, msg=None)

        sleep(2)
        band = 0
        while band == 0:
            try:
                if driver.find_element_by_xpath('//a[@href="/admin/campaign/detail/%d/"]' % campaign):
                    band = 1
                    if browser_name == "internet explorer":
                        print(browser_name)
                    if browser_name == "chrome" or browser_name == "firefox" or browser_name == "edge":
                        posicion = driver.find_element_by_xpath('//a[@href="/admin/campaign/detail/%d/"]' % campaign) \
                            .location_once_scrolled_into_view
                        driver.execute_script("window.scrollTo(0, %d);" %(posicion["y"]+110))
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

        self.assertIn("%s/admin/campaign/detail/" % modelConfig.base_url, driver.current_url, msg=None)
        for posicion_file in range(4):
            print("\n<<<------ %s ------>>>\n" % types[posicion_file]["type"])
            posicion = driver.find_element_by_xpath('//*[@id="btn-add-"]').location_once_scrolled_into_view
            driver.execute_script("window.scrollTo(0, %d);" % (posicion["y"]+110))
            sleep(2)
            driver.find_element_by_xpath('//*[@id="btn-add-"]').click()
            sleep(2)
            driver.find_element_by_css_selector('#form-add-creative #id_name').clear()
            driver.find_element_by_css_selector('#form-add-creative #id_name') \
                .send_keys(list_creatives[posicion_file]["name"])
            driver.find_element_by_css_selector('#form-add-creative #id_status').click()
            sleep(1)
            #rand = random.randint(0,2)
            driver.find_element_by_css_selector('#form-add-creative #id_status > option[value="%d"]'
                                                % list_creatives[posicion_file]["status"]).click()
            sleep(1)
            driver.find_element_by_css_selector('#form-add-creative #id_measure').clear()
            driver.find_element_by_css_selector('#form-add-creative #id_measure') \
                .send_keys(list_creatives[posicion_file]["measure"])
            driver.find_element_by_css_selector('#form-add-creative #id_url').clear()
            driver.find_element_by_css_selector('#form-add-creative #id_url') \
                .send_keys(list_creatives[posicion_file]["url"])
            driver.find_element_by_css_selector('#form-add-creative #id_type').click()
            sleep(1)
            driver.find_element_by_css_selector('#form-add-creative #id_type > option[value="%s"]'
                                                % types[posicion_file]["type"]) \
                .click()
            sleep(1)
            driver.find_element_by_css_selector('#form-add-creative #id_type').click()
            sleep(1)
            #driver.find_element_by_css_selector('#form-add-creative #id_file').click()
            #sleep(5)
            driver.switch_to_window(driver.window_handles[0])
            sleep(2)
            if browser_name == "chrome" or browser_name == "firefox" or browser_name == "edge":
                posicion=driver.find_element_by_xpath('/html/body/div[12]/div/div/div[3]/button') \
                    .location_once_scrolled_into_view
                driver.execute_script("window.scrollTo(0, %d);" %(posicion["y"]))
            #for i in range(0,10):
            #    sleep(1)
            #    driver.find_element_by_css_selector('html').send_keys(Keys.ARROW_DOWN)
            sleep(2)
            Imagepath = types[posicion_file]["file"]
            driver.find_element_by_css_selector('#form-add-creative #id_file').send_keys(Imagepath)
            sleep(2)
            driver.find_element_by_xpath('//*[@id="modal-add-creative"]/div/div/div[3]/button').click()
            sleep(3)
            try:
                while driver.find_element_by_css_selector \
                            ('#form-add-creative div div.loader-input-file.center span'):
                    print("Cargando %s ..." % types[posicion_file]["type"])
                    sleep(2)
            except Exception:
                print("Archivo %s cargado" % types[posicion_file]["type"])

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)


    def tearDown(self):
        logout(self)
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()