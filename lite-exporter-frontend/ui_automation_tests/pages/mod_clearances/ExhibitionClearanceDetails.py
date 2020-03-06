from ui_automation_tests.shared.BasePage import BasePage


class ExhibitionClearanceDetailsPage(BasePage):
    NAME_FIELD_ID = "title"
    EXHIBITION_START_DAY_ID = "first_exhibition_dateday"
    EXHIBITION_START_MONTH_ID = "first_exhibition_datemonth"
    EXHIBITION_START_YEAR_ID = "first_exhibition_dateyear"
    CLEARANCE_REQUIRED_BY_DAY_ID = "required_by_dateday"
    CLEARANCE_REQUIRED_BY_MONTH_ID = "required_by_datemonth"
    CLEARANCE_REQUIRED_BY_YEAR_ID = "required_by_dateyear"

    def enter_exhibition_name(self, name):
        self.driver.find_element_by_id(self.NAME_FIELD_ID).clear()
        self.driver.find_element_by_id(self.NAME_FIELD_ID).send_keys(name)

    def enter_exhibition_start_date(self, day, month, year):
        self.driver.find_element_by_id(self.EXHIBITION_START_DAY_ID).clear()
        self.driver.find_element_by_id(self.EXHIBITION_START_DAY_ID).send_keys(day)
        self.driver.find_element_by_id(self.EXHIBITION_START_MONTH_ID).clear()
        self.driver.find_element_by_id(self.EXHIBITION_START_MONTH_ID).send_keys(month)
        self.driver.find_element_by_id(self.EXHIBITION_START_YEAR_ID).clear()
        self.driver.find_element_by_id(self.EXHIBITION_START_YEAR_ID).send_keys(year)

    def enter_exhibition_required_by_date(self, day, month, year):
        self.driver.find_element_by_id(self.CLEARANCE_REQUIRED_BY_DAY_ID).clear()
        self.driver.find_element_by_id(self.CLEARANCE_REQUIRED_BY_DAY_ID).send_keys(day)
        self.driver.find_element_by_id(self.CLEARANCE_REQUIRED_BY_MONTH_ID).clear()
        self.driver.find_element_by_id(self.CLEARANCE_REQUIRED_BY_MONTH_ID).send_keys(month)
        self.driver.find_element_by_id(self.CLEARANCE_REQUIRED_BY_YEAR_ID).clear()
        self.driver.find_element_by_id(self.CLEARANCE_REQUIRED_BY_YEAR_ID).send_keys(year)
