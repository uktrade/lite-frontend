class CaseFlagsPages():

    def __init__(self, driver):
        self.driver = driver

    def assign_flags(self, context):
        flags = self.driver.find_elements_by_css_selector("input.govuk-checkboxes__input")
        flags[0].click()
        context.assigned_flag = flags[0].get_attribute("id")
        
    def select_flag(self, context, flag_id):
        flag = self.driver.find_elements_by_id(flag_id)[0]
        flag.click()
        context.assigned_flag = flag_id

