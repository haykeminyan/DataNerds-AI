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
import requests
import time
from itertools import cycle
from fake_useragent import UserAgent
from collections import Counter
import shutil
import os
import pandas as pd
import logging
from selenium.webdriver.support.ui import Select
import ssl
logging.basicConfig(filename="1.log",format='%(asctime)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S',filemode='w', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)

href_addr='https://www.gks.ru/dbscripts/cbsd/DBInet.cgi?pl=9460361'

directory=os.path.abspath(os.getcwd())
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : directory+'/report',
         "download.prompt_for_download": False,
         "download.directory_upgrade": True}
chrome_options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.wait = WebDriverWait(browser,10)
# browser.maximize_window()

ua = UserAgent()
headers = {'User-Agent':str(ua.chrome)}

def switcher(href_addr):
    while True:
        try:
            ip=requests.get(href_addr,headers=headers,timeout=10).content
            break
        except Exception as errors:
            logging.info('--------------------------------------------------------------------------')
            logging.error('{}'.format(errors))
            continue
    return ip


main_page=switcher(href_addr)
soup_one=BeautifulSoup(main_page,'html.parser')



main_territory=list(soup_one.find('select', {'name':'okato'}))
territory=main_territory[1].text.strip().split('\r\n')



main_okved=list(soup_one.find('select', {'name':'OKVED2'}))
okved=main_okved[1].text.strip().split('\r\n')

file_xls=directory+'/okved.xls'
pd.set_option('display.max_colwidth',-1)
df = pd.read_excel (file_xls)

new_okved_russian=list(dict(df['ОКВЭД2']).values())
k=1
full_counter_okved={}
for i in range(len(okved)):
    if okved[i] not in full_counter_okved:
        full_counter_okved[okved[i]]=k
        k+=1


w=1
full_counter_new_okved={}
for i in range(len(new_okved_russian)):
    if new_okved_russian[i] not in full_counter_new_okved:
        full_counter_new_okved[new_okved_russian[i]]=w
        w+=1

answer={}
e={}
for i,j in full_counter_new_okved.items():
    for k,l in full_counter_okved.items():
        if i==k:
            e={i:l}
            answer={**answer,**e}

new_okved_list=list(answer.values())
new_okved_english=list(dict(df['filename']).values())

okved_final=dict(zip(new_okved_english,new_okved_list))
# print(new_okved_russian)
# print(okved_final)
# print(new_okved_english)
main_kanal=list(soup_one.find('select', {'name':'kanalreal'}))
kanal=main_kanal[1].text.strip().split('\r\n')


main_years=list(soup_one.find('select',{'name':'god'}))
years=(main_years[1].text.strip().split('\r\n')[::-1])[0]


main_months=list(soup_one.find('select',{'name':'period'}))
month=main_months[1].text.strip().split('\r\n')


last_date={}
z=1
for i in range(len(month)):
    last_date[month[i]]=z
    z+=1
date=((list(last_date.values()))[::-1])[0]

final_date=str(years)+'_'+str(date)



browser.get(href_addr)

# Эти два клика , если браузер пишет незащищнное соединеине
# WebDriverWait(browser,25).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#details-button'))).click()
# WebDriverWait(browser,25).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#proceed-link'))).click()


#Виды показателя
WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > input:nth-child(1)'))).click()
#Годы 
WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)'))).click()

#каналы
WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > input:nth-child(1)'))).click()


# # #расселектить
# WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child(1)'))).click()
# WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child(1)'))).click()
counter=1



WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child(1)'))).click()
WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child(1)'))).click()   

def first_page(href_addr,i,k):
    #страны
    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child('+str(i)+')'))).click()

    #оквэд2
    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child('+str(k)+')'))).click()
    

    #Ручное маркирование
    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#Manual'))).click()
    #всякие данные по док файлу
    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > input:nth-child(1)'))).click()
    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > input:nth-child(1)'))).click()
    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(3) > input:nth-child(1)'))).click()
    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(3) > input:nth-child(1)'))).click()
    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(3) > input:nth-child(1)'))).click()
    #годы
    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(8) > td:nth-child(4) > input:nth-child(1)'))).click()
    #периоды
    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(9) > td:nth-child(4) > input:nth-child(1)'))).click()
    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(9) > td:nth-child(3) > input:nth-child(1)'))).click()
    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(9) > td:nth-child(4) > input:nth-child(1)'))).click()
    #кнопка_выбрать 
    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.BtnStyle'))).click()
    browser.implicitly_wait(5)
    return None

