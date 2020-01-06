from selenium import webdriver
import time
import os

browser=webdriver.Chrome()
browser.get('http://suninjuly.github.io/file_input.html')

first_name=browser.find_element_by_css_selector('input.form-control:nth-child(2)')
first_name.send_keys('Hayk')

last_name=browser.find_element_by_css_selector('input.form-control:nth-child(4)')
last_name.send_keys('Eminyan')

email_1=browser.find_element_by_css_selector('input.form-control:nth-child(6)')
email_1.send_keys('spam@spam.ru')

button=browser.find_element_by_css_selector('#file')

current_dir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(current_dir, '1.txt')    
button.send_keys(file_path)

final=browser.find_element_by_css_selector('.btn').click()