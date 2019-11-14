class AddEndUserAdvisoryPages:

    def __init__(self, driver):
        self.driver = driver
        self.add_new_address_button = 'a[href*="add"]'
        self.type_choices = "sub_type-"

        self.nature_of_business = "nature_of_business"  # ID
        self.primary_contact_email = "contact_email"  # ID
        self.primary_contact_name = "contact_name"  # ID
        self.primary_contact_telephone = "contact_telephone"  # ID
        self.primary_contact_job_title = "contact_job_title"  # ID

    def enter_name(self, name, prefix=''):
        name_tb = self.driver.find_element_by_id(prefix + 'name')
        name_tb.clear()
        name_tb.send_keys(name)

    def enter_address(self, address, prefix=''):
        address_tb = self.driver.find_element_by_id(prefix + 'address')
        address_tb.clear()
        address_tb.send_keys(address)

    def enter_website(self, website, prefix=''):
        address_tb = self.driver.find_element_by_id(prefix + 'website')
        address_tb.clear()
        address_tb.send_keys(website)

    def enter_country(self, country, prefix=''):
        country_tb = self.driver.find_element_by_id(prefix + 'country')
        country_tb.send_keys(country)

    def enter_reasoning(self, reasoning):
        reasoning_tb = self.driver.find_element_by_id('reasoning')
        reasoning_tb.send_keys(reasoning)

    def enter_notes(self, notes):
        reasoning_tb = self.driver.find_element_by_id('note')
        reasoning_tb.send_keys(notes)

    def confirmation_code(self):
        confirmation_panel_body = '//div[@class="govuk-panel__body"]'
        text = self.driver.find_element_by_xpath(confirmation_panel_body).text
        numbers = ''.join(text.split(': ')[1].split('-'))
        return numbers

    def select_type(self, string, prefix=''):
        self.driver.find_element_by_id(prefix + self.type_choices + string).click()

    def enter_nature(self, nature_of_business):
        nature_of_business_tb = self.driver.find_element_by_id(self.nature_of_business)
        nature_of_business_tb.send_keys(nature_of_business)

    def enter_primary_contact_email(self, primary_contact_email):
        primary_contact_email_tb = self.driver.find_element_by_id(self.primary_contact_email)
        primary_contact_email_tb.send_keys(primary_contact_email)

    def enter_primary_contact_name(self, primary_contact_name):
        primary_contact_name_tb = self.driver.find_element_by_id(self.primary_contact_name)
        primary_contact_name_tb.send_keys(primary_contact_name)

    def enter_primary_contact_job_title(self, primary_contact_job_title):
        primary_contact_name_tb = self.driver.find_element_by_id(self.primary_contact_job_title)
        primary_contact_name_tb.send_keys(primary_contact_job_title)

    def enter_primary_contact_telephone(self, primary_contact_telephone):
        primary_contact_telephone_tb = self.driver.find_element_by_id(self.primary_contact_telephone)
        primary_contact_telephone_tb.send_keys(primary_contact_telephone)
