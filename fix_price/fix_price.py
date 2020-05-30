# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import itertools
import re
from pymongo import MongoClient
import datetime
from collections import Counter
import logging
from itertools import cycle

client = MongoClient('localhost', 27017)
db = client.shop_fix_price
final_4 = db.final_4
href_addr = 'https://fix-price.ru/'


def switcher(href_addr):
    while True:
        try:
            ip = requests.get(href_addr, timeout=20).text
            break
        except Exception as errors:
            print('Error! {}'.format(errors))
            continue
    return ip


logging.basicConfig(filename="fix_price.log", format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filemode='w', level=logging.INFO)

logging.getLogger('requests').setLevel(logging.ERROR)
fix_price_main_page = switcher(href_addr)
fix_price_main_soup = BeautifulSoup(fix_price_main_page, 'html.parser')
fix_price_heading = fix_price_main_soup.find_all(class_='catalog-nav')

arr_names = []
arr_href = []
arr_names_href = {}
fix_1_level_page = switcher(href_addr)
fix_1_level_soup = BeautifulSoup(fix_1_level_page, 'html.parser')
fix_1_level_names = fix_1_level_soup.find_all(class_='catalog-sub__link')
for k in fix_1_level_names:
    d = k.text.strip()
    arr_names.append(d)
for m in fix_1_level_names:
    arr_href.append('https://fix-price.ru'+m.get('href'))

arr_names_href = dict(zip(arr_names, arr_href))
logging.info('Welcome to my parser! I hope you will enjoy it!')
logging.info(
    'The length of names 1 level Category is: {}'.format(len(arr_names)))
logging.info('The length of href 1 level Category is: {}'.format(len(arr_href)))
logging.info('Here is the first dictionary: {}'.format(arr_names_href))

g = open('res.txt', 'w')


def parse_single_html(href_addr):
    res = {}
    counter = 1
    fix = switcher(href_addr)
    fix_soup = BeautifulSoup(fix, 'html.parser')
    fix_pages_heading = fix_soup.find_all(class_='paging__item')
    fix_pages_bad = []
    for i in fix_pages_heading:
        j = i.text.strip()
        fix_pages_bad.append(j)
    # print(fix_pages_bad)
    fix_pages_bad = fix_pages_bad[::-1]
    try:
        page = int(fix_pages_bad[0])
    except Exception as errors:
        page = 1
        # print('We have only one page in this category:{}'.format(errors))
        logging.exception('{}'.format(errors))
    for i in range(1, page+1):
        html_addr = href_addr+'?set_filter=y&PAGEN_1='+str(i)
        html_page = switcher(html_addr)
        fix_soup_1 = BeautifulSoup(html_page, 'html.parser')
        fix_names_heading = fix_soup_1.find_all(class_='product-card__title')
        fix_names_bad = []
        for j in fix_names_heading:
            k = j.text.strip()
            fix_names_bad.append(k.replace('.', ','))
        # c = Counter()
        # print(fix_names)
        a = {}
        # fix_names=[]
        for c in range(len(fix_names_bad)):
            k = fix_names_bad[c]
            if k not in a:
                a[k] = 1
            else:
                fix_names_bad[c] += '_'+str(a[k])
                a[k] += 1
                logging.error(
                    'We have similar {} <<name={}>> in {}   page!!!!!!!!!!!!!'.format(a[k], k, i))
        # for key,value in c.items():
        #     if value>1:
        #         logging.warning('We have similar {} <<name={}>> in {}!!!!!!!!!!!!!'.format(value,key,i))
        #         for k in range(1,value+1):
        #             fix_names.append(key+'_'+str(k))
        #     else:
        #         fix_names.append(key)

        fix_cost_heading = fix_soup_1.find_all(class_='main-list__card-item')
        fix_cost = []
        fix_cost_bad = []
        for l in fix_cost_heading:
            for m in l.find_all(style='font-family: RotondaC-Bold;'):
                fix_cost_bad.append(m.text.strip())
        for z in fix_cost_bad:
            x = float(z.replace(',', '.'))
            fix_cost.append(x)
        fix_names_price = {}
        fix_names_price = dict(zip(fix_names_bad, fix_cost))
        print('-----------------')
        print(fix_names_price)
        print(len(fix_names_price))
        print(len(set(fix_names_price)))
        print(html_addr)
        print('-----------------')
        res = {**res, **fix_names_price}
        g.write(str(res))
        counter += 1
    # logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
    logging.info('{:<11} #Pages: {:<11}  #Goods:{:<11}'.format(
        str(href_addr), str(page), str(len(res))))
    logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
    return res


date = datetime.datetime.now().strftime("%d-%m-%Y")
final_4 = {}
counter = 1
f = open('final_fix.txt', 'w')
for i, j in arr_names_href.items():
    final_4[i] = {'link': j, date: parse_single_html(j)}
    db.final_4.insert_one({i: final_4[i]})
    logging.info('Counter:{}'.format(counter))
    counter += 1
    f.write(str(final_4[i]))
