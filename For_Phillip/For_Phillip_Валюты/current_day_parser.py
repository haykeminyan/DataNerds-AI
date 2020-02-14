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

logging.basicConfig(filename="currency_log_for_current_day.log",format='%(asctime)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S',filemode='w', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)

current_date = datetime.today().strftime("%d.%m.%Y")
href_addr='http://www.cbr.ru/currency_base/daily/?date_req='+current_date
ua = UserAgent()
headers = {'User-Agent':str(ua.chrome)}
def switcher(href_addr):
    while True:
        try:
            ip=requests.get(href_addr,timeout=10,headers=headers).content
            break
        except Exception as errors:
            print(errors)
            continue
    return ip


directory=os.path.abspath(os.getcwd())
folder_name='current_day_directory'
if not os.path.exists(folder_name):
    os.mkdir(folder_name)
    logging.info("Directory {} created".format(folder_name))
else:    
    logging.info("Directory {} already exists".format(folder_name))

main_page=switcher(href_addr)
main_soup=BeautifulSoup(main_page,'html.parser')
digital_code=list(main_soup.find_all(class_='data'))

rows=list(main_soup.select('.data > tbody:nth-child(1) > tr:nth-child(1)'))
for i in rows:
    j=i.text.strip()
    columns=j.split('\n')


for i in digital_code:
    j=i.text.strip()
    data=j.split('\n')
data=[i for i in data if i]

current_len_rows=len(columns)
current_len_columns=int(len(data)/current_len_rows)

def main(i,k):
    a=list(main_soup.select('.data > tbody:nth-child('+str(i)+') > tr:nth-child('+str(k)+')'))
    for i in a:
        j=i.text.strip()
        k=j.split('\n')
    return k
result=[]  
for i in range(1,current_len_rows+1):
    for k in range(1,current_len_columns+1):
        result.append(main(i,k))
main_arrays=[]
for i in result:
    if type(i)!=int:
        main_arrays.append(i)
df = pd.DataFrame.from_records(main_arrays)
df.to_csv(os.path.join(directory+'/'+folder_name,current_date+'.csv'))

