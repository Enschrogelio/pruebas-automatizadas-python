import csv
from datetime import datetime
from time import sleep
import random
import string
import psycopg2
from util.config import modelConfig

#login
def login(self):
    driver = self.driver
    #login
    driver.get(modelConfig.base_url+"/admin/login")
    driver.find_element_by_xpath('//*[@id="id_username"]').send_keys(modelConfig.email)
    driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(modelConfig.password)
    driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()
    sleep(2)

#logout
def logout(self):
    sleep(5)
    driver=self.driver
    driver.get(modelConfig.base_url+"/admin/login")
    sleep(1)
    driver.find_element_by_xpath('//a[@href="/admin/logout/"]').click()
    sleep(2)

#Screenshot
def screenshot(self,ruta):
    driver = self.driver
    now = datetime.now().strftime("%Y-%m-%d %H;%M;%S")
    driver.save_screenshot(modelConfig.base_screenshot+ruta+" %s.png" % now)

#Randoms
def randoms(long,tipo):
    dato = ""
    if tipo == "letter":
        letters = [chr(random.randint(97, 122)) for r in range(long)]
        dato = ''.join(letters)
    else:
        if tipo == "number":
            numbers = [str(random.randint(0, 9)) for r in range(long)]
            dato = ''.join(numbers)
        else:
            if tipo == "alpha":
                alpha = [random.choice(string.ascii_letters + string.digits) for r in range(long)]
                dato = ''.join(alpha)
            else:
                if tipo == "special":
                    specials = [random.choice(string.punctuation) for r in range(long)]
                    dato = ''.join(specials)
    return dato

#DB functions
# noinspection PyUnresolvedReferences
def db_functions(code):
    conn=None
    try:
        conn = psycopg2.connect(modelConfig.connection)
        cur = conn.cursor()
        exec(code)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

#Read csv
def read_csv(root):
    csv_list = []
    print(root)
    with open(root, newline='') as csvfile:
        reader = csv.reader(csvfile)
        title = reader.__next__()
        for row in reader:
            listcsv = {}
            for column in range(len(title)):
                listcsv[title[column]] = row[column]
            csv_list.append(listcsv)
    return csv_list
