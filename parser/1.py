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


href_addr='https://www.gks.ru/dbscripts/cbsd/DBInet.cgi?pl=9460361'



browser = webdriver.Chrome()
browser.wait = WebDriverWait(browser,10)
browser.maximize_window()
options = Options()
options.add_experimental_option("prefs", {
  "download.default_directory": r"/report",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
ua = UserAgent()
headers = {'User-Agent':str(ua.chrome)}

def switcher(href_addr):
    while True:
        try:
            ip=requests.get(href_addr,headers=headers,timeout=10).content
            print(headers)
            break
        except Exception as errors:
            print(errors)
            continue
    return ip


main_page=switcher(href_addr)
soup_one=BeautifulSoup(main_page,'html.parser')



main_territory=soup_one.find('select', {'name':'okato'})
a=[]
a.append(main_territory)
territory_bad=[]
for item in a:
    territory_bad.append(item.text.strip().split('\r\n'))
territory=[]
for i in territory_bad:
    for j in i:
        territory.append(j)
# print(territory)

main_okved=soup_one.find('select', {'name':'OKVED2'})
b=[]
b.append(main_okved)
okved_bad=[]
for item in b:
    okved_bad.append(item.text.strip().split('\r\n'))
okved=[]
for i in okved_bad:
    for j in i:
        okved.append(j)
# print(okved)
new_okved=['Производство готовых металлических изделий, кроме машин и оборудования','Промышленное производство (промышленность)','Производство химических веществ и химических продуктов','Добыча металлических руд','Производство целлюлозы, древесной массы, бумаги и картона','Производство машин и оборудования общего назначения','Производство кирпича, черепицы и прочих строительных изделий из обожженной глины','Производство пищевых продуктов','Производство продуктов мукомольной и крупяной промышленности','Производство строительных металлических конструкций и изделий','Производство автотранспортных средств, прицепов и полуприцепов','Добыча руд цветных металлов','Лесоводство и лесозаготовки','Добыча сырой нефти и природного газа','Производство молочной продукции','Производство удобрений и азотных соединений','Производство чугуна, стали и ферросплавов','Производство растительных и животных масел и жиров','Производство машин и оборудования для сельского и лесного хозяйства','Подготовка и прядение текстильных волокон','Производство сахара','Производство текстильных тканей','Производство цемента, извести и гипса','Добыча угля','Производство кокса']

counter_okved={}
full_counter_okved={}
q=0
for i in range(len(okved)):
    counter_okved={okved[i]:q}
    full_counter_okved={**full_counter_okved,**counter_okved}
    q+=1
 
counter_new_okved={}
full_counter_new_okved={}
w=0
for i in range(len(new_okved)):
    counter_new_okved={new_okved[i]:w}
    full_counter_new_okved={**full_counter_new_okved,**counter_new_okved}
    w+=1
answer={}
e={}
for i,j in full_counter_new_okved.items():
    for k,l in full_counter_okved.items():
        if i==k:
            e={i:l}
            answer={**answer,**e}
# print(answer)

new_okved_list=[164, 1, 109, 17, 96, 190, 147, 31, 38, 165, 212, 19, 2, 12, 36, 115, 154, 35, 203, 64, 45, 65, 149, 9, 107]
new_okved_list.sort()

# print(new_okved_list)
main_kanal=soup_one.find('select', {'name':'kanalreal'})
c=[]
c.append(main_kanal)
kanal_bad=[]
for item in c:
    kanal_bad.append(item.text.strip().split('\r\n'))
kanal=[]
for i in kanal_bad:
    for j in i:
        kanal.append(j)
browser.get(href_addr)



#Виды показателя
WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > input:nth-child(1)'))).click()
#Годы 
WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)'))).click()
# okved=new_okved
for i in range(1,len(territory)):
    for j in new_okved_list:
        for z in range(1,len(kanal)):
            driver=WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child('+str(i)+')')))
            if driver.is_selected():
                pass
            else:
                driver.click()
    
            driver_1=WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child('+str(j)+')')))
            if driver_1.is_selected():
                pass
            else:
                driver_1.click()

            driver_2=WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > select:nth-child(4) > option:nth-child('+str(z)+')')))
            if driver_2.is_selected():
                pass
            else:
                driver_2.click()
            
            #Ручное маркирование
            WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#Manual'))).click()
            #всякие данные по док файлу
            WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > input:nth-child(1)'))).click()
            WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > input:nth-child(1)'))).click()
            WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(3) > input:nth-child(1)'))).click()
            WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(3) > input:nth-child(1)'))).click()
            WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(3) > input:nth-child(1)'))).click()
            WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(8) > td:nth-child(4) > input:nth-child(1)'))).click()
            WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#form2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(9) > td:nth-child(4) > input:nth-child(1)'))).click()
            WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.BtnStyle'))).click()
            #отправка на новую страницу
            window_after = browser.window_handles[1]
            browser.switch_to_window(window_after)
            WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > form:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > select:nth-child(1) > option:nth-child(2)'))).click()
            WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > form:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > input:nth-child(1)'))).click()
            #свитчемся на старую
            window_before = browser.window_handles[0]
            browser.switch_to.window(window_before)



#Периоды
# WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > font:nth-child(1) > center:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3) > input:nth-child(1)'))).click()


