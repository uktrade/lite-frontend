class ExporterHub():

    # called e time you create an object for this class
    def __init__(self, driver):
        self.driver = driver

        self.url = "https://lite-exporter-frontend-dev.london.cloudapps.digital/"

    def go_to(self):
        self.driver.get(self.url)

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector("button[action*='submit']").click()

    def click_submit_application(self):
        self.driver.find_element_by_css_selector("button[type*='submit']").click()
