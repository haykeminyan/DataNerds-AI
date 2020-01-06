from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import requests
import time
import re
from itertools import cycle


from selenium import webdriver
from selenium.webdriver.support.ui import Select

browser = webdriver.Chrome()
browser.get("http://suninjuly.github.io/selects1.html")

a = int(browser.find_element_by_css_selector("#num1").text)
b = int(browser.find_element_by_css_selector("#num2").text)

select = Select(browser.find_element_by_tag_name("select"))
select.select_by_value(str(a+b))

button = browser.find_element_by_tag_name("button")
button.click()