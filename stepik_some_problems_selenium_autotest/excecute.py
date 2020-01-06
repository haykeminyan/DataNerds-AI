from selenium import webdriver
import math

def func(x):
    return math.log(abs(12*math.sin(x)))

browser=webdriver.Chrome()
browser.get('http://suninjuly.github.io/execute_script.html')
a=int(browser.find_element_by_id('input_value').text)
b=func(a)
answer=browser.find_element_by_id('answer')
answer.send_keys(str(b))
browser.find_element_by_css_selector('#robotCheckbox').click()

radiobutton=browser.find_element_by_css_selector('#robotsRule')
browser.execute_script("return arguments[0].scrollIntoView(true);", radiobutton)
radiobutton.click()

final=browser.find_element_by_class_name('btn-primary.btn')
browser.execute_script("return arguments[0].scrollIntoView(true);", final)
final.click()