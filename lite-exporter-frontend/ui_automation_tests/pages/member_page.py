from shared.BasePage import BasePage


class MemberPage(BasePage):

    PANE_MORE_ACTIONS_HIDDEN_CLASS = "lite-more-actions__container--hidden"
    BUTTON_REACTIVATE_ID = "button-reactivate"
    BUTTON_DEACTIVATE_ID = "button-deactivate"
    BUTTON_REACTIVATE_CONFIRM_ID = "reactivate-confirm"
    BUTTON_DEACTIVATE_CONFIRM_ID = "deactivate-confirm"
    BUTTON_MORE_ACTIONS_ID = "button-more-actions"
    BUTTON_CHANGE_ROLE_ID = "button-edit"
    BUTTON_ASSIGN_SITES_ID = "button-assign-sites"

    def try_click_more_actions_button(self):
        if self.driver.find_elements_by_class_name(self.PANE_MORE_ACTIONS_HIDDEN_CLASS):
            self.driver.find_element_by_id(self.BUTTON_MORE_ACTIONS_ID).click()

    def click_deactivate_button(self):
        self.try_click_more_actions_button()
        self.driver.find_element_by_id(self.BUTTON_DEACTIVATE_ID).click()
        self.driver.find_element_by_id(self.BUTTON_DEACTIVATE_CONFIRM_ID).click()

    def click_reactivate_button(self):
        self.try_click_more_actions_button()
        self.driver.find_element_by_id(self.BUTTON_REACTIVATE_ID).click()
        self.driver.find_element_by_id(self.BUTTON_REACTIVATE_CONFIRM_ID).click()

    def click_assign_sites_button(self):
        self.try_click_more_actions_button()
        self.driver.find_element_by_id(self.BUTTON_ASSIGN_SITES_ID).click()

    def click_change_role_button(self):
        self.try_click_more_actions_button()
        self.driver.find_element_by_id(self.BUTTON_CHANGE_ROLE_ID).click()
