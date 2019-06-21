class TeamsPages():

    def __init__(self, driver):
        self.driver = driver
        self.add_team_text_field = "name" #id
        self.add_team_button = ".govuk-button[href*='teams/add']" #css

    def enter_team_name(self, text):
        self.driver.find_element_by_id(self.add_team_text_field).clear()
        return self.driver.find_element_by_id(self.add_team_text_field).send_keys(text)

    def click_add_a_team_button(self):
        self.driver.find_element_by_css_selector(self.add_team_button).click()

