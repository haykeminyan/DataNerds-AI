## -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import requests
from fake_useragent import UserAgent
import os
from fake_useragent import UserAgent
import pandas as pd
import logging
from datetime import datetime,timedelta
import schedule
import time
logging.basicConfig(filename="one_day_srednevz.log",format='%(asctime)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S',filemode='w', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)

current_date = datetime.today().strftime("%d.%m.%Y")
yesterday_fulltime=datetime.today()-timedelta(1)
yesterday=yesterday_fulltime.strftime("%d.%m.%Y")
href_addr='http://www.cbr.ru/hd_base/mkr/mkr_base/?UniDbQuery.Posted=True&UniDbQuery.st=SF&UniDbQuery.ob=OB_MIACR_0&UniDbQuery.Currency=-1&UniDbQuery.sk=Dd1_&UniDbQuery.FromDate='+str(yesterday)+'&UniDbQuery.ToDate='+str(current_date)

directory=os.path.abspath(os.getcwd())
folder_name='current_day_Средневзвешенные фактические ставки по кредитам в рублях, предоставленным московскими банками'
if not os.path.exists(folder_name):
    os.mkdir(folder_name)
    logging.info("Directory {} created".format(folder_name))
else:    
    logging.info("Directory {} already exists".format(folder_name))
ua=UserAgent()
headers={'User-Agent':str(ua.random)}
def switcher(href_addr):
    while True:
        try:
            ip=requests.get(href_addr,headers=headers,timeout=10).content
            break
        except Exception as errors:
            print(errors)
            continue
    return ip
main_page=switcher(href_addr)
main_soup=BeautifulSoup(main_page,'html.parser')
table=list(main_soup.find_all(class_='data'))

columns=2
a=list(main_soup.select('div.table-wrapper:nth-child(2) > div:nth-child(2) > table:nth-child(1)'))
for i in a:
    j=i.text.strip()
    k=j.split('\n')
k=[i for i in k if i]
new=[]
for i in range(0, len(k)-1, columns):
    new.append(k[i : i+columns])
df=pd.DataFrame.from_records(new)
df.drop_duplicates(keep=False)
df.to_csv(os.path.join(directory+'/'+folder_name,yesterday+'.csv'))