f=open('checkpoint.txt','w')
# g=open('checkpoint.txt','r')
for i in range(1,len(territory)+1):
    for j,k in okved_final.items():
        try:
            browser.implicitly_wait(2)
            first_page(href_addr,i,k)
            browser.implicitly_wait(5)
            #отправка на новую страницу
            browser.switch_to_window(browser.window_handles[1])
            browser.implicitly_wait(5)
            #выбор формата
            WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > form:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > select:nth-child(1) > option:nth-child(2)'))).click()
            #
            WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > form:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > input:nth-child(1)'))).click()
            # time.sleep(2)
            old_file = os.path.join(directory+'/report', 'Report.xls')
            new_file = os.path.join(directory+'/report', str(territory[i-1])+'_'+str(j)+'_'+final_date+'_'+'.xls')
            # time.sleep(3)
            f.write(str(i)+' ')
            f.write(str(j)+' ')
            f.write(str(k))
            f.write('\n')
            # f.close()
            logging.info('Counter {}'.format(counter))
            logging.info('Country_index: {} ,Name_okved_2: {} , Index_okved: {} '.format(i,j,k))
            logging.info('New_file_name: {} '.format(new_file))
            logging.info('--------------------------------------------------------------------------')
            while True:
                # time.sleep(10)
                if os.path.isfile(directory+'/report/Report.xls'):
                    browser.implicitly_wait(10)
                    os.rename(old_file, new_file)
                    browser.implicitly_wait(2)
                    browser.switch_to.window(browser.window_handles[0])
                    #страны
                    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child('+str(i)+')'))).click()
                    #оквэд2
                    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child('+str(k)+')'))).click()
                    break
                # elif not os.path.exists(directory+'/report/Report.xls'):
                #     print('wait untill downloading file')
                #     time.sleep(10)
                #     os.rename(old_file, new_file)
                #     time.sleep(3)
                #     browser.switch_to.window(browser.window_handles[0])
                #     #страны
                #     WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child('+str(i)+')'))).click()
                #     #оквэд2
                #     WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child('+str(k)+')'))).click()
                #     break
                else:
                    print('bad connection')
                    time.sleep(5)
                    f=open('checkpoint.txt','r')
                    last_line_with_spaces=[]
                    new_variables=[]
                    last_line=f.readlines()[-1]
                    last_line_with_spaces.append(last_line)
                    for line in last_line_with_spaces:
                        new_variables_with_new_line=line.split(' ')
                    for i in new_variables_with_new_line:
                        new_variables.append(i.split('\n')[0])
                    logging.info('Connection error! Requesting again! {}{}{}'.format(i,j,k))
                    new_i=new_variables[0]
                    new_k=new_variables[2]
                    print(new_i)
                    print(new_k)
                    browser.switch_to.window(browser.window_handles[0])
                    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.BtnStyle'))).click()
                    browser.implicitly_wait(5)
                    browser.switch_to.window(browser.window_handles[1])
                    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > form:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > select:nth-child(1) > option:nth-child(2)'))).click()
                    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > form:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > input:nth-child(1)'))).click()
                    time.sleep(10)
                    os.rename(old_file, new_file)
                    browser.switch_to.window(browser.window_handles[0])
                    #страны
                    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child('+str(new_i)+')'))).click()
                    #оквэд2
                    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child('+str(new_k)+')'))).click()
                    first_page(href_addr,new_i,new_k)
                    WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.BtnStyle'))).click()
                    time.sleep(2)
                    print('going_back')
                    break
        except Exception as error:
            print('Sdswdasdsafa')
            # counter+=1  
           
        # except Exception as errors:
        #     logging.error('{}'.format(errors))
        #     while True:
        #         try:
        #             browser.refresh()
        #             browser.refresh()
        #             f=open('checkpoint.txt','r')
        #             last_line_with_spaces=[]
        #             new_variables=[]
        #             last_line=f.readlines()[-1]
        #             last_line_with_spaces.append(last_line)
        #             for line in last_line_with_spaces:
        #                 new_variables_with_new_line=line.split(' ')
        #             for i in new_variables_with_new_line:
        #                 new_variables.append(i.split('\n')[0])
        #             logging.info('Connection error! Requesting again! {}{}{}'.format(i,j,k))
        #             new_i=new_variables[0]
        #             new_k=new_variables[2]
        #             WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child(1)'))).click()
        #             WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child(1)'))).click()
        #             break
        #         except Exception as error:
        #             logging.error('{}'.format(error))
        #             break
# try:
#     os.remove(directory+'/report/Report.xls')
# except Exception as e:
#     print('{}'.format(e))