from shared.BasePage import BasePage
from shared.tools.helpers import scroll_to_element_by_id


class StandardApplicationTaskListPage(BasePage):

    LINK_GOODS_ID = "link-products"
    LINK_GOODS_LOCATIONS_ID = "link-goods-locations"
    LINK_END_USER_ID = "link-end-user"
    LINK_CONSIGNEE_ID = "link-consignee"
    LINK_THIRD_PARTIES_ID = "link-third-parties"
    LINK_ULTIMATE_RECIPIENTS_ID = "link-ultimate-end-users"
    LINK_SUPPORTING_DOCUMENTATION = "link-supporting-documentation"

    def _click_link(self, element_id):
        scroll_to_element_by_id(self.driver, element_id)
        self.driver.find_element_by_id(element_id).click()

    def click_goods_link(self):
        self._click_link(self.LINK_GOODS_ID)

    def click_goods_locations_link(self):
        self._click_link(self.LINK_GOODS_LOCATIONS_ID)

    def click_end_user_link(self):
        self._click_link(self.LINK_END_USER_ID)

    def click_consignee_link(self):
        self._click_link(self.LINK_CONSIGNEE_ID)

    def click_third_parties_link(self):
        self._click_link(self.LINK_THIRD_PARTIES_ID)

    def click_ultimate_recipients_link(self):
        self._click_link(self.LINK_ULTIMATE_RECIPIENTS_ID)

    def click_supporting_documentation_link(self):
        self._click_link(self.LINK_SUPPORTING_DOCUMENTATION)
