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

    def select_product_category(self, category):
        # Accept categories "one", "two", "three-software", "three-technology" and match with an id accordingly
        if category == "two":
            self.driver.find_element_by_id(self.GROUP2_FIREARMS_ID).click()
        if category == "three-software":
            self.driver.find_element_by_id(self.GROUP3_SOFTWARE_ID).click()
        if category == "three-technology":
            self.driver.find_element_by_id(self.GROUP3_TECHNOLOGY_ID).click()
        else:
            # default to category one
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

    def enter_related_field_details(self, related_details_field_id):
        details = fake.sentence(nb_words=5)
        details_element = self.driver.find_element_by_id(related_details_field_id)
        details_element.clear()
        details_element.send_keys(details)
