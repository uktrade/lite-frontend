

class EndUserAdvisoryPage:

    def __init__(self, driver):
        self.driver = driver

        self.apply_for_advisory = "apply"  # id

    def click_apply_for_advisories(self):
        self.driver.find_element_by_id(self.apply_for_advisory).click()
