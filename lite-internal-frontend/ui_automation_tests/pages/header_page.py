class HeaderPage():

    def __init__(self, driver):
        self.driver = driver
        self.menu_button = "lite-user-menu-button" #id

    def click_lite_menu(self):
        self.driver.find_element_by_id(self.menu_button).click()

    def click_organisations(self):
        self.driver.find_element_by_css_selector("a[href*='/organisations/']").click()

    def click_teams(self):
        self.driver.find_element_by_css_selector("a[href*='/teams/']").click()

    def click_users(self):
        self.driver.find_element_by_css_selector("a[href*='/users/']").click()

    def open_users(self):
        self.click_lite_menu()
        self.click_users()

    def click_user_profile(self):
        self.driver.find_element_by_css_selector(".lite-user-menu-button--user").click()
