from faker import Faker

from ui_automation_tests.pages.BasePage import BasePage

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

    # Firearms - Firearms and ammunition details
    FIREARM_YEAR_OF_MANUFACTURE_TEXTFIELD_ID = "year_of_manufacture"
    FIREARM_CALIBRE_TEXTFIELD_ID = "calibre"

    # Firearms - Firearms act sections 1,2,5 applicable
    FIREARMS_ACT_PREFIX = "is_covered_by_firearm_act_section_one_two_or_five-"
    FIREARMS_ACT_YES_ID = FIREARMS_ACT_PREFIX + "True"
    FIREARMS_ACT_NO_ID = FIREARMS_ACT_PREFIX + "False"
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

    def select_product_category(self, category):
        # Accept categories "one", "two", "three-software", "three-technology" and match with an id accordingly
        if category == "two":
            self.driver.find_element_by_id(self.GROUP2_FIREARMS_ID).click()
        if category == "three-software":
            self.driver.find_element_by_id(self.GROUP3_SOFTWARE_ID).click()
        if category == "three-technology":
            self.driver.find_element_by_id(self.GROUP3_TECHNOLOGY_ID).click()
        if category == "one":
            self.driver.find_element_by_id(self.GROUP1_DEVICE_ID).click()

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
        details_element = self.driver.find_element_by_id(related_details_field_id)
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
        """ Only applicable to firearm goods """
        if option == "firearm":
            self.driver.find_element_by_id(self.FIREARM_TYPE_FIREARM_ID).click()
        if option == "components_for_firearm":
            self.driver.find_element_by_id(self.FIREARM_TYPE_FIREARM_COMPONENT_ID).click()
        if option == "ammunition":
            self.driver.find_element_by_id(self.FIREARM_TYPE_AMMUNITION_ID).click()
        if option == "component_for_ammunition":
            self.driver.find_element_by_id(self.FIREARM_TYPE_AMMUNITION_COMPONENT_ID).click()

    def enter_year_of_manufacture(self):
        self.enter_related_field_details(self.FIREARM_YEAR_OF_MANUFACTURE_TEXTFIELD_ID, text="2004")

    def enter_calibre(self):
        self.enter_related_field_details(self.FIREARM_CALIBRE_TEXTFIELD_ID, text=".99mm")

    def select_do_firearms_act_sections_apply(self, option):
        if option == "Yes":
            self.driver.find_element_by_id(self.FIREARMS_ACT_YES_ID).click()
            self.enter_related_field_details(self.SECTION_CERTIFICATE_NUMBER_TEXTFIELD_ID, text=fake.ean(length=13))
            self.enter_certificate_expiry_date("03", "8", "2027")
        if option == "No":
            self.driver.find_element_by_id(self.FIREARMS_ACT_NO_ID).click()

    def enter_certificate_expiry_date(self, day, month, year):
        self.driver.find_element_by_id(self.CERTIFICATE_EXPIRY_DATE_DAY_ID).send_keys(day)
        self.driver.find_element_by_id(self.CERTIFICATE_EXPIRY_DATE_MONTH_ID).send_keys(month)
        self.driver.find_element_by_id(self.CERTIFICATE_EXPIRY_DATE_YEAR_ID).send_keys(year)

    def does_firearm_have_identification_markings(self, has_markings):
        if has_markings == "Yes":
            self.driver.find_element_by_id(self.FIREARMS_IDENTIFICATION_MARKINGS_YES_ID).click()
            self.enter_related_field_details(self.FIREARMS_IDENTIFICATION_MARKINGS_DETAILS_TEXTAREA_ID)
        if has_markings == "No":
            self.driver.find_element_by_id(self.FIREARMS_IDENTIFICATION_MARKINGS_NO_ID).click()
            self.enter_related_field_details(self.FIREARMS_NO_IDENTIFICATION_MARKINGS_DETAILS_TEXTAREA_ID)
