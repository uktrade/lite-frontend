from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.BasePage import BasePage


class AssignUserPage(BasePage):
    VISIBLE_CHOICES_EMAILS = ".govuk-radios__item.visible .govuk-hint"
    VISIBLE_CHOICE_BUTTON = ".govuk-radios__item.visible .govuk-radios__input"
    ASSIGNED_USER_ID = "assigned-users"
    TEXTAREA_SEARCH_ID = "filter-box"

    def select_first_radio_button(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value=self.VISIBLE_CHOICE_BUTTON).click()

    def search(self, text):
        self.driver.find_element(by=By.ID, value=self.TEXTAREA_SEARCH_ID).send_keys(text)

    def get_users_email(self):
        return self.driver.find_elements_by_css_selector(self.VISIBLE_CHOICES_EMAILS)

    def get_assigned_user(self):
        return self.driver.find_element(by=By.ID, value=self.ASSIGNED_USER_ID).text
