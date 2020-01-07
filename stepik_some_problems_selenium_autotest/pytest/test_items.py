import time

def test_product_page_contains_add_to_basket_button(browser):
    browser.get("http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/")
    #time.sleep(30) 
    browser.find_element_by_css_selector(".btn-add-to-basket")