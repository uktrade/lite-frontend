from ui_tests.caseworker.pages.BasePage import BasePage
from tests_common.tools.wait import wait_until_page_is_loaded

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class HeaderPage(BasePage):
    MENU_BUTTON = "link-menu"  # ID
    ORGANISATIONS_LINK = "a[href*='/organisations/']"  # CSS
    TEMPLATES_LINK = "a[href*='/document-templates/']"  # CSS
    TEAMS_LINK = "a[href*='/teams/']"  # CSS
    USERS_LINK = "a[href*='/users/']"  # CSS
    FLAGS_LINK = "a[href*='/flags/']"  # CSS
    QUEUES_LINK = "a[href*='/queues/']"  # CSS
    MY_TEAM_LINK = "a[href='/team']"  # CSS

    def click_lite_menu(self):
        wait_until_page_is_loaded(self.driver)
        self.driver.find_element(by=By.ID, value=self.MENU_BUTTON).click()

    def click_organisations(self):
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, self.ORGANISATIONS_LINK))
        ).click()

    def click_letters(self):
        self.driver.find_element_by_css_selector(self.TEMPLATES_LINK).click()

    def click_teams(self):
        self.driver.find_element_by_css_selector(self.TEAMS_LINK).click()

    def click_users(self):
        self.driver.find_element_by_css_selector(self.USERS_LINK).click()

    def open_users(self):
        self.click_lite_menu()
        self.click_users()

    def click_flags(self):
        self.driver.find_element_by_css_selector(self.FLAGS_LINK).click()

    def click_queues(self):
        self.driver.find_element_by_css_selector(self.QUEUES_LINK).click()

    def click_my_team(self):
        self.driver.find_element_by_css_selector(self.MY_TEAM_LINK).click()
