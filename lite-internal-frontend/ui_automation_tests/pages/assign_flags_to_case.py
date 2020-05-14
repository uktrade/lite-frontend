import time
from shared import selectors
from shared.BasePage import BasePage


class CaseFlagsPages(BasePage):
    def select_flag(self, flag_name):
        # TODO Make this an implicit wait!
        time.sleep(0.5)
        self.driver.find_element_by_id("filter-box").send_keys(flag_name)
        self.driver.find_element_by_css_selector(selectors.VISIBLE + " " + selectors.CHECKBOX).click()
