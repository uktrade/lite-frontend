from selenium.webdriver.common.keys import Keys

from shared.BasePage import BasePage


class HMRCQueryPage(BasePage):

    TEXTBOX = ".govuk-input"
    ORG_RADIO_GUTTON_ID_PART = "organisation-"
    CONTINUE_BUTTON = "button[value='continue']"

    def search_for_org(self, name):
        textbox = self.driver.find_element_by_css_selector(self.TEXTBOX)
        textbox.clear()
        textbox.send_keys(name)
        textbox.send_keys(Keys.ENTER)

    def click_org_radio_button(self, org_id):
        self.driver.find_element_by_id(self.ORG_RADIO_GUTTON_ID_PART + org_id).click()

    def click_continue(self):
        self.driver.find_element_by_css_selector(self.CONTINUE_BUTTON).click()
