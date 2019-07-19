class AttachDocumentPage():

    def __init__(self, driver):
        self.driver = driver
        self.file = 'file' #id
        self.description = 'description' #id
        self.submit_btn = '.govuk-button[action="submit"]' #css

    def choose_file(self, file_location_path):
        self.driver.find_element_by_id(self.file).send_keys(file_location_path)

    def enter_description(self, description):
        self.driver.find_element_by_id(self.description).send_keys(description)

    def click_submit_btn(self):
        self.driver.find_element_by_css_selector(self.submit_btn).click()
