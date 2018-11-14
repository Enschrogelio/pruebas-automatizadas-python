import datetime
import random
import string

import psycopg2
from util.config import ModelConfig
from time import *



def db_functions(code):
    conn = None
    valor=""
    try:
        conn = psycopg2.connect(ModelConfig.connection)
        cur = conn.cursor()
        exec(code)
        valor = cur.fetchmany()
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            return valor

def login(self):
    driver = self.driver
    #login
    driver.get(ModelConfig.url_login)
    driver.find_element_by_xpath('//*[@id="id_username"]').send_keys(ModelConfig.email)
    driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(ModelConfig.password)
    driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()

def logout(self):
    sleep(5)
    driver = self.driver
    driver.get(ModelConfig.base_url+"/admin/login")
    sleep(1)
    driver.find_element_by_xpath('//a[@href="/admin/logout/"]').click()
    sleep(2)



def screenshot(self,ruta):
    driver = self.driver
    now = datetime.datetime.now()
    hour = now.hour
    min = now.min
    second = now.second
    today = datetime.date.today()
    driver.save_screenshot(ModelConfig.base_screenshot+ruta+"%s-hora-%s-seg_%s.png" %(today, hour, second))
    return ruta

def randoms(long, tipo):
    dato = ""
    if tipo == "letter":
        letters = [chr(random.randint(97, 122)) for _ in range(long)]
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
