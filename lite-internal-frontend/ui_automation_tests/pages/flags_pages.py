import shared.tools.helpers as utils
from pages.shared import Shared


class FlagsPages:
    def __init__(self, driver):
        self.driver = driver
        self.add_flag_text_field = "name"  # ID
        self.select_flag_level_dropdown = "level"  # ID
        self.add_flag_button = "add-a-flag-button"  # ID
        self.flags_in_edit_box = "lite-flag"  # CLASS NAME
        self.reactivate_flag_button = "a[href*='edit/reactivate/']"  # CSS
        self.deactivate_flag_button = "a[href*='edit/deactivate/']"  # CSS
        self.include_deactivated_flags_button = "[href*='flags/all/']"  # CSS
        self.include_reactivated_flags_button = "[href*='flags/active/']"  # CSS

    def enter_flag_name(self, text):
        self.driver.find_element_by_id(self.add_flag_text_field).clear()
        self.driver.find_element_by_id(self.add_flag_text_field).send_keys(text)

    def select_flag_level(self, value):
        utils.select_visible_text_from_dropdown(self.driver.find_element_by_id(self.select_flag_level_dropdown), value)

    def click_add_a_flag_button(self):
        self.driver.find_element_by_id(self.add_flag_button).click()

    def get_size_of_number_of_assigned_flags(self):
        return len(self.driver.find_elements_by_class_name(self.flags_in_edit_box))

    def get_size_of_active_flags(self):
        return Shared(self.driver).get_text_of_lite_table_body().count("Active")

    def get_size_of_inactive_flags(self):
        return Shared(self.driver).get_text_of_lite_table_body().count("Deactivated")

    def click_on_deactivate_flag(self):
        self.driver.find_element_by_css_selector(self.deactivate_flag_button).click()

    def click_on_reactivate_flag(self):
        self.driver.find_element_by_css_selector(self.reactivate_flag_button).click()

    def is_include_deactivated_button_displayed(self):
        return len(self.driver.find_elements_by_css_selector(self.include_deactivated_flags_button)) == 1

    def click_include_deactivated_flags(self):
        self.driver.find_element_by_css_selector(self.include_deactivated_flags_button).click()

    def is_include_reactivated_button_displayed(self):
        return len(self.driver.find_elements_by_css_selector(self.include_reactivated_flags_button)) == 1

    def click_include_reactivated_flags(self):
        self.driver.find_element_by_css_selector(self.include_reactivated_flags_button).click()
