from shared import functions
from shared.BasePage import BasePage


class ApplyForALicencePage(BasePage):

    NAME_OR_REFERENCE_INPUT_ID = "name"
    BUTTON_STANDARD_LICENCE = "input#application_type-standard_licence"
    BUTTON_OPEN_LICENCE = "input#application_type-open_licence"
    EXPORT_BUTTON = "export_type-"
    EXPORT_LICENCE_YES_OR_NO = "have_you_been_informed-"
    REFERENCE_NUMBER = "reference_number_on_information_form"
    SUCCESS_MESSAGE = ".govuk-panel__title"
    APPLICATION_IS_SUBMITTED = ".govuk-panel__title"
    LINK_DELETE_DRAFT_ID = "link-delete-draft"
    SUCCESS_BANNER_CLASS = ".govuk-panel--confirmation"

    def enter_name_or_reference_for_application(self, name):
        element = self.driver.find_element_by_id(self.NAME_OR_REFERENCE_INPUT_ID)
        element.clear()
        element.send_keys(name)

    def click_delete_application(self):
        self.driver.find_element_by_id(self.LINK_DELETE_DRAFT_ID).click()
        self.driver.find_element_by_id("choice-yes").click()
        functions.click_submit(self.driver)

    def click_export_licence(self, export_type):
        if export_type == "standard":
            return self.driver.find_element_by_css_selector(self.BUTTON_STANDARD_LICENCE).click()
        elif export_type == "open":
            return self.driver.find_element_by_css_selector(self.BUTTON_OPEN_LICENCE).click()

    def click_permanent_or_temporary_button(self, string):
        self.driver.find_element_by_id(self.EXPORT_BUTTON + string).click()

    def click_export_licence_yes_or_no(self, string):
        self.driver.find_element_by_id(self.EXPORT_LICENCE_YES_OR_NO + string).click()

    def get_text_of_success_message(self):
        return self.driver.find_element_by_css_selector(self.SUCCESS_MESSAGE).text

    def type_into_reference_number(self, string):
        self.driver.find_element_by_id(self.REFERENCE_NUMBER).clear()
        self.driver.find_element_by_id(self.REFERENCE_NUMBER).send_keys(string)

    def application_submitted_text(self):
        return self.driver.find_element_by_css_selector(self.APPLICATION_IS_SUBMITTED).text

    def is_success_panel_present(self):
        return len(self.driver.find_elements_by_css_selector(self.SUCCESS_BANNER_CLASS)) > 0
