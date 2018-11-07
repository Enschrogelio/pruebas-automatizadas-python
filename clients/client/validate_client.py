import unittest
from util.functions import *

class ValidateClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = modelConfig.driverWeb
    #def setUp(self):
        # self.driver = modelConfig.driverWeb

    def test_required(self):
        driver = self.driver
        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        sleep(1)
        driver.find_element_by_xpath("//*[@id='modal-add']/div[1]/div[1]/div[3]/button[1 and @type='submit']").click()
        sleep(2)
        self.assertEqual('This field is empty', driver.find_element_by_xpath('//*[@id="form-add"]/div[1]/span')
                         .text, msg=None)
        self.assertEqual('This field is empty', driver.find_element_by_xpath('//*[@id="form-add"]/div[4]/span')
                         .text, msg=None)
        self.assertEqual('This field is empty', driver.find_element_by_xpath('//*[@id="form-add"]/div[5]/span')
                         .text, msg=None)
        self.assertEqual('This field is empty.', driver.find_element_by_xpath('//*[@id="form-add"]/div[6]/span')
                         .text, msg=None) #quitar punto
        self.assertEqual('This field is empty', driver.find_element_by_xpath('//*[@id="form-add"]/div[7]/span')
                         .text, msg=None)
        mi_ruta = "clients/client/screenshot/test_required"
        screenshot(self, mi_ruta)
        sleep(3)

        driver.refresh()

    def test_client_exist(self):
        #login
        driver = self.driver
        login(self)
        sleep(2)

        self.assertIn("http://stage.eupam5k9mb.us-west-2.elasticbeanstalk.com/admin/clients/",
                      driver.current_url, msg=None)
        sleep(3)
        driver.find_element_by_xpath('//*[@id="sections-access"]/div[2]/a').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_email"]').send_keys("sonia.amezcua@varangard.com")
        driver.find_element_by_xpath('//*[@id="id_status"]').click()
        driver.find_element_by_xpath('//*[@id="id_password"]').send_keys("123")
        driver.find_element_by_xpath('//*[@id="id_cpm"]').send_keys("12")
        driver.find_element_by_xpath('//*[@id="id_budget"]').send_keys("12")
        driver.find_element_by_xpath('//*[@id="id_company_name"]')\
            .send_keys("AUTOLINEAS UNIDAS SALVADOR ALMAGUER, S.A.DE C.V")
        driver.find_element_by_xpath("//*[@id='modal-add']/div[1]/div[1]/div[3]/button[1 and @type='submit']").click()
        sleep(1)
        self.assertEqual('Client with this Email already exists.',
                         driver.find_element_by_xpath('//*[@id="form-add"]/div[1]/span').text, msg=None)
        mi_ruta = "clients/client/screenshot/test_client_exist"
        screenshot(self, mi_ruta)
        sleep(3)
        driver.refresh()

    def test_data_type(self):
        driver = self.driver
        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_cpm"]').send_keys("aa")
        driver.find_element_by_xpath('//*[@id="id_budget"]').send_keys("aa")
        driver.find_element_by_xpath('//*[@id="id_phone"]').send_keys("aa")
        driver.find_element_by_xpath("//*[@id='modal-add']/div[1]/div[1]/div[3]/button[1 and @type='submit']").click()
        sleep(1)
        self.assertEqual('Enter a valid budget. Maximum allowed decimals: 2',
                         driver.find_element_by_xpath('//*[@id="form-add"]/div[6]/span').text, msg=None)
        mi_ruta = "clients/client/screenshot/test_data_type"
        screenshot(self, mi_ruta)
        sleep(5)
        driver.refresh()

    def test_format_email(self):
        mi_ruta = "clients/client/screenshot/test_format_email"
        driver = self.driver
        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_email"]').clear()
        driver.find_element_by_xpath('//*[@id="id_email"]').send_keys("sonia.amezcua")
        driver.find_element_by_xpath("//*[@id='modal-add']/div[1]/div[1]/div[3]/button[1 and @type='submit']").click()
        sleep(1)
        self.assertEqual('Enter valid email', driver.find_element_by_xpath('//*[@id="form-add"]/div[1]/span')
                         .text, msg=None)
        screenshot(self, mi_ruta)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_email"]').clear()
        driver.find_element_by_xpath('//*[@id="id_email"]').send_keys("sonia.amezcua@")
        driver.find_element_by_xpath("//*[@id='modal-add']/div[1]/div[1]/div[3]/button[1 and @type='submit']").click()
        sleep(1)
        self.assertEqual('Enter valid email', driver.find_element_by_xpath('//*[@id="form-add"]/div[1]/span')
                         .text, msg=None)
        screenshot(self, mi_ruta)
        # sleep(1)
        # driver.find_element_by_xpath('//*[@id="id_email"]').clear()
        # driver.find_element_by_xpath('//*[@id="id_email"]').send_keys("sonia.amezcua@varangard")
        # driver.find_element_by_xpath("//*[@id='modal-add']/div[1]/div[1]/div[3]/button[1 and @type='submit']").click()
        # sleep(1)
        # self.assertEqual('Enter valid email', driver.find_element_by_xpath('//*[@id="form-add"]/div[1]/span').text, msg=None)
        sleep(5)
        screenshot(self, mi_ruta)
        driver.refresh()

    def test_max_min(self):
        mi_ruta = "clients/client/screenshot/test_max_min"
        driver = self.driver
        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_budget"]').send_keys("-0.01")
        driver.find_element_by_xpath("//*[@id='modal-add']/div[1]/div[1]/div[3]/button[1 and @type='submit']").click()
        sleep(1)
        self.assertEqual('Enter a valid budget. Maximum allowed decimals: 2',
                         driver.find_element_by_xpath('//*[@id="form-add"]/div[6]/span').text, msg=None)
        screenshot(self, mi_ruta)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_budget"]').clear()
        driver.find_element_by_xpath('//*[@id="id_budget"]').send_keys("999999999999999999.99")
        driver.find_element_by_xpath("//*[@id='modal-add']/div[1]/div[1]/div[3]/button[1 and @type='submit']").click()
        sleep(1)
        self.assertEqual('Enter a valid budget. Maximum allowed decimals: 2',
                         driver.find_element_by_xpath('//*[@id="form-add"]/div[6]/span').text, msg=None)
        sleep(3)
        screenshot(self, mi_ruta)
        driver.refresh()

    def test_format_rfc(self):
        mi_ruta = "clients/client/screenshot/test_format_rfc"
        driver = self.driver
        driver.find_element_by_xpath('//*[@id="btn-add"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_rfc"]').send_keys("AEAS850120H3A2")
        driver.find_element_by_xpath("//*[@id='modal-add']/div[1]/div[1]/div[3]/button[1 and @type='submit']").click()
        sleep(1)
        self.assertEqual('Enter valid RFC', driver.find_element_by_xpath('//*[@id="form-add"]/div[8]/span')
                         .text, msg=None)
        screenshot(self, mi_ruta)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_rfc"]').clear()
        driver.find_element_by_xpath('//*[@id="id_rfc"]').send_keys("AEA850120H3A2")
        driver.find_element_by_xpath("//*[@id='modal-add']/div[1]/div[1]/div[3]/button[1 and @type='submit']").click()
        sleep(1)
        self.assertEqual('Enter valid RFC', driver.find_element_by_xpath('//*[@id="form-add"]/div[8]/span')
                         .text, msg=None)
        screenshot(self, mi_ruta)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_rfc"]').clear()
        driver.find_element_by_xpath('//*[@id="id_rfc"]').send_keys("AEAS8R0120H3A")
        driver.find_element_by_xpath("//*[@id='modal-add']/div[1]/div[1]/div[3]/button[1 and @type='submit']").click()
        sleep(1)
        self.assertEqual('Enter valid RFC', driver.find_element_by_xpath('//*[@id="form-add"]/div[8]/span')
                         .text, msg=None)
        screenshot(self, mi_ruta)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_rfc"]').clear()
        driver.find_element_by_xpath('//*[@id="id_rfc"]').send_keys("AAS8R0120H3A")
        driver.find_element_by_xpath("//*[@id='modal-add']/div[1]/div[1]/div[3]/button[1 and @type='submit']").click()
        sleep(1)
        self.assertEqual('Enter valid RFC', driver.find_element_by_xpath('//*[@id="form-add"]/div[8]/span')
                         .text, msg=None)
        screenshot(self, mi_ruta)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="id_rfc"]').clear()
        driver.find_element_by_xpath('//*[@id="id_rfc"]').send_keys("A#AS850120H3A")
        driver.find_element_by_xpath("//*[@id='modal-add']/div[1]/div[1]/div[3]/button[1 and @type='submit']").click()
        sleep(1)
        self.assertEqual('Enter valid RFC', driver.find_element_by_xpath('//*[@id="form-add"]/div[8]/span')
                         .text, msg=None)
        sleep(4)
        screenshot(self, mi_ruta)
        driver.refresh()

    #def tearDown(self):
        #self..driver.close()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

if __name__ == "__main__":
    unittest.main()
