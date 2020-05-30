from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import logging
import datetime
from pymongo import MongoClient
href_addr = 'https://msk.metro-cc.ru/'


client = MongoClient('localhost', 27017)
db = client.shop_prices
final_metro = db.final_metro

logging.basicConfig(filename="metro.log", format='%(asctime)s - %(message)s',
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
            # print(errors)
            logging.info('{}'.format(errors))
            continue
    return ip


main_page = switcher(href_addr)
main_soup = BeautifulSoup(main_page, 'html.parser')
main_heading = list(main_soup.find_all(class_='menu_col'))
category_name = []
href_1_level = []
for i in main_heading:
    for j in i.find_all(class_='child'):
        category_name.append(j.text.strip())
    for k in i.find_all('a', href=True):
        href_1_level.append(k['href'])
b = {}
for c in range(len(category_name)):
    k = category_name[c]
    if k not in b:
        b[k] = 1
    else:
        category_name[c] += '_'+str(b[k])
        b[k] += 1
        logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
        logging.error(
            'We have similar {} <<category_1_level={}>> !!!!!'.format(b[k], k))
dict_main_1_level = {}
dict_main_1_level = dict(zip(category_name, href_1_level))
logging.info('We have {} 1_categories'.format(len(category_name)))
dict_main_2_level = {}
for k, m in dict_main_1_level.items():
    main_page_two = switcher(m)
    main_soup_two = BeautifulSoup(main_page_two, 'html.parser')
    category_name_2_level = []
    href_2_level = []
    main_heading_2_level = list(
        main_soup_two.find_all(class_='subcatalog cat1'))
    for i in main_heading_2_level:
        category_name_2_level = list(filter(None, i.text.strip().split('\n')))
        for j in i.find_all(class_='subcatalog_link'):
            href_2_level.append('https://msk.metro-cc.ru'+j.get('href'))
    a = {}
    for c in range(len(category_name_2_level)):
        k = category_name_2_level[c]
        if k not in a:
            a[k] = 1
        else:
            category_name_2_level[c] += '_'+str(a[k])
            a[k] += 1
            logging.info(
                '--------------------------------------------------------------------------------------------------------------------------------------------------')
            logging.error(
                'We have similar {} <<category_2_level={}>> !!!!!!!!!!!!!'.format(a[k], k))
    dict_main_2_level[k] = dict(zip(category_name_2_level, href_2_level))


def parse_single_html(href_addr):
    result = {}
    main_page = switcher(href_addr)
    main_soup = BeautifulSoup(main_page, 'html.parser')
    pages_heading = list(main_soup.find_all(class_='pagination'))
    pages = []
    try:
        for i in pages_heading:
            pages.append(i.text.strip().split('...'))
        if len(pages[0]) == 2:
            pages = int(pages[0][-1])
        elif len(pages[0]) == 1:
            pages = int(pages[0][0][-1])
    except:
        pages = 1
    for page in range(1, pages+1):
        html_page = href_addr + \
            '?price_range=11%3B601&brands=&attrs=&attr[5163][from]=0&attr[5163][to]=0&sorting=0&limit=12&in_stock=0&virtual_stock=0&page='+str(
                page)
        print(html_page)
        main_page_goods = switcher(html_page)
        main_soup_goods = BeautifulSoup(main_page_goods, 'html.parser')
        goods_names_soup = list(
            main_soup_goods.find_all(class_='catalog-i_image'))
        goods_names = []
        goods_cost = []
        for k in goods_names_soup:
            for j in k.find_all('img', alt=True):
                goods_names.append(j['alt'].replace('.', ','))
        a = {}
        for c in range(len(goods_names)):
            k = goods_names[c]
            if k not in a:
                a[k] = 1
            else:
                goods_names[c] += '_'+str(a[k])
                a[k] += 1
                logging.info(
                    '--------------------------------------------------------------------------------------------------------------------------------------------------')
                logging.error(
                    'We have similar {} <<name={}>> in {}  page!!!!!!!!!!!!!'.format(a[k], k, page))
        goods_cost_soup = list(main_soup.find_all(class_='buttons'))

        # for i in goods_cost_soup:
        #     for k in i.find_all(class_='price'):
        #         try:
        #             goods_cost.append(float((list(filter(None,k.text.strip().split('\n')))[0]+'.'+list(filter(None,k.text.strip().split('\n')))[1]).replace(' ','')))
        #         except:
        #             goods_cost.append(float((list(filter(None,k.text.strip().split('\n')))[0]).replace(' ','')))
        for i in goods_cost_soup:
            for j in i.find_all(class_='add2list add-to-list'):
                goods_cost.append(float(j.get('data-regular_price')))
        # print(goods_names)
        # print(goods_cost)
        dict_goods = {}
        dict_goods = dict(zip(goods_names, goods_cost))
        result = {**result, **dict_goods}
    logging.info('{:<11} #Pages: {:<11}  #Goods:{:<11}'.format(
        str(href_addr), str(pages), str(len(result))))
    print(result)
    return result


# print(parse_single_html('https://msk.metro-cc.ru/category/remont/stroitelnye-materialy/taburety-stremyanki?price_range=11%3B601&brands=&attrs=&attr[5163][from]=0&attr[5163][to]=0&sorting=0&limit=12&in_stock=0&virtual_stock=0&page=1'))
date = datetime.datetime.now().strftime("%d-%m-%Y")
arr = []
dict_2 = {}
counter_2 = 1

g = open('res.txt', 'w')

for i, j in dict_main_2_level.items():
    final_m = {}
    for k, m in j.items():
        final_m = {
            'link': m,
            'category_name': k,
            date: parse_single_html(m)
        }
        logging.info('#Category_2_name:  {:<11} Counter_2_level: {:<11} #href_2_level:{:<11}'.format(
            str(k), str(counter_2), str(m)))
        logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
        counter_2 += 1
        db.final_metro.update_one({'category_name': k, 'link': m}, {
                                  '$set': {date: final_m[date]}}, upsert=True)
    g.write(str(final_metro))
