from ui_automation_tests.shared import functions
from ui_automation_tests.shared.BasePage import BasePage


class ApplyForALicencePage(BasePage):

    NAME_OR_REFERENCE_INPUT_ID = "name"
    LICENCE_TYPE_PARTIAL_ID = "licence_type-"
    MOD_APPLICATION_TYPE_PARTIAL_ID = "application_type-"
    RADIOBUTTON_LICENCE_ID_PARTIAL = "input#application_type-"
    EXPORT_BUTTON = "export_type-"
    EXPORT_LICENCE_YES_OR_NO = "have_you_been_informed-"
    REFERENCE_NUMBER = "reference_number_on_information_form"
    LINK_DELETE_DRAFT_ID = "link-delete-draft"
    SUCCESS_BANNER_CLASS = ".govuk-panel--confirmation"
    CHECKBOXES_GOODS_CATEGORIES_NAME = "goods_categories[]"
    F680_CLEARANCE_TYPE_CHECKBOXES_NAME = "types[]"

    def enter_name_or_reference_for_application(self, name):
        element = self.driver.find_element_by_id(self.NAME_OR_REFERENCE_INPUT_ID)
        element.clear()
        element.send_keys(name)

    def select_licence_type(self, type):
        self.driver.find_element_by_id(f"{self.LICENCE_TYPE_PARTIAL_ID}{type}").click()

    def select_mod_application_type(self, type):
        self.driver.find_element_by_id(f"{self.MOD_APPLICATION_TYPE_PARTIAL_ID}{type}").click()

    def click_delete_application(self):
        self.driver.find_element_by_id(self.LINK_DELETE_DRAFT_ID).click()
        self.driver.find_element_by_id("choice-yes").click()
        functions.click_submit(self.driver)

    def click_export_licence(self, export_type):
        return self.driver.find_element_by_css_selector(self.RADIOBUTTON_LICENCE_ID_PARTIAL + export_type).click()

    def select_goods_categories(self):
        checkboxes = self.driver.find_elements_by_name(self.CHECKBOXES_GOODS_CATEGORIES_NAME)
        for checkbox in checkboxes:
            checkbox.click()

    def select_types_of_clearance(self):
        checkboxes = self.driver.find_elements_by_name(self.F680_CLEARANCE_TYPE_CHECKBOXES_NAME)
        for checkbox in checkboxes:
            checkbox.click()

    def click_permanent_or_temporary_button(self, string):
        self.driver.find_element_by_id(self.EXPORT_BUTTON + string).click()

    def click_export_licence_yes_or_no(self, string):
        self.driver.find_element_by_id(self.EXPORT_LICENCE_YES_OR_NO + string).click()

    def type_into_reference_number(self, string):
        self.driver.find_element_by_id(self.REFERENCE_NUMBER).clear()
        self.driver.find_element_by_id(self.REFERENCE_NUMBER).send_keys(string)

    def is_success_panel_present(self):
        return len(self.driver.find_elements_by_css_selector(self.SUCCESS_BANNER_CLASS)) > 0
