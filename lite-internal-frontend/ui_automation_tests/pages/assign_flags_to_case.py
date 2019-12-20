from shared.BasePage import BasePage


class CaseFlagsPages(BasePage):
    def select_flag(self, flag_name):
        flag = self.driver.find_elements_by_id(flag_name)[0]
        flag.click()
