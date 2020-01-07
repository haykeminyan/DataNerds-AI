import unittest
from selenium import webdriver
import time

def register(href_addr):
    browser = webdriver.Chrome()
    browser.get(href_addr)
    input1 = browser.find_element_by_css_selector('.first_block .first')
    input1.send_keys("Iva n")
    input2 = browser.find_element_by_css_selector('.first_block .second')
    input2.send_keys("P etrov")
    input3 = browser.find_element_by_css_selector(".first_block .third")
    input3.send_keys("Pet rov")
    time.sleep(1)
    button = browser.find_element_by_xpath('/html/body/div/form/button')
    button.click()
    time.sleep(1)
    text = browser.find_element_by_xpath('//h1')
    return text.text
class TestAbs(unittest.TestCase):
    def test_abs1(self):
        text = register("http://suninjuly.github.io/registration1.html")
        assert "Congratulations! You have successfully registered!" in text
    def test_abs2(self):
        text = register("http://suninjuly.github.io/registration2.html")
        assert "Congratulations! You have successfully registered!" in text
if __name__ == "__main__":
    unittest.main()

