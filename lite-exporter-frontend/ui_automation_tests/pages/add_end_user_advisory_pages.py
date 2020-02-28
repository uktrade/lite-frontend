from ui_automation_tests.shared.BasePage import BasePage


class AddEndUserAdvisoryPages(BasePage):

    ADD_NEW_ADDRESS_BUTTON = 'a[href*="add"]'
    TYPE_CHOICES = "sub_type-"

    NATURE_OF_BUSINESS = "nature_of_business"  # ID
    PRIMARY_CONTACT_EMAIL = "contact_email"  # ID
    PRIMARY_CONTACT_NAME = "contact_name"  # ID
    PRIMARY_CONTACT_TELEPHONE = "contact_telephone"  # ID
    PRIMARY_CONTACT_JOB_TITLE = "contact_job_title"  # ID

    def enter_name(self, name, prefix=""):
        name_tb = self.driver.find_element_by_id(prefix + "name")
        name_tb.clear()
        name_tb.send_keys(name)

    def enter_address(self, address, prefix=""):
        address_tb = self.driver.find_element_by_id(prefix + "address")
        address_tb.clear()
        address_tb.send_keys(address)

    def enter_website(self, website, prefix=""):
        address_tb = self.driver.find_element_by_id(prefix + "website")
        address_tb.clear()
        address_tb.send_keys(website)

    def enter_country(self, country, prefix=""):
        country_tb = self.driver.find_element_by_id(prefix + "country")
        country_tb.send_keys(country)

    def enter_reasoning(self, reasoning):
        reasoning_tb = self.driver.find_element_by_id("reasoning")
        reasoning_tb.send_keys(reasoning)

    def enter_notes(self, notes):
        reasoning_tb = self.driver.find_element_by_id("note")
        reasoning_tb.send_keys(notes)

    def select_type(self, string, prefix=""):
        self.driver.find_element_by_id(prefix + self.TYPE_CHOICES + string).click()

    def enter_nature(self, nature_of_business):
        nature_of_business_tb = self.driver.find_element_by_id(self.NATURE_OF_BUSINESS)
        nature_of_business_tb.send_keys(nature_of_business)

    def enter_primary_contact_email(self, primary_contact_email):
        primary_contact_email_tb = self.driver.find_element_by_id(self.PRIMARY_CONTACT_EMAIL)
        primary_contact_email_tb.send_keys(primary_contact_email)

    def enter_primary_contact_name(self, primary_contact_name):
        primary_contact_name_tb = self.driver.find_element_by_id(self.PRIMARY_CONTACT_NAME)
        primary_contact_name_tb.send_keys(primary_contact_name)

    def enter_primary_contact_job_title(self, primary_contact_job_title):
        primary_contact_name_tb = self.driver.find_element_by_id(self.PRIMARY_CONTACT_JOB_TITLE)
        primary_contact_name_tb.send_keys(primary_contact_job_title)

    def enter_primary_contact_telephone(self, primary_contact_telephone):
        primary_contact_telephone_tb = self.driver.find_element_by_id(self.PRIMARY_CONTACT_TELEPHONE)
        primary_contact_telephone_tb.send_keys(primary_contact_telephone)
