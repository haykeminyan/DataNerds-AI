from datetime import timedelta, date
from fake_useragent import UserAgent
from collections import Counter
import shutil
import os
import datetime
from fake_useragent import UserAgent
import pandas as pd
import numpy as np
import csv
import logging
from selenium.webdriver.support.ui import Select
import ssl
from datetime import datetime
import requests
from bs4 import BeautifulSoup

href_addr='https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130429&end=20200212'

logging.basicConfig(filename="1.log",format='%(asctime)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S',filemode='w', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)
ua = UserAgent()
headers = {'User-Agent':str(ua.random)}
def switcher(href_addr):
    while True:
        try:
            ip=requests.get(href_addr,timeout=None).content
            break
        except Exception as errors:
            logging.error('{}'.format(errors))
            continue
    return ip

main_page=switcher(href_addr)
main_soup=BeautifulSoup(main_page,'html.parser')
how_many_we_have_rows=main_soup.find_all(class_='cmc-table__cell cmc-table__cell--sticky cmc-table__cell--left')
print(len(how_many_we_have_rows))


def main(i,k):
    a=list(main_soup.select('tr.cmc-table-row:nth-child('+str(i)+') > td:nth-child('+str(k)+') > div:nth-child(1)'))
    for i in a:
        j=i.text.strip()
        # k=j.split('\n')
    return j
# print(main(1,2))


a=[]
b=[]
for i in range(len(how_many_we_have_rows),2461,-1):
    for k in range(1,8):
        a.append(main(i,k))
    logging.info('---------------------------')
    logging.info('{}'.format(a))
    logging.info('---------------------------')
new = []
for i in range(0, len(a), 7):
    new.append(a[i : i+7])

df=pd.DataFrame.from_records(new,columns=['Date','Open','High','Low','Close','Volume','Market Cup'])
# df=pd.DataFrame.from_records(new,columns=['Date','Open','High','Low','Close'])
df.index = np.arange(1, len(df)+1)
df.to_csv('result.csv')
