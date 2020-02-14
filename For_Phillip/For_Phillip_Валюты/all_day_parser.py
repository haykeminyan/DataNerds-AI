## -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from datetime import timedelta, date
from fake_useragent import UserAgent
from collections import Counter
import shutil
import os
import datetime
from fake_useragent import UserAgent
import pandas as pd
import numpy as np
import logging
from selenium.webdriver.support.ui import Select
import ssl
from datetime import datetime
import string

logging.basicConfig(filename="currency_log_all_days.log",format='%(asctime)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S',filemode='w', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)

directory=os.path.abspath(os.getcwd())
folder_name='csv_files'
if not os.path.exists(folder_name):
    os.mkdir(folder_name)
    logging.info("Directory {} created".format(folder_name))
else:    
    logging.info("Directory {} already exists".format(folder_name))

arr_day_month_year=[]
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(1992,7,1)
end_date = date.today()
for single_date in daterange(start_date, end_date):
    arr_day_month_year.append(single_date.strftime("%d-%m-%Y"))
href_massiv=[]
for i in arr_day_month_year:
    href_massiv.append('http://www.cbr.ru/currency_base/daily/?date_req='+i)

ua = UserAgent()
headers = {'User-Agent':str(ua.random)}
def switcher(href_addr):
    while True:
        try:
            ip=requests.get(href_addr,timeout=10,headers=headers).content
            break
        except Exception as errors:
            logging.error(errors)
            continue
    return ip

def main(i,k):
    a=list(main_soup.select('.data > tbody:nth-child('+str(i)+') > tr:nth-child('+str(k)+')'))
    for i in a:
        j=i.text.strip()
        k=j.split('\n')
    return k



main_arrays=[]
dict_i={}
for name in href_massiv:
    a=[]
    result=[]
    main_arrays=[]
    main_page=switcher(name)
    logging.info('{}'.format(name))
    main_soup=BeautifulSoup(main_page,'html.parser')
    digital_code=list(main_soup.find_all(class_='data'))
    rows=list(main_soup.select('.data > tbody:nth-child(1) > tr:nth-child(1)'))
    for i in rows:
        j=i.text.strip()
        columns=j.split('\n')
    for a in digital_code:
        j=a.text.strip()
        data=j.split('\n')
    data=[i for i in data if i]
    current_len_rows=len(columns)
    current_len_columns=int(len(data)/current_len_rows)
    for i in range(1,current_len_rows+1):
        for k in range(1,current_len_columns+1):
            result.append(main(i,k))
    for b in result:
        if type(b)!=int:
            main_arrays.append(b)
    df=pd.DataFrame.from_records(main_arrays)
    df.to_csv(os.path.join(directory+'/'+folder_name,name[48:]+'.csv'))