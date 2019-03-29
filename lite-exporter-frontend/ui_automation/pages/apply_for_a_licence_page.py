class ApplyForALicencePage():

    # called e time you create an object for this class
    def __init__(self, driver):
        self.driver = driver

        self.apply_for_a_licence_btn = "a[href*='/new-application/']"
        self.drafts_btn = "a[href*='/drafts/']"
        self.name_or_reference_input_id = "name"
        self.control_code_input_id = "control_code"
        self.destination_input_id = "destination"
        self.usage_input_id = "usage"
        self.activity_input_id = "activity"


    def enter_name_or_reference_for_application(self, name):
        self.driver.find_element_by_id(self.name_or_reference_input_id).clear()
        self.driver.find_element_by_id(self.name_or_reference_input_id).send_keys(name)

    def enter_control_code(self, controlCode):
        self.driver.find_element_by_id(self.control_code_input_id).clear()
        self.driver.find_element_by_id(self.control_code_input_id).send_keys(controlCode)

    def enter_destination(self, destination):
        self.driver.find_element_by_id(self.destination_input_id).clear()
        self.driver.find_element_by_id(self.destination_input_id).send_keys(destination)

    def enter_usage(self, usage):
        self.driver.find_element_by_id(self.usage_input_id).clear()
        self.driver.find_element_by_id(self.usage_input_id).send_keys(usage)

    def enter_activity(self, activity):
        self.driver.find_element_by_id(self.activity_input_id).clear()
        self.driver.find_element_by_id(self.activity_input_id).send_keys(activity)

    def click_start_btn(self):
        self.driver.find_element_by_css_selector("a[href*='/start']").click()

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector("button[action*='submit']").click()
