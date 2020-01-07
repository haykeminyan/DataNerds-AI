import pytest

from .pages.main_page import MainPage
from .pages.login_page import LoginPage
from .pages.cart_page import CartPage


link = "http://selenium1py.pythonanywhere.com/"

@pytest.mark.login_guest
class TestLoginFromMainPage(object):
    def test_guest_can_see_login_link(self, browser):
        main_page = MainPage(browser, link)
        main_page.open()
        main_page.should_be_login_link()


    def test_guest_can_go_to_login_page(self, browser):
        main_page = MainPage(browser, link)
        main_page.open()
        main_page.go_to_login_page()
        login_page = LoginPage(browser=browser, url=browser.current_url)
        login_page.should_be_login_page()


def test_guest_cant_see_product_in_cart_opened_from_main_page(browser):
    main_page = MainPage(browser, link)
    main_page.open()
    main_page.go_to_cart_page()
    cart_page = CartPage(browser=browser, url=browser.current_url)
    cart_page.cart_should_be_empty()
    cart_page.should_be_empty_cart_message()