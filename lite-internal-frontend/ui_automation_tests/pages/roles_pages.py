from helpers.BasePage import BasePage


class RolesPages(BasePage):

    ADD_ROLE_TEXT_FIELD = "name"  # ID
    ADD_ROLE = "button_add_role"  # ID

    def enter_role_name(self, text):
        self.driver.find_element_by_id(self.ADD_ROLE_TEXT_FIELD).clear()
        self.driver.find_element_by_id(self.ADD_ROLE_TEXT_FIELD).send_keys(text)

    def select_permissions(self, value):
        self.driver.find_element_by_id(value).click()

    def click_add_a_role_button(self):
        self.driver.find_element_by_id(self.ADD_ROLE).click()
