## -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import requests
from fake_useragent import UserAgent
import os
import datetime
from fake_useragent import UserAgent
import pandas as pd
import logging
from datetime import datetime
import schedule
import time
logging.basicConfig(filename="all_days.log",format='%(asctime)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S',filemode='w', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)
current_date = datetime.today().strftime("%d.%m.%Y")
href_addr='http://www.cbr.ru/hd_base/metall/metall_base_new/?UniDbQuery.Posted=True&UniDbQuery.Gold=true&UniDbQuery.Silver=true&UniDbQuery.Platinum=true&UniDbQuery.Palladium=true&UniDbQuery.FromDate=01.07.2008&UniDbQuery.ToDate='+str(current_date)

directory=os.path.abspath(os.getcwd())
folder_name='all_days_directory'
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
table=list(main_soup.find_all(class_='table'))

for i in table:
    k=i.find(class_='')
    m=k.text.strip()
    columns=m.split('\n')
    j=i.text.strip()
    a=j.split('\n')
a=[i for i in a if i]
rows=len(a)//len(columns)
columns=len(columns)
new=[]
for i in range(0, len(a)-1, columns):
    new.append(a[i : i+columns])
df=pd.DataFrame.from_records(new)
df.to_csv(os.path.join(directory+'/'+folder_name,current_date+'.csv'))


