from selenium.common.exceptions import WebDriverException

from tests_common import selectors
from ui_tests.caseworker.pages.BasePage import BasePage


class BaseAdvicePage(BasePage):
    TABLE_GOODS_ID = None
    TABLE_DESTINATIONS_ID = None
    ALL_GOODS_CHECKBOX_ID = "link-select-all-goods"
    BUTTON_GIVE_ADVICE_ID = "button-give-user-advice"
    BUTTON_GROUPED_VIEW_ID = "button-grouped-view"
    APPROVE_OPTION_ID = "type-approve"
    NO_FOOTNOTE_OPTION_ID = "footnote_required-False"
    SUBMIT_ADVICE_ID = "button-Submit advice"

    def click_good(self):
        # Resort to using javascript to click the button because the element is "hidden"
        # element = self.driver.find_element_by_id(self.ALL_GOODS_CHECKBOX_ID)
        # self.driver.execute_script("arguments[0].click();", element)
        self.driver.find_element_by_name("goods").click()

    def click_give_advice(self):
        # element = self.driver.find_element_by_id(self.BUTTON_GIVE_ADVICE_ID)
        # self.driver.execute_script("disabled = false;", element)
        # element.submit()
        self.driver.find_element_by_id("form-user-advice-container").submit()

    def click_approve(self):
        self.driver.find_element_by_id(self.APPROVE_OPTION_ID).click()

    def click_no_footnote_required(self):
        self.driver.find_element_by_id(self.NO_FOOTNOTE_OPTION_ID).click()

    def click_submit_advice(self):
        self.driver.find_element_by_id(self.SUBMIT_ADVICE_ID).click()

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
            return self.driver.find_element_by_id(self.BUTTON_GIVE_ADVICE_ID).is_enabled()
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
    EDIT_FLAGS_ID = "link-change-flags"
    ENFORCEMENT_CHECK_ID = "Enforcement-Check-Req"
    SET_FLAGS_ID = "button-Set flags"

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

    def click_edit_flags(self):
        self.driver.find_element_by_id(self.EDIT_FLAGS_ID).click()

    def click_enforcement_check_box(self):
        self.driver.find_element_by_id(self.ENFORCEMENT_CHECK_ID).click()

    def click_set_flags(self):
        self.driver.find_element_by_id(self.SET_FLAGS_ID).click()
