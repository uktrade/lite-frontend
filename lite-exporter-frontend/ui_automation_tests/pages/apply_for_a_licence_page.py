import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


class ApplyForALicencePage:
    def __init__(self, driver):
        self.driver = driver
        self.name_or_reference_input_id = "name"
        self.standard_licence_button = "input#application_type-standard_licence"
        self.open_licence_button = "input#application_type-open_licence"
        self.export_button = "export_type-"
        self.export_licence_yes_or_no = "have_you_been_informed-"
        self.reference_number = "reference_number_on_information_form"
        self.success_message = ".govuk-panel__title"
        self.application_is_submitted = ".govuk-panel__title"
        self.delete_application_button = '.govuk-link[href*="/delete"]'  # CSS

    def enter_name_or_reference_for_application(self, name):
        element = self.driver.find_element_by_id(self.name_or_reference_input_id)
        element.clear()
        element.send_keys(name)

    def click_delete_application(self):
        self.driver.find_element_by_css_selector(self.delete_application_button).click()
        self.driver.implicitly_wait(10)
        self.driver.execute_script("document.querySelectorAll('.govuk-button--warning')[0].click()")

    def click_export_licence(self, type):
        logging.info(type)
        if type == "standard":
            return self.driver.find_element_by_css_selector(self.standard_licence_button).click()
        elif type == "open":
            return self.driver.find_element_by_css_selector(self.open_licence_button).click()

    def click_permanent_or_temporary_button(self, string):
        self.driver.find_element_by_id(self.export_button + string).click()

    def click_export_licence_yes_or_no(self, string):
        self.driver.find_element_by_id(self.export_licence_yes_or_no + string).click()

    def get_text_of_success_message(self):
        return self.driver.find_element_by_css_selector(self.success_message).text

    def type_into_reference_number(self, string):
        self.driver.find_element_by_id(self.reference_number).clear()
        self.driver.find_element_by_id(self.reference_number).send_keys(string)

    def application_submitted_text(self):
        return self.driver.find_element_by_css_selector(self.application_is_submitted).text
