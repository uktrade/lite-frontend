from selenium.webdriver.common.by import By
from ui_tests.exporter.pages.BasePage import BasePage


class RouteOfGoodsFormPage(BasePage):
    TEXT_AREA_CLASS = "govuk-textarea"

    def click_on_yes_radiobutton(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value="[id$=-True]").click()

    def click_on_no_radiobutton(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value="[id$=-False]").click()

    def enter_non_waybill_or_lading_route_details(self, details):
        details_field = self.driver.find_element(by=By.CLASS_NAME, value=self.TEXT_AREA_CLASS)
        details_field.clear()
        details_field.send_keys(details)

    def answer_route_of_goods_question(self, flag: bool, details=None):
        if flag:
            self.click_on_no_radiobutton()
            self.enter_non_waybill_or_lading_route_details(details)
        else:
            self.click_on_yes_radiobutton()
