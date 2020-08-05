from selenium.common.exceptions import WebDriverException

from shared import selectors
from pages.BasePage import BasePage


class BaseAdvicePage(BasePage):
    TABLE_GOODS_ID = None
    TABLE_DESTINATIONS_ID = None
    BUTTON_GIVE_ADVICE_ID = None
    BUTTON_GROUPED_VIEW_ID = "button-grouped-view"

    def click_give_advice(self):
        self.driver.find_element_by_id(self.BUTTON_GIVE_ADVICE_ID).click()

    def click_grouped_view_button(self):
        self.driver.find_element_by_id(self.BUTTON_GROUPED_VIEW_ID).click()

    def click_on_all_checkboxes(self):
        elements = self.driver.find_elements_by_css_selector(f"#{self.TABLE_GOODS_ID} {selectors.CHECKBOX}")

        for element in elements:
            self.driver.execute_script("arguments[0].click();", element)

        self.driver.find_element_by_id(self.BUTTON_GIVE_ADVICE_ID).click()
        return len(elements)

    def is_advice_button_enabled(self):
        try:
            self.driver.find_element_by_id(self.BUTTON_GIVE_ADVICE_ID).click()
            return True
        except WebDriverException:
            return False


class UserAdvicePage(BaseAdvicePage):
    TABLE_GOODS_ID = "table-goods-user-advice"
    TABLE_DESTINATIONS_ID = "table-goods-user-advice"
    BUTTON_GIVE_ADVICE_ID = "button-give-user-advice"
    BUTTON_COALESCE_ID = "button-combine-user-advice"

    def click_combine_advice(self):
        self.driver.find_element_by_id(self.BUTTON_COALESCE_ID).click()

    def click_grouped_view_checkboxes(self, group):
        for checkbox in self.driver.find_elements_by_css_selector(
            f"#form-user-advice-container .app-grouped-advice--{group} .app-grouped-advice__heading .lite-button-checkbox"
        ):
            checkbox.click()


class TeamAdvicePage(BaseAdvicePage):
    TABLE_GOODS_ID = "table-goods-team-advice"
    TABLE_DESTINATIONS_ID = "table-goods-team-advice"
    BUTTON_GIVE_ADVICE_ID = "button-give-team-advice"
    BUTTON_CLEAR_ADVICE_ID = "button-clear-team-advice"
    BUTTON_COALESCE_ID = "button-combine-team-advice"

    def click_combine_advice(self):
        self.driver.find_element_by_id(self.BUTTON_COALESCE_ID).click()

    def click_clear_advice(self):
        self.driver.find_element_by_id(self.BUTTON_CLEAR_ADVICE_ID).click()


class FinalAdvicePage(BaseAdvicePage):
    TABLE_GOODS_ID = "table-goods-final-advice"
    TABLE_DESTINATIONS_ID = "table-destination-final-advice"
    BUTTON_GIVE_ADVICE_ID = "button-give-final-advice"
    BUTTON_CLEAR_ADVICE_ID = "button-clear-final-advice"
    BUTTON_FINALISE_ID = "button-finalise"
    BLOCKING_FLAGS_WARNING_ID = "warning-text-blocking-flags"

    def can_finalise(self):
        return "govuk-button--disabled" in self.driver.find_element_by_id(self.BUTTON_FINALISE_ID).get_attribute(
            "class"
        )

    def click_finalise(self):
        self.driver.find_element_by_id(self.BUTTON_FINALISE_ID).click()

    def get_blocking_flags_text(self):
        return self.driver.find_element_by_id(self.BLOCKING_FLAGS_WARNING_ID).text

    def click_clear_advice(self):
        self.driver.find_element_by_id(self.BUTTON_CLEAR_ADVICE_ID).click()
