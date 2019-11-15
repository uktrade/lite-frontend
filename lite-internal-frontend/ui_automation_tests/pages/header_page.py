from shared.tools.wait import wait_until_page_is_loaded, wait_until_menu_is_visible


class HeaderPage:
    def __init__(self, driver):
        self.driver = driver
        self.menu_button = "lite-user-menu-button"  # ID
        self.organisations_link = "a[href*='/organisations/']"  # CSS
        self.templates_link = "a[href*='/letter-templates/']"  # CSS
        self.hmrc_link = "a[href*='/hmrc/']"  # CSS
        self.teams_link = "a[href*='/teams/']"  # CSS
        self.users_link = "a[href*='/users/']"  # CSS
        self.flags_link = "a[href*='/flags/']"  # CSS
        self.queues_link = "a[href*='/queues/']"  # CSS
        self.my_team_link = "a[href='/team']"  # CSS
        self.user_profile = ".lite-user-menu-button--user"  # CSS

    def click_lite_menu(self):
        wait_until_page_is_loaded(self.driver)
        self.driver.find_element_by_id(self.menu_button).click()
        wait_until_menu_is_visible(self.driver)

    def click_organisations(self):
        self.driver.find_element_by_css_selector(self.organisations_link).click()

    def click_letters(self):
        self.driver.find_element_by_css_selector(self.templates_link).click()

    def click_hmrc(self):
        self.driver.find_element_by_css_selector(self.hmrc_link).click()

    def click_teams(self):
        self.driver.find_element_by_css_selector(self.teams_link).click()

    def click_users(self):
        self.driver.find_element_by_css_selector(self.users_link).click()

    def open_users(self):
        self.click_lite_menu()
        self.click_users()

    def click_user_profile(self):
        self.driver.find_element_by_css_selector(self.user_profile).click()

    def click_flags(self):
        self.driver.find_element_by_css_selector(self.flags_link).click()

    def click_queues(self):
        self.driver.find_element_by_css_selector(self.queues_link).click()

    def click_my_team(self):
        self.driver.find_element_by_css_selector(self.my_team_link).click()
