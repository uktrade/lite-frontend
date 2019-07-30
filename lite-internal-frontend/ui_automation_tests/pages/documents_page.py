class DocumentsPage():

    def __init__(self, driver):
        self.driver = driver
        self.attach_docs_btn = '.govuk-button[href*="cases"]' #css
        self.doc_description = '//div[@class="lite-card lite-card--download"]/div[1]/p[@class="govuk-body"]' # xpath
        self.doc_filename = '//div[@class="lite-card lite-card--download"]/div[1]/p[@class="govuk-body govuk-!-font-weight-bold"]' # xpath

    def click_attach_documents(self):
        return self.driver.find_element_by_css_selector(self.attach_docs_btn).click()

    def get_document_description_at_position(self, position:int):
        return self.driver.find_elements_by_xpath(self.doc_description)[position].text

    def get_document_filename_at_position(self, position:int):
        return self.driver.find_elements_by_xpath(self.doc_filename)[position].text
