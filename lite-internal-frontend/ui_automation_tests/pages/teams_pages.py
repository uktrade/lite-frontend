from selenium.webdriver.support.ui import Select

from shared.BasePage import BasePage


class TeamsPages(BasePage):
    ADD_TEAM_TEXT_FIELD = "name"  # ID
    ADD_TEAM_BUTTON = ".govuk-button[href*='teams/add']"  # CSS
    TEAM_DROPDOWN = "team"  # ID

    def enter_team_name(self, text):
        self.driver.find_element_by_id(self.ADD_TEAM_TEXT_FIELD).clear()
        return self.driver.find_element_by_id(self.ADD_TEAM_TEXT_FIELD).send_keys(text)

    def click_add_a_team_button(self):
        self.driver.find_element_by_css_selector(self.ADD_TEAM_BUTTON).click()

    def select_team_from_dropdown(self, team):
        select = Select(self.driver.find_element_by_id(self.TEAM_DROPDOWN))
        select.select_by_visible_text(team)
