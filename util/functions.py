import csv
from datetime import datetime
from time import sleep, strftime
import random
import string
import psycopg2
from util.config import ModelConfig


def login(self):
    driver = self.driver
    driver.get(ModelConfig.url_login)
    driver.find_element_by_xpath('//*[@id="id_username"]').send_keys(ModelConfig.email)
    driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(ModelConfig.password)
    driver.find_element_by_xpath('//*[@id="formLogin"]/button').click()
    sleep(2)
    
    
def logout(self):
    sleep(5)
    driver = self.driver
    driver.get(ModelConfig.url_login)
    sleep(1)
    driver.find_element_by_xpath('//a[@href="/admin/logout/"]').click()
    sleep(2)


def screenshot(self, path):
    driver = self.driver
    now = datetime.now().strftime("%Y-%m-%d %H;%M;%S")
    driver.save_screenshot(ModelConfig.base_screenshot+path+" %s.png" % now)


def randoms(long, _type):
    _data = ""
    if _type == "letter":
        letters = [chr(random.randint(97, 122)) for r in range(long)]
        _data = ''.join(letters)
    else:
        if _type == "number":
            numbers = [str(random.randint(0, 9)) for r in range(long)]
            _data = ''.join(numbers)
        else:
            if _type == "alpha":
                alpha = [random.choice(string.ascii_letters + string.digits) for r in range(long)]
                _data = ''.join(alpha)
            else:
                if _type == "special":
                    specials = [random.choice(string.punctuation) for r in range(long)]
                    _data = ''.join(specials)
    return _data


# DB functions
# noinspection PyUnresolvedReferences
def db_functions(code):
    conn = None
    try:
        conn = psycopg2.connect(ModelConfig.connection)
        cur = conn.cursor()
        exec(code)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# Read csv
def read_csv(root):
    csv_list = []
    print(root)
    with open(root, newline='') as csv_file:
        reader = csv.reader(csv_file)
        title = reader.__next__()
        for row in reader:
            list_csv = {}
            for column in range(len(title)):
                list_csv[title[column]] = row[column]
            csv_list.append(list_csv)
    return csv_list
