# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import requests
from fake_useragent import UserAgent
import os
import datetime
from fake_useragent import UserAgent
import pandas as pd
import logging
from datetime import datetime
import schedule
import time

logging.basicConfig(filename="currency_log_for_current_day.log", format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filemode='w', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)

current_date = datetime.today().strftime("%d.%m.%Y")
href_addr = 'http://www.cbr.ru/hd_base/metall/metall_base_new/?UniDbQuery.Posted=True&UniDbQuery.Gold=true&UniDbQuery.Silver=true&UniDbQuery.Platinum=true&UniDbQuery.Palladium=true&UniDbQuery.FromDate=&UniDbQuery.ToDate='
directory = os.path.abspath(os.getcwd())
folder_name = 'current_day_metalls'
if not os.path.exists(folder_name):
    os.mkdir(folder_name)
    logging.info("Directory {} created".format(folder_name))
else:
    logging.info("Directory {} already exists".format(folder_name))


def switcher(href_addr):
    while True:
        try:
            ip = requests.get(href_addr, timeout=10).content
            break
        except Exception as errors:
            print(errors)
            continue
    return ip


main_page = switcher(href_addr)
main_soup = BeautifulSoup(main_page, 'html.parser')
table = list(main_soup.find_all(class_='data'))

columns = 3
a = list(main_soup.select('.table'))
for i in a:
    j = i.text.strip()
    k = j.split('\n')
k = [i for i in k if i]

new = []
for i in range(0, len(k)-1, columns):
    new.append(k[i: i+columns])

current_date = str(new[1][2])


href_addr_current_date = 'http://www.cbr.ru/hd_base/metall/metall_base_new/?UniDbQuery.Posted=True&UniDbQuery.Gold=true&UniDbQuery.Silver=true&UniDbQuery.Platinum=true&UniDbQuery.Palladium=true&UniDbQuery.FromDate=' + \
    current_date+'&UniDbQuery.ToDate='+current_date
print(href_addr_current_date)


def switcher_current_date(href_addr_current_date):
    while True:
        try:
            ip = requests.get(href_addr_current_date, timeout=10).content
            break
        except Exception as errors:
            print(errors)
            continue
    return ip


main_page_current = switcher_current_date(href_addr_current_date)
main_soup_current = BeautifulSoup(main_page_current, 'html.parser')
table_current = list(main_soup_current.find_all(class_='data'))

columns_1 = 5
a_current = list(main_soup_current.select('.table'))
for i in a_current:
    j = i.text.strip()
    k_current = j.split('\n')
k_current = [i for i in k_current if i]

new_current = []
for i in range(0, len(k_current)-1, columns_1):
    new_current.append(k_current[i: i+columns_1])


df = pd.DataFrame.from_records(new_current)
print(df)
df.to_csv(os.path.join(directory+'/'+folder_name, current_date+'.csv'))
