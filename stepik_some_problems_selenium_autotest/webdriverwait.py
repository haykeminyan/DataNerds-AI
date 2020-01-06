from selenium import webdriver
import time
import math
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
browser=webdriver.Chrome()
# browser.implicitly_wait(12)
browser.get('http://suninjuly.github.io/explicit_wait2.html')
button = WebDriverWait(browser, 15).until(
        EC.text_to_be_present_in_element((By.ID, "price"),'$100')
    )
button_0=browser.find_element_by_css_selector('#book').click()
# confirm=browser.switch_to.alert
# confirm.accept()
def main(x):
    return math.log(abs(12*math.sin(x)))
y=browser.find_element_by_css_selector('#input_value').text
calc=main(int(y))

result=browser.find_element_by_css_selector('#answer')
result.send_keys(str(calc))

button=browser.find_element_by_css_selector('#solve').click()
