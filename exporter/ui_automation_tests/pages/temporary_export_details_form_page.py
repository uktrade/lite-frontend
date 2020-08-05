from ui_automation_tests.pages.BasePage import BasePage


class TemporaryExportDetailsFormPage(BasePage):
    DATE_DAY_ID = "day"
    DATE_MONTH_ID = "month"
    DATE_YEAR_ID = "year"

    TEMP_EXPORT_DETAILS_FIELD_ID = "temp_export_details"
    DIRECT_CONTROL_DETAILS_ID = "temp_direct_control_details"

    IS_TEMP_DIRECT_CONTROL_RADIO_ID = "is_temp_direct_control"

    def click_on_yes_radiobutton(self):
        self.driver.find_element_by_css_selector("[id$=-True]").click()

    def click_on_no_radiobutton(self):
        self.driver.find_element_by_css_selector("[id$=-False]").click()

    def enter_details(self, field_id, details):
        self.driver.execute_script(f'document.getElementById("{field_id}").value = "{details[:-1]}"')
        self.driver.find_element_by_id(field_id).send_keys(details[-1:])

    def answer_temp_export_details(self, details):
        self.enter_details(self.TEMP_EXPORT_DETAILS_FIELD_ID, details)

    def answer_is_temp_direct_control(self, flag: bool, details=None):
        if flag:
            self.click_on_yes_radiobutton()
        else:
            self.click_on_no_radiobutton()
            self.enter_details(self.DIRECT_CONTROL_DETAILS_ID, details)

    def proposed_return_date(self, day, month, year):
        self.driver.find_element_by_id(self.DATE_DAY_ID).send_keys(day)
        self.driver.find_element_by_id(self.DATE_MONTH_ID).send_keys(month)
        self.driver.find_element_by_id(self.DATE_YEAR_ID).send_keys(year)
