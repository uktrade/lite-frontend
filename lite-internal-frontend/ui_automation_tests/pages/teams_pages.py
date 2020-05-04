from pages.users_page import UsersPage
from shared.BasePage import BasePage


class TeamsPages(BasePage):
    ADD_TEAM_TEXT_FIELD = "name"  # ID
    ADD_TEAM_BUTTON = ".govuk-button[href*='teams/add']"  # CSS

    def enter_team_name(self, text):
        self.driver.find_element_by_id(self.ADD_TEAM_TEXT_FIELD).clear()
        return self.driver.find_element_by_id(self.ADD_TEAM_TEXT_FIELD).send_keys(text)

    def click_add_a_team_button(self):
        self.driver.find_element_by_css_selector(self.ADD_TEAM_BUTTON).click()

    def select_team_from_dropdown(self, team):
        users_page = UsersPage(self.driver)
        users_page.select_option_from_team_drop_down_by_visible_text(team)

    def select_default_queue_from_dropdown(self, queue):
        users_page = UsersPage(self.driver)
        users_page.select_option_from_default_queue_drop_down_by_visible_text(queue)
