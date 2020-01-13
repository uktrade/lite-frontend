from shared.BasePage import BasePage


class HMRCQueryTaskListPage(BasePage):

    LOCATION_LINK = "link-goods-location"
    DESCRIBE_YOUR_GOODS = "link-goods"
    SET_END_USER_ID = "link-end-user"
    EXPLAIN_YOUR_REASONING = "link-reasoning"

    def click_application_locations_link(self):
        self.driver.find_element_by_id(self.LOCATION_LINK).click()

    def click_describe_your_goods(self):
        self.driver.find_element_by_id(self.DESCRIBE_YOUR_GOODS).click()

    def click_set_end_user(self):
        self.driver.find_element_by_id(self.SET_END_USER_ID).click()

    def click_explain_your_reasoning(self):
        self.driver.find_element_by_id(self.EXPLAIN_YOUR_REASONING).click()
