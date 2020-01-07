import pytest
import time

from .pages.main_page import MainPage
from .pages.login_page import LoginPage
from .pages.product_page import ProductPage
from .pages.cart_page import CartPage


link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=newYear2019"


# @pytest.mark.parametrize('link', ["http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer0",
#                                   "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer1",
#                                   "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer2",
#                                   "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer3",
#                                   "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer4",
#                                   "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer5",
#                                   "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer6",
#                                   pytest.param("http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer7", marks=pytest.mark.xfail),
#                                   "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer8",
#                                   "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer9"])
#def test_guest_can_add_product_to_cart(browser, link):

@pytest.mark.need_review
def test_guest_can_add_product_to_cart(browser):
    product_page = ProductPage(browser, link)
    product_page.open()
    product_page.add_product_to_cart()


@pytest.mark.xfail
def test_guest_cant_see_success_message_after_adding_product_to_cart(browser):
    product_page = ProductPage(browser, link)
    product_page.open()    
    product_page.add_product_to_cart()
    product_page.should_not_be_success_message()


def test_guest_cant_see_success_message(browser):
    product_page = ProductPage(browser, link)
    product_page.open()    
    product_page.should_not_be_success_message()


@pytest.mark.xfail
def test_message_disappeared_after_adding_product_to_cart(browser):
    product_page = ProductPage(browser, link)
    product_page.open()    
    product_page.add_product_to_cart()
    product_page.success_message_should_disappear()


def test_guest_should_see_login_link_on_product_page(browser):
    product_page = ProductPage(browser, link)
    product_page.open()
    product_page.should_be_login_link()


@pytest.mark.need_review
def test_guest_can_go_to_login_page_from_product_page(browser):
    product_page = ProductPage(browser, link)
    product_page.open()
    product_page.go_to_login_page()
    login_page = LoginPage(browser=browser, url=browser.current_url)
    login_page.should_be_login_page()


@pytest.mark.need_review
def test_guest_cant_see_product_in_cart_opened_from_product_page(browser):
    page = ProductPage(browser, link)
    page.open()
    page.go_to_cart_page()
    cart_page = CartPage(browser=browser, url=browser.current_url)
    cart_page.cart_should_be_empty()
    cart_page.should_be_empty_cart_message()


@pytest.mark.add_to_cart_by_user
class TestUserAddToCartFromProductPage(object):
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.product_link = link

        main_page = MainPage(browser, "http://selenium1py.pythonanywhere.com/")
        main_page.open()
        main_page.go_to_login_page()
        login_page = LoginPage(browser=browser, url=browser.current_url)        
        login_page.register_new_user(email=str(time.time()) + "@fakemail.org", password=str(time.time()))
        login_page.should_be_authorized_user()


    def test_user_cant_see_success_message(self, browser):
        product_page = ProductPage(browser, self.product_link)
        product_page.open()    
        product_page.should_not_be_success_message()


    @pytest.mark.need_review
    def test_user_can_add_product_to_cart(self, browser):
        product_page = ProductPage(browser, self.product_link)
        product_page.open()
        product_page.add_product_to_cart()