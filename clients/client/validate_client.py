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
refresh = 0


class ValidateClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = ModelConfig.driver_web
        cls.driver.maximize_window()
        login(cls)

        # ENVIROMENT SETTING
        info = json.loads(clients)
        code = """
info = {0}
cur.execute("SELECT id FROM clients WHERE email = '%s'" % info[0]['email'])
try:
    id = cur.fetchone()[0]
    if id is not None:
        cur.execute("DELETE FROM campaigns WHERE client_id = '%d';" % id)
        cur.execute("DELETE FROM clients WHERE id = '%d';" % id)
except Exception as errorFetch:
    errorFetch
sql = 'INSERT INTO clients (person_contact, cpm, budget, status, email, "created_at", updated_at, ' \
'password, company_name, rfc, phone, address) ' \
'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)' 
val = (info[0]['name'], info[0]['cpm'], info[0]['budget'], 1, info[0]['email'], strftime("%Y/%m/%d"), \
strftime("%Y/%m/%d"), info[0]['password'], info[0]['company'], info[0]['rfc'], info[0]['phone'], info[0]['address'])
cur.execute(sql, val)""".format(info)
        db_functions(code)

    def function_type(self, _type):
        global refresh
        driver = self.driver
        info = json.loads(clients)
        if _type == "add":
            driver.refresh()
            form = '#add-form-'
            form2 = '#form-add'
            modal = '#modal-add'
            driver.find_element_by_xpath('//*[@id="btn-add"]').click()
            return form, form2, modal
        else:
            if _type == "edit":
                form = '#edit-form-'  
                form2 = '#form-edit'
                modal = '#modal-edit'
                if refresh == 0:
                    driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
                    driver.find_element_by_id('search').send_keys(info[0]['rfc'])
                    sleep(5)
                    driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[5]/a[2]').click()
                    refresh = 1
                    return form, form2, modal
                else:
                    driver.refresh()
                return form, form2, modal
            else:
                if _type == "detail":
                    form = '#edit-form-'
                    form2 = '#form-edit'
                    modal = '#modal-edit'
                    if refresh == 0:
                        driver.find_element_by_xpath('//*[@id="inputSrc"]/img').click()
                        driver.find_element_by_id('search').send_keys(info[0]['rfc'])
                        sleep(5)
                        driver.find_element_by_xpath('//*[@id="clienttable"]/tbody/tr[1]/td[5]/a[1]').click()
                        sleep(3)
                        self.assertEqual(info[0]['company'],
                                         driver.find_element_by_xpath('//*[@id="client-info-header"]/a[2]')
                                         .text, msg=None)
                        driver.find_element_by_xpath('//*[@id="btn-edit"]').click()
                        refresh = 1
                        return form, form2, modal
                    else:
                        driver.refresh()
                    return form, form2, modal
                else:
                    return "cambiar variable _type: add, edit o detail"

    def test_client_exist(self):
        driver = self.driver
        sleep(5)
        form, form2, modal = self.function_type(_type)
        sleep(5)
        driver.find_element_by_css_selector('%semail' % form).clear()
        driver.find_element_by_css_selector('%semail' % form).send_keys("sonia.amezcua@varangard.com")
        driver.find_element_by_css_selector('%sstatus' % form).click()
        driver.find_element_by_css_selector('%spassword' % form).clear()
        driver.find_element_by_css_selector('%spassword' % form).send_keys("123")
        driver.find_element_by_css_selector('%scpm' % form).clear()
        driver.find_element_by_css_selector('%scpm' % form).send_keys("12")
        driver.find_element_by_css_selector('%sbudget' % form).clear()
        driver.find_element_by_css_selector('%sbudget' % form).send_keys("12")
        driver.find_element_by_css_selector('%scompany_name' % form).clear()
        driver.find_element_by_css_selector('%scompany_name' % form) \
            .send_keys("AUTOLINEAS UNIDAS SALVADOR ALMAGUER, S.A.DE C.V")
        driver.find_element_by_css_selector('%s> div > div > div.modal-footer.col-md-12 > button' % modal).click()
        sleep(1)
        self.assertEqual('Client with this Email already exists.',
                         driver.find_element_by_css_selector('%s > div.form-group.has-error > span' % form2)
                         .text, msg=None)
        path = "clients/client/screenshot/test_client_exist_%s" % form
        screenshot(self, path)
        sleep(3)

    def test_required(self):
        driver = self.driver
        form, form2, modal = self.function_type(_type)
        sleep(5)
        driver.find_element_by_css_selector('%semail' % form).clear()
        driver.find_element_by_css_selector('%sperson_contact' % form).clear()
        driver.find_element_by_css_selector('%spassword' % form).clear()
        driver.find_element_by_css_selector('%scpm' % form).clear()
        driver.find_element_by_css_selector('%sbudget' % form).clear()
        driver.find_element_by_css_selector('%scompany_name' % form).clear()
        driver.find_element_by_css_selector('%srfc' % form).clear()
        driver.find_element_by_css_selector('%saddress' % form).clear()
        driver.find_element_by_css_selector('%sphone' % form).clear()
        driver.find_element_by_css_selector('%s> div > div > div.modal-footer.col-md-12 > button' % modal).click()
        sleep(2)
        self.assertEqual('This field is empty',
                         driver.find_element_by_css_selector('%s > div:nth-child(2) > span' % form2).text, msg=None)
        self.assertEqual('This field is empty',
                         driver.find_element_by_css_selector('%s > div:nth-child(5) > span' % form2) .text, msg=None)
        self.assertEqual('This field is empty',
                         driver.find_element_by_css_selector('%s > div:nth-child(6) > span' % form2).text, msg=None)
        self.assertEqual('This field is empty.',
                         driver.find_element_by_css_selector('%s > div:nth-child(7) > span' % form2).text, msg=None)  # quitar punto
        self.assertEqual('This field is empty',
                         driver.find_element_by_css_selector('%s > div:nth-child(8) > span' % form2).text, msg=None)
        path = "clients/client/screenshot/test_required_%s" % form
        screenshot(self, path)
        sleep(3)

    def test_data_type(self):
        driver = self.driver
        form, form2, modal = self.function_type(_type)
        sleep(5)
        driver.find_element_by_css_selector('%scpm' % form).clear()
        driver.find_element_by_css_selector('%scpm' % form).send_keys("aa")
        driver.find_element_by_css_selector('%sbudget' % form).clear()
        driver.find_element_by_css_selector('%sbudget' % form).send_keys("aa")
        driver.find_element_by_css_selector('%sphone' % form).clear()
        driver.find_element_by_css_selector('%sphone' % form).send_keys("aa")
        driver.find_element_by_css_selector('%s> div > div > div.modal-footer.col-md-12 > button' % modal).click()
        sleep(1)
        self.assertEqual('Enter a valid budget. Maximum allowed decimals: 2',
                         driver.find_element_by_css_selector('%s > div:nth-child(7) > span' % form2).text, msg=None)
        path = "clients/client/screenshot/test_data_type_%s" % form
        screenshot(self, path)
        sleep(3)

    def test_format_email(self):
        driver = self.driver
        form, form2, modal = self.function_type(_type)
        path = "clients/client/screenshot/test_format_email_%s" % form
        sleep(5)
        driver.find_element_by_css_selector('%semail' % form).clear()
        driver.find_element_by_css_selector('%scpm' % form).clear()
        driver.find_element_by_css_selector('%sbudget' % form).clear()
        driver.find_element_by_css_selector('%sphone' % form).clear()
        driver.find_element_by_css_selector('%semail' % form).send_keys("sonia.amezcua")
        driver.find_element_by_css_selector('%s> div > div > div.modal-footer.col-md-12 > button' % modal).click()
        sleep(1)
        self.assertEqual('Enter valid email',
                         driver.find_element_by_css_selector('%s > div:nth-child(2) > span' % form2).text, msg=None)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_css_selector('%semail' % form).clear()
        driver.find_element_by_css_selector('%semail' % form).send_keys("sonia.amezcua@")
        driver.find_element_by_css_selector('%s> div > div > div.modal-footer.col-md-12 > button' % modal).click()
        sleep(1)
        self.assertEqual('Enter valid email',
                         driver.find_element_by_css_selector('%s > div:nth-child(2) > span' % form2).text, msg=None)
        screenshot(self, path)
        # sleep(1)
        # driver.find_element_by_css_selector('%semail' % form).clear()
        # driver.find_element_by_css_selector('%semail' % form).send_keys("sonia.amezcua@varangard")
        # driver.find_element_by_css_selector('%s> div > div > div.modal-footer.col-md-12 > button' % modal).click()
        # sleep(1)
        # self.assertEqual('Enter valid email',
        #                  driver.find_element_by_css_selector('%s > div:nth-child(2) > span' % form2).text, msg=None)
        sleep(5)
        screenshot(self, path)

    def test_max_min(self):
        driver = self.driver
        form, form2, modal = self.function_type(_type)
        path = "clients/client/screenshot/test_max_min_%s" % form
        sleep(5)
        driver.find_element_by_css_selector('%sbudget' % form).clear()
        driver.find_element_by_css_selector('%sbudget' % form).send_keys("-0.01")
        driver.find_element_by_css_selector('%s> div > div > div.modal-footer.col-md-12 > button' % modal).click()
        sleep(1)
        self.assertEqual('Enter a valid budget. Maximum allowed decimals: 2',
                         driver.find_element_by_css_selector('%s > div:nth-child(7) > span' % form2).text, msg=None)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_css_selector('%sbudget' % form).clear()
        driver.find_element_by_css_selector('%sbudget ' % form).send_keys("999999999999999999.99")
        driver.find_element_by_css_selector('%s> div > div > div.modal-footer.col-md-12 > button' % modal).click()
        sleep(1)
        self.assertEqual('Enter a valid budget. Maximum allowed decimals: 2',
                         driver.find_element_by_css_selector('%s > div:nth-child(7) > span' % form2).text, msg=None)
        sleep(3)
        screenshot(self, path)

    def test_format_rfc(self):
        driver = self.driver
        form, form2, modal = self.function_type(_type)
        path = "clients/client/screenshot/test_format_rfc_%s" % form
        sleep(8)
        # driver.find_element_by_css_selector('%srfc' % form).clear()
        # driver.find_element_by_css_selector('%srfc' % form).send_keys("AEAS850120H3A2")
        # driver.find_element_by_css_selector('%s> div > div > div.modal-footer.col-md-12 > button' % modal).click()
        # sleep(1)
        # self.assertEqual('Enter valid RFC',
        #                  driver.find_element_by_css_selector('%s > div:nth-child(9) > span' % form2).text, msg=None)
        # screenshot(self, path)
        # sleep(1)
        driver.find_element_by_css_selector('%srfc' % form).clear()
        driver.find_element_by_css_selector('%srfc' % form).send_keys("AEA850120H3A2")
        driver.find_element_by_css_selector('%s> div > div > div.modal-footer.col-md-12 > button' % modal).click()
        sleep(1)
        self.assertEqual('Enter valid RFC',
                         driver.find_element_by_css_selector('%s > div:nth-child(9) > span' % form2).text, msg=None)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_css_selector('%srfc' % form).clear()
        driver.find_element_by_css_selector('%srfc' % form).send_keys("AEAS8R0120H3A")
        driver.find_element_by_css_selector('%s> div > div > div.modal-footer.col-md-12 > button' % modal).click()
        sleep(1)
        self.assertEqual('Enter valid RFC',
                         driver.find_element_by_css_selector('%s > div:nth-child(9) > span' % form2).text, msg=None)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_css_selector('%srfc' % form).clear()
        driver.find_element_by_css_selector('%srfc' % form).send_keys("AAS8R0120H3A")
        driver.find_element_by_css_selector('%s> div > div > div.modal-footer.col-md-12 > button' % modal).click()
        sleep(1)
        self.assertEqual('Enter valid RFC',
                         driver.find_element_by_css_selector('%s > div:nth-child(9) > span' % form2).text, msg=None)
        screenshot(self, path)
        sleep(1)
        driver.find_element_by_css_selector('%srfc' % form).clear()
        driver.find_element_by_css_selector('%srfc' % form).send_keys("A#AS850120H3A")
        driver.find_element_by_css_selector('%s> div > div > div.modal-footer.col-md-12 > button' % modal).click()
        sleep(1)
        self.assertEqual('Enter valid RFC',
                         driver.find_element_by_css_selector('%s > div:nth-child(9) > span' % form2).text, msg=None)
        sleep(4)
        screenshot(self, path)

    @classmethod
    def tearDownClass(cls):
        logout(cls)
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
