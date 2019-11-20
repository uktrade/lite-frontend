from helpers.BasePage import BasePage
from shared.tools.wait import wait_until_page_is_loaded, wait_until_menu_is_visible


class HeaderPage(BasePage):
    MENU_BUTTON = "lite-user-menu-button"  # ID
    ORGANISATIONS_LINK = "a[href*='/organisations/']"  # CSS
    TEMPLATES_LINK = "a[href*='/letter-templates/']"  # CSS
    HMRC_LINK = "a[href*='/hmrc/']"  # CSS
    TEAMS_LINK = "a[href*='/teams/']"  # CSS
    USERS_LINK = "a[href*='/users/']"  # CSS
    FLAGS_LINK = "a[href*='/flags/']"  # CSS
    QUEUES_LINK = "a[href*='/queues/']"  # CSS
    MY_TEAM_LINK = "a[href='/team']"  # CSS
    USER_PROFILE = ".lite-user-menu-button--user"  # CSS

    def click_lite_menu(self):
        wait_until_page_is_loaded(self.driver)
        self.driver.find_element_by_id(self.MENU_BUTTON).click()
        wait_until_menu_is_visible(self.driver)

    def click_organisations(self):
        self.driver.find_element_by_css_selector(self.ORGANISATIONS_LINK).click()

    def click_letters(self):
        self.driver.find_element_by_css_selector(self.TEMPLATES_LINK).click()

    def click_hmrc(self):
        self.driver.find_element_by_css_selector(self.HMRC_LINK).click()

    def click_teams(self):
        self.driver.find_element_by_css_selector(self.TEAMS_LINK).click()

    def click_users(self):
        self.driver.find_element_by_css_selector(self.USERS_LINK).click()

    def open_users(self):
        self.click_lite_menu()
        self.click_users()

    def click_user_profile(self):
        self.driver.find_element_by_css_selector(self.USER_PROFILE).click()

    def click_flags(self):
        self.driver.find_element_by_css_selector(self.FLAGS_LINK).click()

    def click_queues(self):
        self.driver.find_element_by_css_selector(self.QUEUES_LINK).click()

    def click_my_team(self):
        self.driver.find_element_by_css_selector(self.MY_TEAM_LINK).click()
