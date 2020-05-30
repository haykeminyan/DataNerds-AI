# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import itertools
from pymongo import MongoClient
import datetime
import re
import logging
from itertools import cycle

client = MongoClient('localhost', 27017)
db = client.tekh
final_3 = db.final_3
href_addr = 'https://время-техники.com/product_list'


def switcher(href_addr):
    while True:
        try:
            ip = requests.get(href_addr, timeout=20).text
            break
        except Exception as errors:
            print('Error! {0}'.format(errors))
            continue
    return ip


logging.basicConfig(filename="tekh.log", format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filemode='w', level=logging.INFO)
tekh_main_page = switcher(href_addr)
tekh_main_soup = BeautifulSoup(tekh_main_page, 'html.parser')
tekh_main_heading = tekh_main_soup.find_all(
    class_='cs-product-groups-gallery__image-link')
arr_names = []
arr_href = []
for i in tekh_main_heading:
    arr_names.append(i.get('title'))
for i in tekh_main_heading:
    arr_href.append('https://время-техники.com'+i.get('href'))
arr_names_href_level = {}
arr_names_href_1_level = dict(zip(arr_names, arr_href))
f = open('cost.txt', 'w')
logging.info('Welcome to my parser! I hope you will enjoy it!')
logging.info(
    'The length of names 1 level Category is: {}'.format(len(arr_names)))
logging.info('The length of href 1 level Category is: {}'.format(len(arr_href)))
logging.info('Here is the first dictionary: {}'.format(arr_names_href_1_level))


def parse_single_html(href_addr):
    res = {}
    counter = 1
    tekh_main_page = switcher(href_addr)
    tekh_main_soup = BeautifulSoup(tekh_main_page, 'html.parser')
    tekh_heading = tekh_main_soup.find_all(class_='b-pager__link')
    pages_bad = []
    for i in tekh_heading:
        j = i.text.strip()
        pages_bad.append(j)
    pages_very_bad = []
    pages_very_bad = pages_bad[::-1]
    pages = []
    try:
        pages.append(pages_very_bad[1])
    except Exception as errors:
        pages.append(1)
        print('Specialize page! {}'.format(errors))
    for i in pages:
        page = int(i)
        print(page)
    for i in range(1, page+1):
        html_href = href_addr+'/page_'+str(i)+'#'
        print(html_href)
        html_page = switcher(html_href)
        tekh_soup = BeautifulSoup(html_page, 'html.parser')
        tekh_names = tekh_soup.find_all(class_='cs-goods-title')
        arr_names = []
        for a in tekh_names:
            b = a.text.strip()
            arr_names.append(b.replace('.', ','))
        tekh_price = tekh_soup.find_all(
            class_='cs-goods-price__value cs-goods-price__value_type_current')
        arr_price_bad = []
        for c in tekh_price:
            d = c.text.strip()
            j = d.split('\xa0')
            arr_price_bad.append(j)
        arr_price_bad_bad_1 = []
        arr_price_bad_bad_2 = []
        for h in arr_price_bad:
            arr_price_bad_bad_1.append(h[0].replace('руб.', ' '))
        for g in arr_price_bad:
            arr_price_bad_bad_2.append(g[1].replace('руб.', ' '))
        arr_price_not_bad = []
        for k, l in zip(arr_price_bad_bad_1, arr_price_bad_bad_2):
            arr_price_not_bad.append(k+l)
        arr_price = []
        for i in arr_price_not_bad:
            j = int(i)
            arr_price.append(j)
        print(arr_price)
        f.write(str(arr_price))
        arr_names_price = {}
        arr_names_price = dict(zip(arr_names, arr_price))
        res = {**res, **arr_names_price}
        counter += 1
    logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
    logging.info('{:<11} #Pages: {:<11}  #Goods:{:<11}'.format(
        str(href_addr), str(page), str(len(res))))
    return res


date = datetime.datetime.now().strftime("%d-%m-%Y")
counter_2 = 1
dict_1 = {}


for i, j in arr_names_href_1_level.items():
    arr_names = []
    arr_href = []
    html_level = switcher(j)
    html_soup = BeautifulSoup(html_level, 'html.parser')
    html_heading = html_soup.find_all(
        class_='cs-product-groups-gallery__image-link')
    for s in html_heading:
        arr_names.append(s.get('title'))
        arr_href.append('https://время-техники.com'+s.get('href'))
    dict_1[i] = dict(zip(arr_names, arr_href))
logging.info('Here is the second dictionary: {}'.format(dict_1))
g = open('final_tekh.txt', 'w')

final_3 = {}
for i, j in dict_1.items():
    final_vremya = {}
    for k, m in j.items():
        final_3 = {}
        final_vremya[k] = {'link': m, date: parse_single_html(m)}
        final_3 = {**final_3, **final_vremya}
        logging.info('#Category_2_name:  {:<11} Counter_2_level: {:<11} #href_2_level:{:<11}'.format(
            str(k), str(counter_2), str(m)))
        counter_2 += 1
    db.final_3.insert_one({i: final_3})
    g.write(str(final_3))
logging.info('Parsing is finished!')
