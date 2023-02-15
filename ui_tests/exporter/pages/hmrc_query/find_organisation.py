from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from ui_tests.exporter.pages.BasePage import BasePage


class HMRCQueryFindOrganisationPage(BasePage):

    TEXTBOX = ".govuk-input"
    ORG_RADIO_GUTTON_ID_PART = "organisation-"
    CONTINUE_BUTTON = "button[value='continue']"

    def search_for_org(self, name):
        textbox = self.driver.find_element(by=By.CSS_SELECTOR, value=self.TEXTBOX)
        textbox.clear()
        textbox.send_keys(name)
        textbox.send_keys(Keys.ENTER)

    def click_org_radio_button(self, org_id):
        self.driver.find_element(by=By.ID, value=self.ORG_RADIO_GUTTON_ID_PART + org_id).click()

    def click_continue(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value=self.CONTINUE_BUTTON).click()
