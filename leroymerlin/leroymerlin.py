# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import requests
import logging
import datetime
from pymongo import MongoClient
href_addr = 'https://leroymerlin.ru/catalogue/'
client = MongoClient('localhost', 27017)
db = client.shop_leroy
final_2 = db.final_2


def switcher(href_addr):
    while True:
        try:
            ip = requests.get(href_addr, timeout=20).text
            break
        except Exception as errors:
            print('Error:{0}'.format(errors))
            continue
    return ip


logging.basicConfig(filename="leroymerlin.log", format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filemode='w', level=logging.INFO)

leroy_main_page = switcher(href_addr)
leroy_main_soup = BeautifulSoup(leroy_main_page, 'html.parser')
leroy_heading = leroy_main_soup.find_all(class_='leftmenu-small')

arr_names_1_level_very_bad = []
for i in leroy_heading:
    j = i.text.strip()
    k = j.split('\n')
    arr_names_1_level_very_bad.append(k)
arr_names_1_level_bad = []
for i in arr_names_1_level_very_bad:
    for j in i:
        arr_names_1_level_bad.append(j)
arr_names_1_level_bad = [x for x in arr_names_1_level_bad if x]
arr_names_1_level = []
for i in arr_names_1_level_bad:
    j = " ".join(i.split())
    arr_names_1_level.append(j)
arr_names_1_level = [x for x in arr_names_1_level if x]

arr_href_1_level_bad = []
arr_href_1_level = []
for n in leroy_heading:
    for a in n.find_all('a', href=True):
        arr_href_1_level_bad.append(a['href'])
for i in arr_href_1_level_bad:
    j = 'https://leroymerlin.ru'+str(i)
    arr_href_1_level.append(j)
arr_names_href_0_level = {}
arr_names_href_0_level = dict(zip(arr_names_1_level, arr_href_1_level))
print(arr_names_href_0_level)


def parse_single_html(href_addr):
    res = {}
    counter = 0
    leroy_main_page_1 = switcher(href_addr)
    leroy_main_soup_1 = BeautifulSoup(leroy_main_page_1, 'html.parser')
    leroy_main_count_pages_1 = leroy_main_soup_1.find_all(
        class_='paginator-item')
    arr_count_pages_bad = []
    arr_count_pages = []
    for i in leroy_main_count_pages_1:
        j = i.get('data-page')
        arr_count_pages_bad.append(j)
    try:
        arr_count_pages.append(arr_count_pages_bad[::-1][0])
        print(arr_count_pages)
    except Exception as errors:
        arr_count_pages.append(1)
        print('This page has only 1 page: {0}'.format(errors))
    for i in arr_count_pages:
        page = int(i)
    for i in range(1, page+1):
        html_href = href_addr+'?sortby=8&page='+str(i)
        print(html_href)
        html_page = switcher(html_href)
        leroy = BeautifulSoup(html_page, 'html.parser')
        leroy_main_names = leroy.find_all(class_='product-name')
        arr_names = []
        for a in leroy_main_names:
            j = a.text.strip()
            arr_names.append(j.replace('.', ','))
        arr_cost_bad = []
        arr_cost = []
        leroy_main_cost = leroy_main_soup_1.find_all(class_='main-value-part')
        for b in leroy_main_cost:
            arr_cost_bad.append(b.get('content').replace(',', '.'))
        for c in arr_cost_bad:
            j = float(c.replace(' ', ''))
            arr_cost.append(j)
        arr_names_cost = {}
        arr_names_cost = dict(zip(arr_names, arr_cost))
        res = {**res, **arr_names_cost}
        counter += 1
    logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
    logging.info('{:<11} #Pages: {:<11}  #Goods:{:<11}'.format(
        str(href_addr), str(page), str(len(res))))
    return res


date = datetime.datetime.now().strftime("%d-%m-%Y")
counter_2 = 1
dict_1 = {}


for i, j in arr_names_href_0_level.items():
    arr_names = []
    arr_href_bad = []
    html_level = switcher(j)
    html_soup = BeautifulSoup(html_level, 'html.parser')
    html_heading = html_soup.find_all(
        class_='items-border section-card__items')
    for s in html_heading:
        for k in s.find_all(class_='section-card-text'):
            arr_names.append(k.text.strip())
        for h in s.find_all('a', href=True):
            arr_href_bad.append(h['href'])
    arr_href = []
    for a in arr_href_bad:
        j = 'https://leroymerlin.ru'+a
        arr_href.append(j)
    dict_1[i] = dict(zip(arr_names, arr_href))

g = open('final.txt', 'w')
final_2 = {}
for i, j in dict_1.items():
    final_leroy = {}
    for k, m in j.items():
        final_2 = {}
        final_leroy[k] = {'link': m, date: parse_single_html(m)}
        final_2 = {**final_2, **final_leroy}
        logging.info('#Category_2_name:  {:<11} Counter_2_level: {:<11} #href_2_level:{:<11}'.format(
            str(k), str(counter_2), str(m)))
        counter_2 += 1
    db.final_2.insert_one({i: final_2})
    g.write(str(final_2))
