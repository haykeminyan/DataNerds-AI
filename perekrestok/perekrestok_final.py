# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import itertools
from pymongo import MongoClient
import datetime
import re
import logging
from itertools import cycle

client = MongoClient('192.168.149.192', 27017)
db = client.shop_prices
final_perekrestok = db.final_perekrestok

href_addr = 'https://www.perekrestok.ru/catalog/'
user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36']


logging.basicConfig(filename="/Users/datanerds/workspace/perekrestok/perekrestok_2.log",
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filemode='w', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)

user_agent_list_pool = cycle(user_agent_list)


def switcher(href_addr):
    while True:
        try:
            ip = requests.get(href_addr, timeout=20).text
            break
        except Exception as errors:
            # print('Ошибка:\n', errors)
            logging.exception('Connection error!  {}'.format(errors))
            continue
    return ip


perekrestok_main_page = switcher(href_addr)
perekrestok_main_soup = BeautifulSoup(perekrestok_main_page, 'html.parser')
perekrestok_heading_1_catogories = perekrestok_main_soup.find_all(
    class_='xf-catalog-categories__list _list')
arr = []
for i in perekrestok_heading_1_catogories:
    j = i.text.strip().split('\n')
    arr.append(j)
arr_1 = []
for i in arr:
    for j in i:
        arr_1.append(j)
arr_name_submenu = []
arr_1 = [x for x in arr_1 if x]
arr_name_category_1_level = arr_1
arr_href_category_1 = []

arr_href_category_1_level = []
for n in perekrestok_heading_1_catogories:
    for a in n.find_all('a', href=True):
        arr_href_category_1.append(a['href'])
for i in arr_href_category_1:
    arr_href_category_1_level.append('https://www.perekrestok.ru'+i)
arr_name_href_1_level = {}
arr_name_href_1_level = dict(
    zip(arr_name_category_1_level, arr_href_category_1_level))
print(arr_name_href_1_level)

logging.info('The length of array with categories_names 1 level is: ' +
             str(len(arr_name_category_1_level)))
logging.info('The length of array with categories_href 1 level is: ' +
             str(len(arr_href_category_1_level)))


logging.info('Category: {:<11}'.format(str(arr_name_category_1_level)))


def parse_single_html(href_addr):
    res_1 = {}
    counter = 0
    number_of_goods_2_category = []
    number_of_goods_very_bad_2_category = []
    number_of_goods_bad_2_category = []
    arr_2 = []
    html_goods_2 = switcher(href_addr)
    html_goods_2_soup = BeautifulSoup(html_goods_2, 'html.parser')
    html_goods_2_heading = html_goods_2_soup.find_all(
        class_='js-list-total__total-count')
    arr_2.append(html_goods_2_heading)
    for i in arr_2:
        if i == []:
            number_of_goods_very_bad_2_category.append('0')
        else:
            number_of_goods_very_bad_2_category.append(i)
    for i in number_of_goods_very_bad_2_category:
        for j in i:
            if j != str(j):
                number_of_goods_bad_2_category.append(j.text.strip())
            else:
                number_of_goods_bad_2_category.append(j)
    for i in number_of_goods_bad_2_category:
        j = int(i)
        number_of_goods_2_category.append(j)
    for i in number_of_goods_2_category:
        page = i//24+1
    for number in range(1, page+1):
        html_href = href_addr + '?page=' + str(number)+'&sort=rate_desc'
        print(html_href)
        html_page = switcher(html_href)
        arr_items = []
        soup_one = BeautifulSoup(html_page, 'html.parser')
        id_items = soup_one.find_all(
            class_='catalog__items-wrap js-catalog-wrap')
        for a in id_items:
            for f in a.find_all(class_='xf-product js-product'):
                arr_items.append(
                    f.get('data-gtm-product-name').replace('.', ','))
        a = {}
        for c in range(len(arr_items)):
            k = arr_items[c]
            if k not in a:
                a[k] = 1
            else:
                arr_items[c] += '_'+str(a[k])
                a[k] += 1
                logging.info(
                    '--------------------------------------------------------------------------------------------------------------------------------------------------')
                logging.error('We have similar {} <<name={}>> in {}  page!!!!!!!!!!!!!'.format(
                    a[k], k, number))
        arr_rouble = []
        arr_penny = []
        arr_cost_bad = []
        for b in id_items:
            for q in b.find_all(class_='xf-product__cost xf-product-cost'):
                k = q.find(
                    class_='xf-price__rouble js-price-rouble').text.strip()
                arr_rouble.append(k)
                m = q.find(
                    class_='xf-price__penny js-price-penny').text.strip()
                arr_penny.append(m.replace(',', '.'))
        arr_cost = []
        for m, d in zip(arr_rouble, arr_penny):
            arr_cost_bad.append(m+d)
        for i in arr_cost_bad:
            arr_cost.append(float(i.replace(' ', '')))
        result_one = {}
        for key, value in zip(arr_items, arr_cost):
            result_one[key] = value
        res_1 = {**res_1, **result_one}
        counter += 1
        # logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
    logging.info('#Pages:{:<2} #Goods:{:<11}'.format(
        str(number), str(len(res_1))))
    return res_1


counter_1 = 1
date = datetime.datetime.now().strftime("%d-%m-%Y")

g = open('result_2_level.txt', 'w')
counter_2 = 1
dict_1 = {}
for i, j in arr_name_href_1_level.items():
    arr_href_category_2_level_without_https = []
    arr_href_category_2_level = []
    arr_name_category_2_level = []
    perekrestok_main_page_2_ = switcher(j)
    perekrestok_main_soup_2_ = BeautifulSoup(
        perekrestok_main_page_2_, 'html.parser')
    perekrestok_heading_2_catogories = perekrestok_main_soup_2_.find_all(
        class_='xf-filter__item-label xf-ripple js-xf-ripple xf-ripple_gray')
    for m in perekrestok_heading_2_catogories:
        k = m.text.strip()
        arr_name_category_2_level.append(k)
    for n in perekrestok_heading_2_catogories:
        arr_href_category_2_level_without_https.append(n.get('href'))
    for k in arr_href_category_2_level_without_https:
        h = 'https://www.perekrestok.ru'+k
        arr_href_category_2_level.append(h)
    dict_1[i] = dict(zip(arr_name_category_2_level, arr_href_category_2_level))

f = open('resul.txt', 'w')
final_perekrestok = {}
for i, j in dict_1.items():
    final_p = {}
    for k, m in j.items():
        final_p = {
            'link': m,
            'category_name': k,
            date: parse_single_html(m)
        }
        logging.info('#Category_2_name:  {:<11} Counter_2_level: {:<11} #href_2_level:{:<11}'.format(
            str(k), str(counter_2), str(m)))
        logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
        counter_2 += 1
        print(final_p)
        db.final_perekrestok.update_one({'category_name': k, 'link': m}, {
                                        '$set': {date: final_p[date]}}, upsert=True)
        g.write(str(final_perekrestok))
