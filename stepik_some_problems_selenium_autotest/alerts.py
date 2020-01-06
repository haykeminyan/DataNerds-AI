from selenium import webdriver
import time
import math

browser=webdriver.Chrome()
browser.get('http://suninjuly.github.io/alert_accept.html')
button_0=browser.find_element_by_css_selector('.btn').click()
confirm=browser.switch_to.alert
confirm.accept()
def main(x):
    return math.log(abs(12*math.sin(x)))
y=browser.find_element_by_css_selector('#input_value').text
calc=main(int(y))

result=browser.find_element_by_css_selector('#answer')
result.send_keys(str(calc))

button=browser.find_element_by_css_selector('.btn').click()
