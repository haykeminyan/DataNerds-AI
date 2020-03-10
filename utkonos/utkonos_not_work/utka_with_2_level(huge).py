## -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import itertools
from pymongo import MongoClient
import datetime
import re
import string
from itertools import cycle
import traceback
from lxml.html import fromstring
import logging


href_addr='https://www.utkonos.ru/cat'
client = MongoClient('localhost', 27017)
db = client.test_utkonos_huge
final_utkonos_huge = db.final_utkonos_huge

user_agent_list=['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'Mozilla/5.0 (Linux; Android 6.0; MotoG3 Build/MPIS24.65-33.1-2-16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36', 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G610M Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Mobile Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36', 'Mozilla/5.0 (Linux; Android 4.4.2; de-de; SAMSUNG GT-I9301I Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36', 'Mozilla/5.0 (Linux; Android 6.0; vivo 1610 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.124 Mobile Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36', 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36', 'Mozilla/5.0 (X11; CrOS x86_64 12371.75.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.105 Safari/537.36', 'Mozilla/5.0 (Linux; Android 7.0; TRT-LX3 Build/HUAWEITRT-LX3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.1 Safari/533.2', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.1805 Safari/537.36 MVisionPlayer/1.0.0.0', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36']



def switcher(href_addr):
    while True:
        try:
            ip = requests.get(href_addr,timeout=20).text
            break
        except IndexError:
            continue
        except Exception as errors:    
            print('Ошибка:\n', errors)
            continue
    return ip


utkonos_main_page=switcher(href_addr)
utkonos_main_soup=BeautifulSoup(utkonos_main_page,'html.parser')
utkonos_heading=utkonos_main_soup.find_all(class_='megamenu_hidden_links_index')
logging.basicConfig(filename="utkonos_2_huge.log",format='%(asctime)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S',filemode='w', level=logging.INFO)
arr_name_submenu_final_bad=[]
for n in utkonos_heading:
    for a in n.find_all('a',href=True):
        l=a.get_text()
        arr_name_submenu_final_bad.append(l)
q=open('utka_arr_name_submenu_final.txt','w')
q.write(str(arr_name_submenu_final_bad))
q.write('\n')
q.write(str(len(arr_name_submenu_final_bad)))
q.write('\n')
arr_href_submenu=[]
for n in utkonos_heading:
    for a in n.find_all('a',href=True):
        arr_href_submenu.append(a['href'])
arr_href_submenu_final_bad=[]
arr_href_submenu_final=[]
for i in arr_href_submenu:
    arr_href_submenu_final_bad.append('https://www.utkonos.ru'+i)
arr_name_submenu_final=[]

print(len(arr_href_submenu_final_bad))
print(len(set(arr_href_submenu_final_bad)))
logging.info(str(arr_name_submenu_final_bad))
logging.info('The length of array with categories_names is: '+str(len(arr_name_submenu_final_bad)))
logging.info('The length of array with categories_href is: '+str(len(arr_href_submenu_final_bad)))
arr_name_href_submenu={}
for key,value in zip(arr_name_submenu_final_bad,arr_href_submenu_final_bad):
    arr_name_href_submenu[key]=value
logging.info('The dict with names and hrefs is written')




def parsing_single_html(href_addr,number):
    res_1={}
    html_goods_2=switcher(href_addr)
    html_goods_2_main_soup=BeautifulSoup(html_goods_2,'html.parser')
    html_goods_2_main_heading=html_goods_2_main_soup.find_all(class_='el_paginate')
    html_goods_2_main_heading=str(html_goods_2_main_heading)
    number_of_pages=re.findall(r'\d+',html_goods_2_main_heading)
    number_of_pages_final_1=[]
    number_of_pages=number_of_pages[::-1]
    number_of_pages=number_of_pages[0]
    number_of_pages_final_1.append(number_of_pages)
    for i in number_of_pages_final_1:
        page=int(i)
    for k in range(1,page+1):
        html_href = href_addr + '/page/'+ str(k)
        html_page=switcher(html_href)
        print(html_href)
        test_soup_0=BeautifulSoup(html_page,'html.parser')
        base_0=test_soup_0.find_all(class_='goods_view_box catalogue_type_utkonos pharmacy-banner-show')
        arr_names=[]
        arr_cost_1=[]
        arr_cost=[]
        for i in base_0:
            for j in i.find_all(class_='goods_caption'):
                arr_names.append(j.get('title').replace('.',','))
            for j in i.find_all(class_='goods_price'):
                arr_cost_1.append(j.get("data-static-now-price"))
        for i in arr_cost_1:
            j=float(i)
            arr_cost.append(j)
        result={}
        for key,value in zip(arr_names,arr_cost):
            result[key]=value
        res_1={**res_1,**result}
    logging.info('{:<12} #Pages:{:<12}  #Goods:{:<11}'.format(str(href_addr),str(page),str(len(res_1))))
    return res_1


date=datetime.datetime.now().strftime("%d-%m-%Y")
final_utkonos_huge={}
g=open('res.txt','w')
count_categories=0
for i,j in arr_name_href_submenu.items():
    final_utkonos_huge[i]={'link':j,date:parsing_single_html(j,count_categories)}
    g.write(str(final_utkonos_huge))
    db.final_utkonos_huge.insert_one({i:final_utkonos_huge[i]})


