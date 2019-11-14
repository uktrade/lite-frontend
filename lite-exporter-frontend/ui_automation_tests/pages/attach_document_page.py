class AttachDocumentPage:

    def __init__(self, driver):
        self.driver = driver
        self.file = 'file'  # ID
        self.description = 'description'  # ID
        self.added_document_item = '.lite-card--download'  # CSS

    def choose_file(self, file_location_path):
        self.driver.find_element_by_id(self.file).send_keys(file_location_path)

    def enter_description(self, description):
        self.driver.find_element_by_id(self.description).send_keys(description)

    def get_text_of_document_added_item(self):
        return self.driver.find_element_by_css_selector(self.added_document_item).text
