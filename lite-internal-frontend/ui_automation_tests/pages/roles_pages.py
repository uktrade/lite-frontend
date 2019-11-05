


class RolesPages():

    def __init__(self, driver):
        self.driver = driver
        self.add_role_text_field = "name"
        self.add_role_button = ".govuk-button[href*='roles/add']"

    def enter_role_name(self, text):
        self.driver.find_element_by_id(self.add_role_text_field).clear()
        self.driver.find_element_by_id(self.add_role_text_field).send_keys(text)

    def select_permissions(self, value):
        self.driver.find_element_by_id(value).click()

    def click_add_a_role_button(self):
        self.driver.find_element_by_id("button_add_role").click()

    def click_edit_for_default_role(self):
        self.driver.find_element_by_css_selector('[href*="000000000001/edit"]').click()

    def edit_default_role_to_have_permission(self, permission):
        if not self.driver.find_element_by_id(permission).is_selected():
            self.select_permissions(permission)

    def edit_default_role_to_have_all_permissions(self):
        elements = self.driver.find_elements_by_css_selector(".govuk-checkboxes__input")
        for element in elements:
            if not element.is_selected():
                element.click()

    def remove_all_permissions_from_default_role(self):
        elements = self.driver.find_elements_by_css_selector(".govuk-checkboxes__input")
        for element in elements:
            if element.is_selected():
                element.click()

    def current_permissions_count_for_default(self):
        elements = self.driver.find_elements_by_css_selector(".govuk-table__body .govuk-table__row")[0]
        permissions = elements.find_elements_by_css_selector(".lite-tick-cross-list li")
        role_permissions = 0
        for permission in permissions:
            if 'can' in permission.text:
                role_permissions += 1
        return role_permissions
