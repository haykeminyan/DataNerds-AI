# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.common.keys import Keys
from itertools import cycle
from fake_useragent import UserAgent
from collections import Counter
import shutil
import os
import pandas as pd
import logging
from selenium.webdriver.support.ui import Select
import ssl
import datetime
from pymongo import MongoClient


href_addr = 'https://dixy.ru/catalog/'
client = MongoClient('localhost', 27017)
db = client.shop_prices
final_dixy = db.final_dixy

browser = webdriver.Chrome()
browser.get(href_addr)
# browser.maximize_window()
logging.basicConfig(filename="dixy.log", format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filemode='w', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)

ua = UserAgent()
headers = {'User-Agent': str(ua.random)}


def switcher(href_addr):
    while True:
        try:
            ip = requests.get(href_addr, headers=headers, timeout=10).content
            break
        except Exception as errors:
            logging.error('{}'.format(str(errors)))
            continue
    return ip


SCROLL_PAUSE_TIME = 3


def clicker(href_addr):
    while True:
        try:
            last_height = browser.execute_script(
                "return document.body.scrollHeight")
            WebDriverWait(browser, 15).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.btn'))).click()
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = browser.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        except TimeoutException:
            break
    return browser.page_source


main_page = switcher(href_addr)
main_soup = BeautifulSoup(main_page, 'html.parser')
category_heading = list(main_soup.find_all(class_='common'))
hrefs_bad = []
category_bad = []
for i in category_heading:
    for j in i.find_all(class_=''):
        hrefs_bad.append(j.get('data-code'))
        category_bad.append(j.text.strip().replace('.', ','))
href = []
for i in hrefs_bad:
    if i != None:
        href.append('https://dixy.ru/catalog/'+i)
category = []
for i in category_bad:
    if i not in category:
        category.append(i)
dict_0 = {}
for i in range(len(category)):
    k = category[i]
if k not in dict_0:
    dict_0[k] = 1
else:
    category[i] += '_'+str(dict_0[k])

dict_main = {}
dict_main = dict(zip(category, href))
logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
logging.info('We have to parse: {} categories'.format(len(category)))


def parsing_single_html(href_addr):
    res = {}
    main_soup = BeautifulSoup(clicker(href_addr), 'html.parser')
    # main_page=switcher(href_addr)
    # main_soup=BeautifulSoup(main_page,'html.parser')
    arr_names = []
    arr_names_bad = []
    arr_cost = []
    goods_heading = list(main_soup.find_all(
        True, {'class': ['item', 'item more']}))
    for i in goods_heading:
        for j in i.find_all(class_='product'):
            for k in j.find_all(class_='preview'):
                arr_names_bad.append(k.get('alt').replace('.', ','))
        for a in i.find_all(itemprop="price"):
            arr_cost.append(float(a.get('content')))
    for i in arr_names_bad:
        try:
            arr_names.append(i.split('\xa0')[0].replace(
                '...', ',')+i.split('\xa0')[1].replace('...', ','))
        except:
            arr_names.append(i.split('\xa0')[0].replace('...', ','))
    dict_1 = {}
    for i in range(len(arr_names)):
        z = arr_names[i]
        if z not in dict_1:
            dict_1[z] = 1
        else:
            arr_names[i] += '_'+str(dict_1[z])
            logging.info(
                '--------------------------------------------------------------------------------------------------------------------------------------------------')
            logging.info(
                'We have similar goods {} <<name={}>> !!!!!!!!!!!!!'.format(dict_1[k], k))
            logging.info(
                '--------------------------------------------------------------------------------------------------------------------------------------------------')
    dict_main = {}
    dict_main = dict(zip(arr_names, arr_cost))
    res = {**res, **dict_main}
    logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
    logging.info('{:<11} #Goods:{:<11}'.format(str(href_addr), str(len(res))))
    print(res)
    print('----------------------------')
    print(len(arr_names))
    print(len(arr_cost))
    print('--------------------------------')
    return res


# print(parsing_single_html('https://dixy.ru/catalog/krasota/'))
date = datetime.datetime.now().strftime("%d-%m-%Y")
counter_category = 1
final_dixy = {}
f = open('result.txt', 'w')
for i, j in dict_main.items():
    browser.get(j)
    clicker(j)
    final_dixy[i] = {'link': j, date: parsing_single_html(j)}
    logging.info('Counter_category: {} '.format(counter_category))
    logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
    counter_category += 1
    db.final_dixy.insert_one({i: final_dixy[i]})
    f.write(str(final_dixy[i]))
