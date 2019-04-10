class ExporterHubPage():

    # called e time you create an object for this class
    def __init__(self, driver):
        self.driver = driver

        self.url = "https://lite-exporter-frontend-staging.london.cloudapps.digital/"
        self.apply_for_a_licence_btn = "a[href*='/new-application/']"
        self.drafts_btn = "a[href*='/drafts/']"
        self.applications_btn = "a[href*='/applications/']"

    def go_to(self):
        self.driver.get(self.url)

    def click_apply_for_a_licence(self):
        self.driver.find_element_by_css_selector(self.apply_for_a_licence_btn).click()

    def click_drafts(self):
        self.driver.find_element_by_css_selector(self.drafts_btn).click()

    def click_applications(self):
        self.driver.find_element_by_css_selector(self.applications_btn).click()


