import math

from selenium.common.exceptions import NoAlertPresentException

from .base_page import BasePage
from .locators import ProductPageLocators


class ProductPage(BasePage):
    def should_not_be_success_message(self):
        assert self.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGE), \
           "Success message is presented, but should not be"


    def success_message_should_disappear(self):
        assert self.is_disappeared(*ProductPageLocators.SUCCESS_MESSAGE), \
           "Success message is presented, but should disappear"


    def add_product_to_cart(self):
        product_name = self.get_product_name()
        product_price = self.get_product_price()

        button = self.browser.find_element(*ProductPageLocators.ADD_TO_CART_BUTTON)
        button.click()
        self.solve_quiz_and_get_code()

        alert_product_name = self.browser.find_element(*ProductPageLocators.ALERT_PRODUCT_NAME).text
        alert_product_price = self.browser.find_element(*ProductPageLocators.ALERT_PRODUCT_PRICE).text

        assert alert_product_name == product_name, \
            "Wrong product '{}' is added instead of '{}'".format(alert_product_name, product_name)

        assert alert_product_price == product_price, \
            "Wrong product price '{}' is used instead of '{}'".format(alert_product_price, product_price)


    def get_product_name(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_NAME).text


    def get_product_price(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE).text


    def solve_quiz_and_get_code(self):
        alert = self.browser.switch_to.alert
        x = alert.text.split(" ")[2]
        answer = str(math.log(abs((12 * math.sin(float(x))))))
        alert.send_keys(answer)
        alert.accept()
        try:
            alert = self.browser.switch_to.alert
            print("Your code: {}".format(alert.text))
            alert.accept()
        except NoAlertPresentException:
            print("No second alert presented")