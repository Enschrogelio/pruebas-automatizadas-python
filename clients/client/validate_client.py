import unittest
import json
from util.functions import ModelConfig, login, logout, db_functions, sleep, screenshot

# DATA SET
_type = "add"   # "edit" "detail" "add"  CAMBIAR EL TIPO DE PANTALLA EN LA QUE SE REALIZARA EL TEST
clients = '''
        [{ "email" : "MATAMOROS@gmail.com","name" : "OMAR IZHAR ALVAREZ CASTILLO","password" : "ALCANTARA", 
        "cpm" : "1", "budget" : "15000.90", "company" : "AUTOTRANSPORTES MATAMOROS MAZATLAN DIVISION", 
        "rfc" : "ATM850415695", "address" : "2 DE ABRIL NUM 1022 ORIENTE COL INDEPENDENCIA MONTERREY N L",
        "phone" : "3125256987"
        }]'''


class ValidateClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = ModelConfig.driver_web

        # ENVIROMENT SETTING
        info = json.loads(clients)
        code = """
info = {0}
cur.execute("DELETE FROM clients WHERE rfc = '%s'" % info[0]['rfc'])
sql = 'INSERT INTO clients (person_contact, cpm, budget, status, email, "createdAt", updated_at, ' \
'password, company_name, rfc, phone, address) ' \
'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)' 
val = (info[0]['name'], info[0]['cpm'], info[0]['budget'], 1, info[0]['email'], strftime("%Y/%m/%d"), \
strftime("%Y/%m/%d"), info[0]['password'], info[0]['company'], info[0]['rfc'], info[0]['phone'], info[0]['address'])
cur.execute(sql, val)""".format(info)
        db_functions(code)

    def function_type(self, __type, refresh):
        driver = self.driver
        info = json.loads(clients)
        if _type == "add":
            driver.refresh()
            form = '#form-add'
            modal = '#modal-add'
            driver.find_element_by_xpath('//*[@id="btn-add"]').click()
            return form, modal
        else:
            if __type == "edit":
                form = '#form-edit'
                modal = '#modal-edit'
                if refresh == 0:
                    driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
                    driver.find_element_by_id('search').send_keys(info[0]['rfc'])
                    sleep(5)
                    driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[6]/a[2]').click()
                    return form, modal
                else:
                    driver.refresh()
                return form, modal
            else:
                if _type == "detail":
                    form = '#form-edit'
                    modal = '#modal-edit'
                    if refresh == 0:
                        driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
                        driver.find_element_by_id('search').send_keys(info[0]['rfc'])
                        sleep(5)
                        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[6]/a[1]').click()
                        sleep(3)
                        self.assertEqual(info[0]['company'],
                                         driver.find_element_by_xpath('//*[@id="client-info-header"]/a[2]')
                                         .text, msg=None)
                        driver.find_element_by_xpath('//*[@id="btn-edit"]').click()
                        return form, modal
                    else:
                        driver.refresh()
                    return form, modal
                else:
                    return "cambiar variable _type: add, edit o detail"

    def test_client_exist(self):
        # login
        driver = self.driver
        refresh = 0
        login(self)
        sleep(5)
        form, modal = self.function_type(_type, refresh)
        sleep(5)
        driver.find_element_by_css_selector(form+' #id_email').clear()
        driver.find_element_by_css_selector(form+' #id_email').send_keys("sonia.amezcua@varangard.com")
        driver.find_element_by_css_selector(form+' #id_status').click()
        driver.find_element_by_css_selector(form+' #id_password').clear()
        driver.find_element_by_css_selector(form+' #id_password').send_keys("123")
        driver.find_element_by_css_selector(form+' #id_cpm').clear()
        driver.find_element_by_css_selector(form+' #id_cpm').send_keys("12")
        driver.find_element_by_css_selector(form+' #id_budget').clear()
        driver.find_element_by_css_selector(form+' #id_budget').send_keys("12")
        driver.find_element_by_css_selector(form+' #id_company_name').clear()
        driver.find_element_by_css_selector(form+' #id_company_name') \
            .send_keys("AUTOLINEAS UNIDAS SALVADOR ALMAGUER, S.A.DE C.V")
        driver.find_element_by_css_selector(modal+'> div > div > div.modal-footer.col-md-12 > button').click()
        sleep(1)
        self.assertEqual('Client with this Email already exists.',
                         driver.find_element_by_css_selector(form+' > div.form-group.has-error > span').text, msg=None)
        path = "clients/client/screenshot/test_client_exist"+form
        screenshot(self, path)
        sleep(3)

    def test_required(self):
        driver = self.driver
        refresh = 1
        form, modal = self.function_type(_type, refresh)
        sleep(5)
        driver.find_element_by_css_selector(form+' #id_email').clear()
        driver.find_element_by_css_selector(form+' #id_person_contact').clear()
        driver.find_element_by_css_selector(form+' #id_password').clear()
        driver.find_element_by_css_selector(form+' #id_cpm').clear()
        driver.find_element_by_css_selector(form+' #id_budget').clear()
        driver.find_element_by_css_selector(form+' #id_company_name').clear()
        driver.find_element_by_css_selector(form+' #id_rfc').clear()
        driver.find_element_by_css_selector(form+' #id_address').clear()
        driver.find_element_by_css_selector(form+' #id_phone').clear()
        driver.find_element_by_css_selector(modal+'> div > div > div.modal-footer.col-md-12 > button').click()
        sleep(2)
        self.assertEqual('This field is empty', driver.find_element_by_css_selector(form+' > div:nth-child(2) > span')
                         .text, msg=None)
        self.assertEqual('This field is empty', driver.find_element_by_css_selector(form+' > div:nth-child(5) > span')
                         .text, msg=None)
        self.assertEqual('This field is empty', driver.find_element_by_css_selector(form+' > div:nth-child(6) > span')
                         .text, msg=None)
        self.assertEqual('This field is empty.', driver.find_element_by_css_selector(form+' > div:nth-child(7) > span')
                         .text, msg=None)  # quitar punto
        self.assertEqual('This field is empty', driver.find_element_by_css_selector(form+' > div:nth-child(8) > span')
                         .text, msg=None)
        path = "clients/client/screenshot/test_required_"+form
        screenshot(self, path)
        sleep(3)

    def test_data_type(self):
        driver = self.driver
        refresh = 1
        form, modal = self.function_type(_type, refresh)
        sleep(5)
        driver.find_element_by_css_selector(form+' #id_cpm').clear()
        driver.find_element_by_css_selector(form+' #id_cpm').send_keys("aa")
        driver.find_element_by_css_selector(form+' #id_budget').clear()
        driver.find_element_by_css_selector(form+' #id_budget').send_keys("aa")
        driver.find_element_by_css_selector(form+' #id_phone').clear()
        driver.find_element_by_css_selector(form+' #id_phone').send_keys("aa")
        driver.find_element_by_css_selector(modal+'> div > div > div.modal-footer.col-md-12 > button').click()
        sleep(1)
        self.assertEqual('Enter a valid budget. Maximum allowed decimals: 2',
                         driver.find_element_by_css_selector(form+' > div:nth-child(7) > span').text, msg=None)
        path = "clients/client/screenshot/test_data_type"+form
        screenshot(self, path)
        sleep(3)

    def test_format_email(self):
        driver = self.driver
        refresh = 1
        form, modal = self.function_type(_type, refresh)
        path = "clients/client/screenshot/test_format_email"+form
        sleep(5)
        driver.find_element_by_css_selector(form+' #id_email').clear()
        driver.find_element_by_css_selector(form+' #id_email').send_keys("sonia.amezcua")
        driver.find_element_by_css_selector(modal+'> div > div > div.modal-footer.col-md-12 > button').click()
        sleep(1)
        self.assertEqual('Enter valid email',
                         driver.find_element_by_css_selector(form+' > div:nth-child(2) > span').text, msg=None)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_css_selector(form+' #id_email').clear()
        driver.find_element_by_css_selector(form+' #id_email').send_keys("sonia.amezcua@")
        driver.find_element_by_css_selector(modal+'> div > div > div.modal-footer.col-md-12 > button').click()
        sleep(1)
        self.assertEqual('Enter valid email',
                         driver.find_element_by_css_selector(form+' > div:nth-child(2) > span').text, msg=None)
        screenshot(self, path)
        # sleep(1)
        # driver.find_element_by_css_selector(form+' #id_email').clear()
        # driver.find_element_by_css_selector(form+' #id_email').send_keys("sonia.amezcua@varangard")
        # driver.find_element_by_css_selector(modal+'> div > div > div.modal-footer.col-md-12 > button').click()
        # sleep(1)
        # self.assertEqual('Enter valid email',
        #                  driver.find_element_by_css_selector(form+' > div:nth-child(2) > span').text, msg=None)
        sleep(5)
        screenshot(self, path)

    def test_max_min(self):
        driver = self.driver
        refresh = 1
        form, modal = self.function_type(_type, refresh)
        path = "clients/client/screenshot/test_max_min"+form
        sleep(5)
        driver.find_element_by_css_selector(form+' #id_budget').clear()
        driver.find_element_by_css_selector(form+' #id_budget').send_keys("-0.01")
        driver.find_element_by_css_selector(modal+'> div > div > div.modal-footer.col-md-12 > button').click()
        sleep(1)
        self.assertEqual('Enter a valid budget. Maximum allowed decimals: 2',
                         driver.find_element_by_css_selector(form+' > div:nth-child(7) > span').text, msg=None)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_css_selector(form+' #id_budget').clear()
        driver.find_element_by_css_selector(form+' #id_budget').send_keys("999999999999999999.99")
        driver.find_element_by_css_selector(modal+'> div > div > div.modal-footer.col-md-12 > button').click()
        sleep(1)
        self.assertEqual('Enter a valid budget. Maximum allowed decimals: 2',
                         driver.find_element_by_css_selector(form+' > div:nth-child(7) > span').text, msg=None)
        sleep(3)
        screenshot(self, path)

    def test_format_rfc(self):
        driver = self.driver
        refresh = 1
        form, modal = self.function_type(_type, refresh)
        path = "clients/client/screenshot/test_format_rfc"+form
        sleep(8)
        driver.find_element_by_css_selector(form+' #id_rfc').clear()
        driver.find_element_by_css_selector(form+' #id_rfc').send_keys("AEAS850120H3A2")
        driver.find_element_by_css_selector(modal+'> div > div > div.modal-footer.col-md-12 > button').click()
        sleep(1)
        self.assertEqual('Enter valid RFC',
                         driver.find_element_by_css_selector(form+' > div:nth-child(9) > span').text, msg=None)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_css_selector(form+' #id_rfc').clear()
        driver.find_element_by_css_selector(form+' #id_rfc').send_keys("AEA850120H3A2")
        driver.find_element_by_css_selector(modal+'> div > div > div.modal-footer.col-md-12 > button').click()
        sleep(1)
        self.assertEqual('Enter valid RFC',
                         driver.find_element_by_css_selector(form+' > div:nth-child(9) > span').text, msg=None)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_css_selector(form+' #id_rfc').clear()
        driver.find_element_by_css_selector(form+' #id_rfc').send_keys("AEAS8R0120H3A")
        driver.find_element_by_css_selector(modal+'> div > div > div.modal-footer.col-md-12 > button').click()
        sleep(1)
        self.assertEqual('Enter valid RFC',
                         driver.find_element_by_css_selector(form+' > div:nth-child(9) > span').text, msg=None)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_css_selector(form+' #id_rfc').clear()
        driver.find_element_by_css_selector(form+' #id_rfc').send_keys("AAS8R0120H3A")
        driver.find_element_by_css_selector(modal+'> div > div > div.modal-footer.col-md-12 > button').click()
        sleep(1)
        self.assertEqual('Enter valid RFC',
                         driver.find_element_by_css_selector(form+' > div:nth-child(9) > span').text, msg=None)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_css_selector(form+' #id_rfc').clear()
        driver.find_element_by_css_selector(form+' #id_rfc').send_keys("A#AS850120H3A")
        driver.find_element_by_css_selector(modal+'> div > div > div.modal-footer.col-md-12 > button').click()
        sleep(1)
        self.assertEqual('Enter valid RFC',
                         driver.find_element_by_css_selector(form+' > div:nth-child(9) > span').text, msg=None)
        sleep(4)
        screenshot(self, path)

    @classmethod
    def tearDownClass(cls):
        logout(cls)
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
