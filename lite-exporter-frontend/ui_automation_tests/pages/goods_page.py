from pages.shared import Shared


class GoodsPage:

    # Selector for the edit/delete goods link in the table
    EDIT_LINK = '[href*="goods/edit"]'
    DELETE_LINK = '[href*="goods/delete"]'
    confirm_delete_id = 'delete'
    cancel_delete_id = 'cancel'

    # This is for the delete confirmation page
    DELETE_BUTTON = '.govuk-button--warning'

    def __init__(self, driver):
        self.driver = driver

    def click_on_goods_edit_link(self):
        self.driver.find_element_by_css_selector(self.EDIT_LINK).click()

    def click_on_delete_link(self):
        self.driver.find_element_by_css_selector(self.DELETE_BUTTON).click()

    def confirm_delete(self, confirm):
        shared = Shared(self.driver)
        shared.click_continue()
