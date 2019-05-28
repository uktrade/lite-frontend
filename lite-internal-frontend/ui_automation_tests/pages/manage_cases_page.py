from selenium.webdriver.support.ui import Select
import time


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

    def click_go_to_queue_button(self):
        self.driver.find_element_by_css_selector(self.go_to_queue_btn).click()

    def click_progress_application(self):
        progress_app_btn = self.driver.find_element_by_xpath("//*[text()[contains(.,'Progress')]]")
        progress_app_btn.click()

    def select_status(self, status):
        case_status_dropdown = Select(self.driver.find_element_by_id('status'))
        time.sleep(1)
        case_status_dropdown.select_by_visible_text(status)

    def enter_case_note(self, text):
        self.driver.find_element_by_id("case_note").send_keys(text)

    def click_post_note_btn(self):
        self.driver.find_element_by_id("button-post-note").click()

    def click_cancel_btn(self):
        self.driver.find_element_by_id("case-note-cancel-button").click()

    def get_case_note_warning(self):
        time.sleep(1)
        return self.driver.find_element_by_id("case_note-warning").text

    def click_save(self):
        save_btn = self.driver.find_element_by_xpath("//button[text()[contains(.,'Save')]]")
        save_btn.click()
