from ui_automation_tests.helpers.helpers import scroll_to_bottom_of_page


class ApplicationOverviewPage:

    def __init__(self, driver):
        self.driver = driver
        self.location_link = "location"
        self.countries_link = "countries"
        self.goods_link = "goods"
        self.end_user_link = "end_users"   # ID
        self.consignees_link = "consignees"
        self.ultimate_end_user_link = "ultimate_end_users"   # ID
        self.third_parties = "third_parties"  # ID
        self.sites_link = "a[href*='sites']"
        self.goods_link = "goods"
        self.show_countries_link = "[onclick*='showCountries']"
        self.modal_close = "modal-close-button"   # ID
        self.modal_content = ".modal-content"   # CSS
        self.lite_section = ".lite-section"   # CSS
        self.gov_tables = ".govuk-table__body"   # CSS
        self.back_to_overview_text = "Back to Application" #link text
        self.submit_application_button = "button[type*='submit']" # CSS
        self.attach_end_user_document_link = "attach_doc" # ID
        self.download_end_user_document = "end_user_document_download" # ID
        self.delete_end_user_document = "end_user_document_delete" # ID
        self.end_user_document_state = "end_user_document_state" # ID
        self.attach_end_user_document = "end_user_attach_doc"  # ID
        self.attach_consignee_document = "consignee_attach_doc"  # ID
        self.download_consignee_document = "consignee_document_download"  # ID
        self.delete_consignee_document = "consignee_document_delete"  # ID

    def click_application_locations_link(self):
        self.driver.execute_script("document.getElementById('" + self.location_link + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.location_link).click()

    def click_goods_link(self):
        element = self.driver.find_element_by_id(self.goods_link)
        self.driver.execute_script("arguments[0].click();", element)

    def click_sites_link(self):
        self.driver.find_element_by_css_selector(self.sites_link).click()

    def click_end_user_link(self):
        self.driver.find_element_by_id(self.end_user_link).click()

    def click_ultimate_end_user_link(self):
        self.driver.find_element_by_id(self.ultimate_end_user_link).click()

    def click_consignee_link(self):
        self.driver.find_element_by_id(self.consignees_link).click()

    def click_countries_link(self):
        self.driver.execute_script("document.getElementById('" + self.countries_link + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.countries_link).click()

    def get_text_of_countries_selected(self):
        return self.driver.find_element_by_css_selector(self.show_countries_link).text

    def click_on_countries_selected(self):
        scroll_to_bottom_of_page(self.driver)
        self.driver.find_element_by_css_selector(self.show_countries_link).click()

    def click_on_modal_close(self):
        self.driver.find_element_by_id(self.modal_close).click()

    def click_on_back_to_overview_text(self):
        self.driver.find_element_by_link_text(self.back_to_overview_text).click()

    def get_text_of_country_modal_content(self):
        return self.driver.find_element_by_css_selector(self.modal_content).text

    def get_text_of_end_user_table(self):
        return self.driver.find_elements_by_css_selector(self.gov_tables)[len(self.driver.find_elements_by_css_selector(self.gov_tables))-1].text

    def get_text_of_good(self, no):
        return self.driver.find_elements_by_css_selector(self.lite_section)[no].text

    def get_end_user_document_state_text(self):
        return self.driver.find_element_by_id(self.end_user_document_state).text

    def click_attach_end_user_document(self):
        self.driver.find_element_by_id(self.attach_end_user_document).click()

    def click_attach_consignee_document(self):
        self.driver.find_element_by_id(self.attach_consignee_document).click()

    def click_delete_end_user_document(self):
        self.driver.find_element_by_id(self.delete_end_user_document).click()

    def attach_end_user_document_is_present(self):
        return self.driver.find_elements_by_id(self.attach_end_user_document)

    def click_delete_consignee_document(self):
        self.driver.find_element_by_id(self.delete_consignee_document).click()

    def attach_consignee_document_is_present(self):
        return self.driver.find_elements_by_id(self.attach_consignee_document)

    def click_third_parties(self):
        self.driver.find_element_by_id(self.third_parties).click()
