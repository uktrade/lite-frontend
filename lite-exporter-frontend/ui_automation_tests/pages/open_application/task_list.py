from shared.BasePage import BasePage
from shared.tools.helpers import scroll_to_element_by_id


class OpenApplicationTaskListPage(BasePage):

    LINK_COUNTRIES_ID = "link-countries"

    def _click_link(self, element_id):
        scroll_to_element_by_id(self.driver, element_id)
        self.driver.find_element_by_id(element_id).click()

    def click_countries_link(self):
        self._click_link(self.LINK_COUNTRIES_ID)
