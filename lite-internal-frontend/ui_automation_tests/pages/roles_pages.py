class RolesPages:

    add_role_text_field = "name"  # ID
    add_role = "button_add_role"  # ID

    def __init__(self, driver):
        self.driver = driver

    def enter_role_name(self, text):
        self.driver.find_element_by_id(self.add_role_text_field).clear()
        self.driver.find_element_by_id(self.add_role_text_field).send_keys(text)

    def select_permissions(self, value):
        self.driver.find_element_by_id(value).click()

    def click_add_a_role_button(self):
        self.driver.find_element_by_id(self.add_role).click()
