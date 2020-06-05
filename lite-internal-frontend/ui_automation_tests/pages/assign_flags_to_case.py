from shared import selectors
from shared.BasePage import BasePage


class CaseFlagsPages(BasePage):
    def select_flag(self, flag_name):
        self.driver.find_element_by_id("filter-box").send_keys(flag_name)
        if (
            not self.driver.find_element_by_css_selector(selectors.VISIBLE + " " + selectors.CHECKBOX).get_attribute(
                "checked"
            )
            == "true"
        ):
            self.driver.find_element_by_css_selector(selectors.VISIBLE + " " + selectors.CHECKBOX).click()
