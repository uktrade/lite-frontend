from selenium.webdriver.support.ui import Select
class ManageCasesPage():

    # called e time you create an object for this class
    def __init__(self, driver):
        self.driver = driver

        self.queue_drop_down = "a[href*='/new-application/']"
        self.go_to_queue_btn = "button.govuk-button"

    def select_from_queue_drop_down(self, value):
        select = Select(self.find_element_by_name('queue'))
        select.select_by_visible_text(value)

    def click_go_to_queue_button(self):
        self.driver.find_element_by_css_selector(self.go_to_queue_btn).click()
