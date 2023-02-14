from selenium.webdriver.common.by import By

from tests_common import functions
from ui_tests.caseworker.pages.BasePage import BasePage

from tests_common.functions import element_with_id_exists


class OpenGeneralLicencesListPage(BasePage):
    BUTTON_NEW_OGL_ID = "button-new-ogl"
    INPUT_NAME_ID = "name"
    LINK_VIEW_SELECTOR = ".govuk-table__cell:last-of-type a"

    def click_new_open_general_licence_button(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_NEW_OGL_ID).click()

    def filter_by_name(self, name):
        functions.try_open_filters(self.driver)
        self.driver.find_element(by=By.ID, value=self.INPUT_NAME_ID).send_keys(name)
        functions.click_apply_filters(self.driver)

    def click_view_first_ogl_link(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value=self.LINK_VIEW_SELECTOR).click()


class OpenGeneralLicencesDetailPage(BasePage):
    SUMMARY_LIST_CLASS = "govuk-summary-list"
    LINK_CHANGE_NAME_ID = "link-change-name"
    LINK_DEACTIVATE_ID = "link-deactivate"

    def get_text_of_summary_list(self):
        return self.driver.find_element(by=By.CLASS_NAME, value=self.SUMMARY_LIST_CLASS).text

    def click_change_name_link(self):
        self.driver.find_element(by=By.ID, value=self.LINK_CHANGE_NAME_ID).click()

    def click_deactivate_link(self):
        self.driver.find_element(by=By.ID, value=self.LINK_DEACTIVATE_ID).click()


class OpenGeneralLicencesCreateEditPage(BasePage):
    RADIO_OPEN_GENERAL_EXPORT_LICENCE_ID = "case_type-00000000-0000-0000-0000-000000000002"
    INPUT_NAME_ID = "name"
    INPUT_DESCRIPTION_ID = "description"
    INPUT_LINK_ID = "url"
    RADIO_REGISTRATION_REQUIRED_YES_ID = "registration_required-True"
    TREE_CONTROLLED_RADIOACTIVE_ID = "node-Controlled-Radioactive-Sources"
    CHECKBOX_UNITED_KINGDOM_ID = "United-Kingdom"
    SUMMARY_LIST_CLASS = "govuk-grid-column-two-thirds"

    def select_open_general_export_licence_radiobutton(self):
        self.driver.find_element(by=By.ID, value=self.RADIO_OPEN_GENERAL_EXPORT_LICENCE_ID).click()

    def enter_name(self, name):
        self.driver.find_element(by=By.ID, value=self.INPUT_NAME_ID).clear()
        self.driver.find_element(by=By.ID, value=self.INPUT_NAME_ID).send_keys(name)

    def enter_description(self, description):
        self.driver.find_element(by=By.ID, value=self.INPUT_DESCRIPTION_ID).send_keys(description)

    def enter_link(self, link):
        self.driver.find_element(by=By.ID, value=self.INPUT_LINK_ID).send_keys(link)

    def select_registration_required_yes(self):
        self.driver.find_element(by=By.ID, value=self.RADIO_REGISTRATION_REQUIRED_YES_ID).click()

    def click_controlled_radioactive_tree(self):
        self.driver.find_element(by=By.ID, value=self.TREE_CONTROLLED_RADIOACTIVE_ID).click()

    def click_united_kingdom_checkbox(self):
        self.driver.find_element(by=By.ID, value=self.CHECKBOX_UNITED_KINGDOM_ID).click()

    def get_text_of_summary_list(self):
        return self.driver.find_element(by=By.CLASS_NAME, value=self.SUMMARY_LIST_CLASS).text


class OpenGeneralLicencesDeactivatePage(BasePage):
    RADIO_YES_ID = "response-yes"

    def select_yes(self):
        self.driver.find_element(by=By.ID, value=self.RADIO_YES_ID).click()


class OpenGeneralLicencesCasePage(BasePage):
    HEADING = ".govuk-heading-m"
    SITE_ID = "ogel_site"
    REISSUE_BUTTON_ID = "button-reissue-ogl"
    CONFIRMATION_YES_RADIO_ID = "confirm-True"

    def get_text_of_first_heading(self):
        return self.driver.find_elements_by_css_selector(self.HEADING)[0].text

    def get_text_of_second_heading(self):
        return self.driver.find_elements_by_css_selector(self.HEADING)[1].text

    def get_text_of_site(self):
        return self.driver.find_element(by=By.ID, value=self.SITE_ID).text

    def reissue_button_is_present(self):
        return element_with_id_exists(self.driver, self.REISSUE_BUTTON_ID)

    def click_reissue_button(self):
        self.driver.find_element(by=By.ID, value=self.REISSUE_BUTTON_ID).click()

    def accept_reissue_confirmation(self):
        self.driver.find_element(by=By.ID, value=self.CONFIRMATION_YES_RADIO_ID).click()
