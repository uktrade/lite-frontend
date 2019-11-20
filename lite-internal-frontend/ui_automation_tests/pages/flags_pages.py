import shared.tools.helpers as utils
from helpers.BasePage import BasePage
from pages.shared import Shared


class FlagsPages(BasePage):
    ADD_FLAG_TEXT_FIELD = "name"  # ID
    SELECT_FLAG_LEVEL_DROPDOWN = "level"  # ID
    ADD_FLAG_BUTTON = "add-a-flag-button"  # ID
    FLAGS_IN_EDIT_BOX = "lite-flag"  # CLASS NAME
    REACTIVATE_FLAG_BUTTON = "a[href*='edit/reactivate/']"  # CSS
    DEACTIVATE_FLAG_BUTTON = "a[href*='edit/deactivate/']"  # CSS
    INCLUDE_DEACTIVATED_FLAGS_BUTTON = "[href*='flags/all/']"  # CSS
    INCLUDE_REACTIVATED_FLAGS_BUTTON = "[href*='flags/active/']"  # CSS

    def enter_flag_name(self, text):
        self.driver.find_element_by_id(self.ADD_FLAG_TEXT_FIELD).clear()
        self.driver.find_element_by_id(self.ADD_FLAG_TEXT_FIELD).send_keys(text)

    def select_flag_level(self, value):
        utils.select_visible_text_from_dropdown(self.driver.find_element_by_id(self.SELECT_FLAG_LEVEL_DROPDOWN), value)

    def click_add_a_flag_button(self):
        self.driver.find_element_by_id(self.ADD_FLAG_BUTTON).click()

    def get_size_of_number_of_assigned_flags(self):
        return len(self.driver.find_elements_by_class_name(self.FLAGS_IN_EDIT_BOX))

    def get_size_of_active_flags(self):
        return Shared(self.driver).get_text_of_lite_table_body().count("Active")

    def get_size_of_inactive_flags(self):
        return Shared(self.driver).get_text_of_lite_table_body().count("Deactivated")

    def click_on_deactivate_flag(self):
        self.driver.find_element_by_css_selector(self.DEACTIVATE_FLAG_BUTTON).click()

    def click_on_reactivate_flag(self):
        self.driver.find_element_by_css_selector(self.REACTIVATE_FLAG_BUTTON).click()

    def is_include_deactivated_button_displayed(self):
        return len(self.driver.find_elements_by_css_selector(self.INCLUDE_DEACTIVATED_FLAGS_BUTTON)) == 1

    def click_include_deactivated_flags(self):
        self.driver.find_element_by_css_selector(self.INCLUDE_DEACTIVATED_FLAGS_BUTTON).click()

    def is_include_reactivated_button_displayed(self):
        return len(self.driver.find_elements_by_css_selector(self.INCLUDE_REACTIVATED_FLAGS_BUTTON)) == 1

    def click_include_reactivated_flags(self):
        self.driver.find_element_by_css_selector(self.INCLUDE_REACTIVATED_FLAGS_BUTTON).click()
