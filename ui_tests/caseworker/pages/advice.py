from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from tests_common import selectors
from ui_tests.caseworker.pages.BasePage import BasePage


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


class RecommendationsAndDecisionPage(BasePage):
    def click_make_recommendation(self):
        self.driver.find_element(by=By.XPATH, value="//a[contains(text(), 'Make recommendation')]").click()

    def click_refuse(self):
        self.driver.find_element(by=By.XPATH, value="//input[@type='radio' and @value='refuse']").click()

    def click_approve_all(self):
        self.driver.find_element(by=By.XPATH, value="//input[@type='radio' and @value='approve_all']").click()

    def click_refuse_all(self):
        self.driver.find_element(by=By.XPATH, value="//input[@type='radio' and @value='refuse_all']").click()

    def select_country(self, country):
        self.driver.find_element(by=By.XPATH, value=f"//input[@type='checkbox' and @value='{country}']").click()

    def select_refusal_criteria(self, criteria):
        self.driver.find_element(by=By.XPATH, value=f"//input[@type='checkbox' and @value='{criteria}']").click()

    def enter_reasons_for_approving(self, reasons):
        el = self.driver.find_element(by=By.XPATH, value="//textarea[@name='approval_reasons']")
        el.clear()
        el.send_keys(reasons)

    def enter_reasons_for_refusal(self, reasons):
        el = self.driver.find_element(by=By.XPATH, value="//textarea[@name='refusal_reasons']")
        el.clear()
        el.send_keys(reasons)

    def enter_licence_condition(self, licence_condition):
        el = self.driver.find_element(by=By.XPATH, value="//textarea[@name='proviso']")
        el.clear()
        el.send_keys(licence_condition)

    def enter_instructions_for_exporter(self, instructions):
        el = self.driver.find_element(by=By.XPATH, value="//textarea[@name='instructions_to_exporter']")
        el.clear()
        el.send_keys(instructions)

    def enter_reporting_footnote(self, footnote):
        el = self.driver.find_element(by=By.XPATH, value="//textarea[@name='footnote_details']")
        el.clear()
        el.send_keys(footnote)

    def enter_optional_decision_note(self, note):
        el = self.driver.find_element(by=By.ID, value="note")
        el.clear()
        el.send_keys(note)

    def get_reasons_for_approving(self):
        return self.driver.find_element(
            by=By.XPATH,
            value="//p[ancestor::div[preceding-sibling::*[self::h2 or self::h3]"
            "[contains(text(), 'Reason for approving') or contains(text(), 'Reasons for approving')]]][2]",
        ).text

    def get_reasons_for_refusal(self):
        return self.driver.find_element(
            by=By.XPATH,
            value="//p[ancestor::div[preceding-sibling::*[self::h2 or self::h3]"
            "[contains(text(), 'Reason for refusing') or contains(text(), 'Reasons for refusing')]]][2]",
        ).text

    def get_licence_condition(self):
        return self.driver.find_element(
            by=By.XPATH,
            value="//p[ancestor::div[preceding-sibling::*[self::h2 or self::h3]"
            "[contains(text(), 'Licence condition')]]][2]",
        ).text

    def get_instructions_for_exporter(self):
        return self.driver.find_element(
            by=By.XPATH,
            value="//p[ancestor::div[preceding-sibling::*[self::h2 or self::h3]"
            "[contains(text(), 'Additional instructions')]]][2]",
        ).text

    def get_reporting_footnote(self):
        return self.driver.find_element(
            by=By.XPATH,
            value="//p[ancestor::div[preceding-sibling::*[self::h2 or self::h3]"
            "[contains(text(), 'Reporting footnote')]]][2]",
        ).text

    def get_refusal_criteria(self):
        """Return the refusal criteria for each destination as a list."""
        return [
            r.find_element(by=By.XPATH, value="td[5]").text
            for r in self.driver.find_elements(
                by=By.XPATH,
                value="//tbody/tr",
            )
        ]
