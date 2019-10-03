from helpers.wait import wait_until_page_is_loaded, wait_until_menu_is_visible


class HeaderPage():

    def __init__(self, driver):
        self.driver = driver
        self.menu_button = "lite-user-menu-button" #id

    def click_lite_menu(self):
        wait_until_page_is_loaded(self.driver)
        self.driver.find_element_by_id(self.menu_button).click()
        wait_until_menu_is_visible(self.driver)

    def click_organisations(self):
        self.driver.find_element_by_css_selector("a[href*='/organisations/']").click()

    def click_hmrc(self):
        self.driver.find_element_by_css_selector("a[href*='/hmrc/']").click()

    def click_teams(self):
        self.driver.find_element_by_css_selector("a[href*='/teams/']").click()

    def click_users(self):
        self.driver.find_element_by_css_selector("a[href*='/users/']").click()

    def open_users(self):
        self.click_lite_menu()
        self.click_users()

    def click_user_profile(self):
        self.driver.find_element_by_css_selector(".lite-user-menu-button--user").click()

    def click_flags(self):
        self.driver.find_element_by_css_selector("a[href*='/flags/']").click()

    def click_queues(self):
        self.driver.find_element_by_css_selector("a[href*='/queues/']").click()

    def click_my_team(self):
        self.driver.find_element_by_css_selector("a[href='/team']").click()
