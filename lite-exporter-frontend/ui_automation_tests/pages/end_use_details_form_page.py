from ui_automation_tests.shared.BasePage import BasePage


class EndUseDetailsFormPage(BasePage):
    INPUT_FIELD_CLASS = "govuk-input"

    COMPLIANT_LIMITATIONS_EU_REF_ID = "compliant_limitations_eu_ref"
    SUSPECTED_WMD_REF_ID = "suspected_wmd_ref"

    def click_on_yes_radiobutton(self):
        self.driver.find_element_by_css_selector("[id$=-True]").click()

    def click_on_no_radiobutton(self):
        self.driver.find_element_by_css_selector("[id$=-False]").click()

    def enter_reference_number(self, ref_number):
        ref_field = self.driver.find_element_by_class_name(self.INPUT_FIELD_CLASS)
        ref_field.clear()
        ref_field.send_keys(ref_number)

    def enter_additional_details(self, field_id, details):
        self.driver.execute_script(f'document.getElementById("{field_id}").value = "{details[:-1]}"')
        self.driver.find_element_by_id(field_id).send_keys(details[-1:])

    def answer_military_end_use_controls(self, flag: bool, ref_number=None):
        if flag:
            self.click_on_yes_radiobutton()
            self.enter_reference_number(ref_number)
        else:
            self.click_on_no_radiobutton()

    def answer_is_informed_wmd(self, flag: bool, ref_number=None):
        if flag:
            self.click_on_yes_radiobutton()
            self.enter_reference_number(ref_number)
        else:
            self.click_on_no_radiobutton()

    def answer_is_suspected_wmd(self, flag: bool, details=None):
        if flag:
            self.click_on_yes_radiobutton()
            self.enter_additional_details(self.SUSPECTED_WMD_REF_ID, details)
        else:
            self.click_on_no_radiobutton()

    def answer_is_eu_military(self, flag: bool):
        if flag:
            self.click_on_yes_radiobutton()
        else:
            self.click_on_no_radiobutton()

    def answer_is_compliant_limitations_eu(self, flag, details=None):
        if flag:
            self.click_on_yes_radiobutton()
        else:
            self.click_on_no_radiobutton()
            self.enter_additional_details(self.COMPLIANT_LIMITATIONS_EU_REF_ID, details)
