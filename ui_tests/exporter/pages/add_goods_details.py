from selenium.webdriver.common.by import By
from faker import Faker

from ui_tests.exporter.pages.BasePage import BasePage

fake = Faker()


class AddGoodDetails(BasePage):
    # Product category
    ITEM_CATEGORY_PREFIX = "item_category-"
    GROUP1_PLATFORM_ID = ITEM_CATEGORY_PREFIX + "group1_platform"
    GROUP1_DEVICE_ID = ITEM_CATEGORY_PREFIX + "group1_device"
    GROUP1_COMPONENTS_ID = ITEM_CATEGORY_PREFIX + "group1_components"
    GROUP1_MATERIALS_ID = ITEM_CATEGORY_PREFIX + "group1_materials"
    GROUP2_FIREARMS_ID = ITEM_CATEGORY_PREFIX + "group2_firearms"
    GROUP3_SOFTWARE_ID = ITEM_CATEGORY_PREFIX + "group3_software"
    GROUP3_TECHNOLOGY_ID = ITEM_CATEGORY_PREFIX + "group3_technology"

    # Military use
    MILITARY_USE_PREFIX = "is_military_use-"
    MILITARY_USE_YES_DESIGNED_ID = MILITARY_USE_PREFIX + "yes_designed"
    MILITARY_USE_YES_MODIFIED_ID = MILITARY_USE_PREFIX + "yes_modified"
    MILITARY_USE_DETAILS_TEXTAREA_ID = "modified_military_use_details"
    NOT_FOR_MILITARY_USE_ID = MILITARY_USE_PREFIX + "no"

    # Component
    COMPONENT_PREFIX = "is_component-"
    COMPONENT_YES_DESIGNED_ID = COMPONENT_PREFIX + "yes_designed"
    COMPONENT_DESIGNED_DETAILS_TEXTAREA_ID = "designed_details"
    COMPONENT_YES_MODIFIED_ID = COMPONENT_PREFIX + "yes_modified"
    COMPONENT_MODIFIED_DETAILS_TEXTAREA_ID = "modified_details"
    COMPONENT_YES_GENERAL_PURPOSE_ID = COMPONENT_PREFIX + "yes_general"
    COMPONENT_GENERAL_DETAILS_TEXTAREA_ID = "general_details"
    NOT_A_COMPONENT_ID = COMPONENT_PREFIX + "no"

    # Information security
    INFORMATION_SECURITY_PREFIX = "uses_information_security-"
    INFORMATION_SECURITY_YES_ID = INFORMATION_SECURITY_PREFIX + "True"
    INFORMATION_SECURITY_DETAILS_TEXTAREA_ID = "information_security_details"
    INFORMATION_SECURITY_NO_ID = INFORMATION_SECURITY_PREFIX + "False"

    # Software/Technology details for category 3 goods
    SOFTWARE_OR_TECHNOLOGY_DETAILS_TEXTAREA_ID = "software_or_technology_details"

    # Firearms - Product type
    FIREARM_TYPE_PREFIX = "type-"
    FIREARM_TYPE_FIREARM_ID = FIREARM_TYPE_PREFIX + "firearms"
    FIREARM_TYPE_FIREARM_COMPONENT_ID = FIREARM_TYPE_PREFIX + "components_for_firearms"
    FIREARM_TYPE_AMMUNITION_ID = FIREARM_TYPE_PREFIX + "ammunition"
    FIREARM_TYPE_AMMUNITION_COMPONENT_ID = FIREARM_TYPE_PREFIX + "components_for_ammunition"
    FIREARM_TYPE_FIREARM_ACCESSORY_ID = FIREARM_TYPE_PREFIX + "firearms_accessory"
    FIREARM_TYPE_FIREARM_SOFTWARE_ID = FIREARM_TYPE_PREFIX + "software_related_to_firearms"
    FIREARM_TYPE_FIREARM_TECHNOLOGY_ID = FIREARM_TYPE_PREFIX + "technology_related_to_firearms"

    # Firearms - Firearms and ammunition details
    FIREARM_YEAR_OF_MANUFACTURE_TEXTFIELD_ID = "year_of_manufacture"
    FIREARM_CALIBRE_TEXTFIELD_ID = "calibre"

    # Firearms - Firearms act sections 1,2,5 applicable
    FIREARMS_ACT_PREFIX = "is_covered_by_firearm_act_section_one_two_or_five-"
    FIREARMS_ACT_YES_ID = FIREARMS_ACT_PREFIX + "Yes"
    FIREARMS_ACT_NO_ID = FIREARMS_ACT_PREFIX + "No"
    FIREARMS_ACT_DONTKNOW_ID = FIREARMS_ACT_PREFIX + "Unsure"
    SECTION_CERTIFICATE_NUMBER_TEXTFIELD_ID = "section_certificate_number"

    CERTIFICATE_EXPIRY_DATE_PREFIX = "section_certificate_date_of_expiry"
    CERTIFICATE_EXPIRY_DATE_DAY_ID = CERTIFICATE_EXPIRY_DATE_PREFIX + "day"
    CERTIFICATE_EXPIRY_DATE_MONTH_ID = CERTIFICATE_EXPIRY_DATE_PREFIX + "month"
    CERTIFICATE_EXPIRY_DATE_YEAR_ID = CERTIFICATE_EXPIRY_DATE_PREFIX + "year"

    # Firearms - identification markings
    FIREARMS_IDENTIFICATION_MARKINGS_PREFIX = "has_identification_markings-"
    FIREARMS_IDENTIFICATION_MARKINGS_YES_ID = FIREARMS_IDENTIFICATION_MARKINGS_PREFIX + "True"
    FIREARMS_IDENTIFICATION_MARKINGS_NO_ID = FIREARMS_IDENTIFICATION_MARKINGS_PREFIX + "False"
    FIREARMS_IDENTIFICATION_MARKINGS_DETAILS_TEXTAREA_ID = "identification_markings_details"
    FIREARMS_NO_IDENTIFICATION_MARKINGS_DETAILS_TEXTAREA_ID = "no_identification_markings_details"
    FIREARMS_NUMBER_OF_ITEMS = "number_of_items"
    FIREARMS_SERIAL_NUMBERS = "serial_numbers"

    def true_or_false(self, status):
        return "True" if status == "Yes" else "False"

    def select_product_category(self, category):
        # Accept categories "one", "two", "three-software", "three-technology" and match with an id accordingly
        if category == "firearms":
            self.driver.find_element_by_id(self.GROUP2_FIREARMS_ID).click()
        if category == "three-software":
            self.driver.find_element_by_id(self.GROUP3_SOFTWARE_ID).click()
        if category == "three-technology":
            self.driver.find_element_by_id(self.GROUP3_TECHNOLOGY_ID).click()
        if category == "one":
            self.driver.find_element_by_id(self.GROUP1_DEVICE_ID).click()

    def set_identification_details(self, has_markings, details):
        self.driver.find_element(by=By.XPATH, value=f"//input[@type='radio' and @value='{has_markings}']").click()
        if has_markings == "NOT_AVAILABLE":
            self.enter_related_field_details("id_IDENTIFICATION_MARKINGS-no_identification_markings_details", details)

    def enter_number_of_items(self, number_of_items):
        element = self.driver.find_element(
            by=By.XPATH, value=f"//input[@type='text' and contains(@id, '{self.FIREARMS_NUMBER_OF_ITEMS}')]"
        )

        element.clear()
        element.send_keys(number_of_items)

    def enter_serial_numbers(self, serial_numbers):
        for i, el in enumerate(
            self.driver.find_elements(
                by=By.XPATH, value=f"//input[@type='text' and contains(@id, '{self.FIREARMS_SERIAL_NUMBERS}')]"
            )
        ):
            el.clear()
            el.send_keys(serial_numbers[i].strip())

    def set_product_document_availability(self, choice):
        choice = choice.lower()
        self.driver.find_element(by=By.ID, value=f"is_document_available-{choice}").click()

    def set_product_document_sensitive(self, choice):
        choice = choice.lower()
        self.driver.find_element_by_id(f"is_document_sensitive-{choice}").click()

    def set_registered_firearms_dealer(self, choice):
        choice = "True" if choice == "Yes" else "False"
        self.driver.find_element_by_id(f"is_registered_firearm_dealer-{choice}").click()

    def select_is_product_for_military_use(self, option):
        # yes_designed, yes_modified and no
        if option == "yes_designed":
            self.driver.find_element_by_id(self.MILITARY_USE_YES_DESIGNED_ID).click()
        if option == "yes_modified":
            self.driver.find_element_by_id(self.MILITARY_USE_YES_MODIFIED_ID).click()
            self.enter_related_field_details(self.MILITARY_USE_DETAILS_TEXTAREA_ID)
        if option == "no":
            self.driver.find_element_by_id(self.NOT_FOR_MILITARY_USE_ID).click()

    def select_is_product_a_component(self, option):
        # yes_designed, yes_modified, yes_general and no
        if option == "yes_designed":
            self.driver.find_element_by_id(self.COMPONENT_YES_DESIGNED_ID).click()
            self.enter_related_field_details(self.COMPONENT_DESIGNED_DETAILS_TEXTAREA_ID)
        if option == "yes_modified":
            self.driver.find_element_by_id(self.COMPONENT_YES_MODIFIED_ID).click()
            self.enter_related_field_details(self.COMPONENT_MODIFIED_DETAILS_TEXTAREA_ID)
        if option == "yes_general":
            self.driver.find_element_by_id(self.COMPONENT_YES_GENERAL_PURPOSE_ID).click()
            self.enter_related_field_details(self.COMPONENT_GENERAL_DETAILS_TEXTAREA_ID)
        if option == "no":
            self.driver.find_element_by_id(self.NOT_A_COMPONENT_ID).click()

    def does_product_employ_information_security(self, option):
        if option == "Yes":
            self.driver.find_element_by_id(self.INFORMATION_SECURITY_YES_ID).click()
            self.enter_related_field_details(self.INFORMATION_SECURITY_DETAILS_TEXTAREA_ID)
        if option == "No":
            self.driver.find_element_by_id(self.INFORMATION_SECURITY_NO_ID).click()

    def enter_related_field_details(self, related_details_field_id, text=None):
        if not text:
            details = fake.sentence(nb_words=5)
        else:
            details = text
        details_element = self.driver.find_element(by=By.ID, value=related_details_field_id)
        details_element.clear()
        details_element.send_keys(details)

    def enter_software_technology_purpose_details(self, text=None):
        if not text:
            self.enter_related_field_details(self.SOFTWARE_OR_TECHNOLOGY_DETAILS_TEXTAREA_ID)
        else:
            details_element = self.driver.find_element_by_id(self.SOFTWARE_OR_TECHNOLOGY_DETAILS_TEXTAREA_ID)
            details_element.clear()
            details_element.send_keys(text)

    def select_firearm_product_type(self, option):
        """Only applicable to firearm goods"""
        if option == "Firearm":
            self.driver.find_element(by=By.CSS_SELECTOR, value="input[value='firearms']").click()
        if option == "components_for_firearm":
            self.driver.find_element(by=By.ID, value=self.FIREARM_TYPE_FIREARM_COMPONENT_ID).click()
        if option == "ammunition":
            self.driver.find_element(by=By.ID, value=self.FIREARM_TYPE_AMMUNITION_ID).click()
        if option == "component_for_ammunition":
            self.driver.find_element(by=By.ID, value=self.FIREARM_TYPE_AMMUNITION_COMPONENT_ID).click()
        if option == "firearm_accessory":
            self.driver.find_element(by=By.ID, value=self.FIREARM_TYPE_FIREARM_ACCESSORY_ID).click()
        if option == "software_for_firearm":
            self.driver.find_element(by=By.ID, value=self.FIREARM_TYPE_FIREARM_SOFTWARE_ID).click()
        if option == "technology_for_firearm":
            self.driver.find_element(by=By.ID, value=self.FIREARM_TYPE_FIREARM_TECHNOLOGY_ID).click()

    def enter_year_of_manufacture(self, year):
        self.driver.find_element(
            by=By.XPATH,
            value=f"//input[contains(@id, '{self.FIREARM_YEAR_OF_MANUFACTURE_TEXTFIELD_ID}')]",
        ).send_keys(year)

    def select_replica_status(self, status, description=""):
        status = self.true_or_false(status)
        self.driver.find_element_by_id(f"is_replica-{status}").click()
        if status == "True":
            desc = self.driver.find_element_by_id("replica_description")
            desc.clear()
            desc.send_keys(description)

    def enter_calibre(self, calibre):
        self.driver.find_element(
            by=By.XPATH, value=f"//input[contains(@id, '{self.FIREARM_CALIBRE_TEXTFIELD_ID}')]"
        ).send_keys(calibre)

    def select_do_firearms_act_sections_apply(self, choice):
        if choice == "Yes":
            self.driver.find_element_by_id(self.FIREARMS_ACT_YES_ID).click()
        if choice == "No":
            self.driver.find_element_by_id(self.FIREARMS_ACT_NO_ID).click()
        if choice == "Unsure":
            self.driver.find_element_by_id(self.FIREARMS_ACT_DONTKNOW_ID).click()

    def select_firearms_act_section(self, num):
        self.driver.find_element_by_id(f"firearms_act_section-firearms_act_section{num}").click()

    def choose_firearms_certificate_file(self, path):
        self.driver.find_element_by_id("file").send_keys(path)

    def enter_firearms_act_certificate_number(self, cert_num):
        self.enter_related_field_details(self.SECTION_CERTIFICATE_NUMBER_TEXTFIELD_ID, cert_num)

    def enter_certificate_expiry_date(self, day, month, year):
        self.driver.find_element_by_id(self.CERTIFICATE_EXPIRY_DATE_DAY_ID).send_keys(day)
        self.driver.find_element_by_id(self.CERTIFICATE_EXPIRY_DATE_MONTH_ID).send_keys(month)
        self.driver.find_element_by_id(self.CERTIFICATE_EXPIRY_DATE_YEAR_ID).send_keys(year)

    def does_firearm_have_identification_markings(self, has_markings, details="details"):
        if has_markings == "Yes":
            self.driver.find_element_by_id(self.FIREARMS_IDENTIFICATION_MARKINGS_YES_ID).click()
            self.enter_related_field_details(self.FIREARMS_IDENTIFICATION_MARKINGS_DETAILS_TEXTAREA_ID, text=details)
        if has_markings == "No":
            self.driver.find_element_by_id(self.FIREARMS_IDENTIFICATION_MARKINGS_NO_ID).click()
            self.enter_related_field_details(self.FIREARMS_NO_IDENTIFICATION_MARKINGS_DETAILS_TEXTAREA_ID, text=details)
