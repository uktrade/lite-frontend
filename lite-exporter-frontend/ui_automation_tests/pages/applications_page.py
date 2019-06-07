class ApplicationsPage():
    # /applications
    def __init__(self, driver):
        self.driver = driver

        self.apply_for_a_licence_btn = "a[href*='/apply_for_a_licence/']"
        self.refresh_btn = "a[href*='.']"


    def click_apply_for_a_licence_btn(self):
        self.driver.find_element_by_css_selector(self.apply_for_a_licence_btn).click()

    def click_refresh_btn(self):
        self.driver.find_element_by_css_selector(self.refresh_btn).click()
