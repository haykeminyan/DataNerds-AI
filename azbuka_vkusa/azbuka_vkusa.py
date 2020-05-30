# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time
from fake_useragent import UserAgent
import logging
import datetime
from pymongo import MongoClient

href_addr = 'https://av.ru/'
client = MongoClient('localhost', 27017)
db = client.shop_prices
final_azbuka_vkusa = db.final_azbuka_vkusa

logging.basicConfig(filename="azbuka_vkusa.log", format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filemode='w', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)
ua = UserAgent()
headers = {'User-Agent': str(ua.chrome)}


def switcher(href_addr):
    while True:
        try:
            ip = requests.get(href_addr, headers=headers, timeout=10).content
            break
        except Exception as errors:
            logging.error('{}'.format(errors))
            continue
    return ip


main_page = switcher(href_addr)
main_soup = BeautifulSoup(main_page, 'html.parser')
heading_1 = list(main_soup.find_all(
    class_='b-header-menu__level-item js-show-menu b-header-menu__level-item_empty'))
heading_2 = list(main_soup.find_all(
    class_='b-header-menu__level-item js-show-menu'))
arr_1_names = []
arr_1_href = []
arr_2_names = []
arr_2_href = []
for i in heading_1:
    for j in i.find_all(class_='b-header-menu__level-link js-menu-link'):
        arr_1_names.append(j.text.strip().replace('.', ','))
        arr_1_href.append('https://av.ru'+j.get('href'))
for i in heading_2:
    for j in i.find_all(class_='b-header-menu__level-link js-menu-link'):
        arr_2_names.append(j.text.strip().replace('.', ','))
        arr_2_href.append('https://av.ru'+j.get('href'))
a = {}
arr_names = arr_1_names+arr_2_names
for i in range(len(arr_names)):
    k = arr_names[i]
    if k not in a:
        a[k] = 1
    else:
        arr_names[i] += '_'+str(a[k])
        a[k] += 1
        logging.info(
            '--------------------------------------------------------------------------------------------------')
        logging.error('We have similar {} name_category {} '.format(a[k], k))
        logging.info(
            '--------------------------------------------------------------------------------------------------')
arr_href = arr_1_href+arr_2_href
logging.info('We have to parse {} hrefs'.format(len(arr_names)))
arr_href.remove('https://av.ruhttps://av.ru/lp/elektronnye-podarochnie-karti/')
arr_names.remove('Подарочные карты')
dict_name_href = dict(zip(arr_names, arr_href))


def parsing_single_html(href_addr):
    arr_items = {}
    res = {}
    azbuka_page = switcher(href_addr)
    azbuka_soup = BeautifulSoup(azbuka_page, 'html.parser')
    pages = []
    pages_heading = list(azbuka_soup.find_all(class_='b-pager__list'))
    for i in pages_heading:
        pages = i.text.strip().split('\n')[-1]
    try:
        pages = int(pages)
    except:
        pages = 1
    for i in range(pages):
        html_addr = href_addr + \
            '?q=%3Aacbestseller%3AassortmentTypes%3AINTERNET&page='+str(i)
        html_page = switcher(html_addr)
        azbuka_soup_1 = BeautifulSoup(html_page, 'html.parser')
        arr_names = []
        heading_names = list(azbuka_soup_1.find_all(
            class_='b-product__title js-list-prod-open'))
        for a in heading_names:
            arr_names.append(a.text.strip().replace('.', ','))
        a = {}
        for b in range(len(arr_names)):
            k = arr_names[b]
            if k not in a:
                a[k] = 1
            else:
                arr_names[b] += '_'+str(a[k])
                a[k] += 1
                logging.info(
                    '--------------------------------------------------------------------------------------------------')
                logging.error(
                    'We have similar {:<3} name_goods={} in {} page!'.format(a[k], k, i+1))
                logging.info(
                    '--------------------------------------------------------------------------------------------------')
        heading_price = list(azbuka_soup_1.find_all(
            class_='b-product__price-block'))
        arr_price_with_and_without_discount = []
        for c in heading_price:
            for d in c.find_all(True, {'class': ['b-product__price b-price b-price_product', 'b-product__price b-price b-price_product b-price_product-red']}):
                arr_price_with_and_without_discount.append(
                    float(d.get('content').replace('\xa0', '')))
        arr_items = dict(zip(arr_names, arr_price_with_and_without_discount))
        res = {**res, **arr_items}
    logging.info(
        '--------------------------------------------------------------------------------------------------')
    logging.info('#Pages: {:<11} href_addr: {:<11} counter_goods: {:<11}'.format(
        pages, href_addr, len(res)))
    return res


date = datetime.datetime.now().strftime("%d-%m-%Y")
final_azbuka_vkusa = {}
counter = 1
f = open('result.txt', 'w')
for i, j in dict_name_href.items():
    final_azbuka_vkusa[i] = {'link': j, date: parsing_single_html(j)}
    db.final_azbuka_vkusa.insert_one({i: final_azbuka_vkusa[i]})
    logging.info('Counter:{:<11} Category name: {:<11}'.format(counter, i))
    logging.info(
        '--------------------------------------------------------------------------------------------------')
    counter += 1
    f.write(str(final_azbuka_vkusa[i]))
