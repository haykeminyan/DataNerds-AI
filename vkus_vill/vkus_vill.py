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

logging.basicConfig(filename="vkus_vill.log", format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filemode='w', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)

ua = UserAgent()
headers = {'User-Agent': str(ua.random)}

href_addr = 'https://vkusvill.ru'
client = MongoClient('localhost', 27017)
db = client.shop_prices
final_vkus_vill = db.final_vkus_vill

browser = webdriver.Chrome()
browser.get(href_addr)
browser.maximize_window()


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
try:
    WebDriverWait(browser, 15).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'body > div.DeliveryAddressWhatsNew.js-DeliveryAddressWhatsNew > a > span'))).click()
except:
    pass


def clicker(href_addr):
    while True:
        try:
            last_height = browser.execute_script(
                "return document.body.scrollHeight")
            WebDriverWait(browser, 15).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '.Button--more'))).click()
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

category_soup = BeautifulSoup(main_page, 'html.parser')
category_heading = list(category_soup.find_all(
    class_='Header__subnavList Header__subnavList--main'))
categories = []
href = []
for i in category_heading:
    all_category_with_html_elem = i.find_all(class_='Header__subnavListItem')
for i in all_category_with_html_elem:
    categories.append(i.find(class_='Header__subnavLink').get(
        'title').replace('.', ','))
    href.append('https://vkusvill.ru' +
                i.find(class_='Header__subnavLink').get('href'))


dict_category_1_level = dict(zip(categories, href))
#!!!!!!!!!!!!!!!!!!
# goods_main_soup=BeautifulSoup(clicker(href_addr),'html.parser')
#!!!!!!!!!!!!!!!!!
# goods_main_soup=BeautifulSoup(main_page,'html.parser')


def parse_single_html(href_addr):
    res = {}
    goods_main_soup = BeautifulSoup(clicker(href_addr), 'html.parser')
    goods_names = []
    goods_names_html = list(goods_main_soup.find_all(
        class_='ProductCard__title H3'))
    for i in goods_names_html:
        goods_names.append(i.find(class_='ProductCard__link').get(
            'title').replace('.', ','))
    dict_1 = {}
    for i in range(len(goods_names)):
        k = goods_names[i]
        if k not in dict_1:
            dict_1[k] = 1
        else:
            goods_names[i] += '_'+str(dict_1[k])
        dict_1[k] += 1
        logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
        logging.info(
            'We have similar goods {} <<name={}>> !!!!!!!!!!!!!'.format(dict_1[k], k))
        logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
    goods_costs = []
    goods_costs_html = list(
        goods_main_soup.find_all(class_='ProductCard__price'))
    for j in goods_costs_html:
        goods_costs.append(float(j.find(class_='Price__value').get('content')))
    result = {}
    result = dict(zip(goods_names, goods_costs))
    res = {**res, **result}
    logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
    logging.info('{:<11} #Goods:{:<11}'.format(str(href_addr), str(len(res))))
    print(res)
    return res


date = datetime.datetime.now().strftime("%d-%m-%Y")

second_level_html = category_soup.find_all(class_='Header__subnavPopup')
href_2_level = []
categories_2_level = []
for a in second_level_html:
    for b in a.find_all(class_='Header__subnavLink'):
        href_2_level.append('https://vkusvill.ru'+b.get('href'))
        categories_2_level.append(b.get('title').replace('.', ','))
dict_2 = {}
counter_similar_categories = 0
for i in range(len(categories_2_level)):
    k = categories_2_level[i]
    if k not in dict_2:
        dict_2[k] = 1
    else:
        categories_2_level[i] += '_'+str(dict_2[k])
        dict_2[k] += 1
        counter_similar_categories += 1
        logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
        logging.error(
            'We have similar categories {} <<name={}>> !!!!!!!!!!!!!'.format(dict_2[k], k))
dict_final = dict(zip(categories_2_level, href_2_level))
logging.info('We have {} categories to parse'.format(len(categories_2_level)))

counter_category = 1
final_vkus_vill = {}
f = open('result.txt', 'w')
for i, j in dict_final.items():
    browser.get(j)
    clicker(j)
    final_vkus_vill[i] = {'link': j, date: parse_single_html(j)}
    logging.info('Counter_category: {} '.format(counter_category))
    logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
    counter_category += 1
    db.final_vkus_vill.insert_one({i: final_vkus_vill[i]})
    f.write(str(final_vkus_vill[i]))

logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
logging.error('All similar categories {} '.format(counter_similar_categories))
logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
