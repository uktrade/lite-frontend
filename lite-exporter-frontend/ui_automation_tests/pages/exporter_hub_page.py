import time

from selenium.webdriver.common.action_chains import ActionChains


class ExporterHubPage:

    def __init__(self, driver):
        self.driver = driver

        self.apply_for_a_licence_btn = "a[href*='/apply-for-a-licence/']"
        self.drafts_btn = "a[href*='/drafts/']"
        self.applications_btn = "a[href*='/applications/']"
        self.my_goods_btn = "a[href*='/goods/']"
        self.add_a_good_btn = "a[href*='/goods/add/']"
        self.users_btn = "a[href='/users/']"
        self.sites_btn = "a[href='/sites/']"
        self.sites_link = "a[href*='sites']"
        self.goods_tile = "a[href*='sites']"

    def go_to(self, url):
        self.driver.get(url)

    def click_apply_for_a_licence(self):
        self.driver.find_element_by_css_selector(self.apply_for_a_licence_btn).click()

    def click_drafts(self):
        self.driver.find_element_by_css_selector(self.drafts_btn).click()

    def click_applications(self):
        self.driver.find_element_by_css_selector(self.applications_btn).click()

    def enter_email(self, email):
        email_tb = self.driver.find_element_by_name("login")
        email_tb.clear()
        email_tb.send_keys(email)

    def enter_add_user_email(self, email):
        email_tb = self.driver.find_element_by_name("email")
        email_tb.clear()
        email_tb.send_keys(email)

    def enter_password(self, password):
        password_tb = self.driver.find_element_by_name("password")
        password_tb.send_keys(password)

    def login(self, email, password):
        if "logout" in self.driver.current_url:
            self.driver.find_element_by_xpath("//a[text()[contains(.,'Log In')]]").click()
        self.enter_email(email)
        self.enter_password(password)
        self.driver.find_element_by_class_name("button").click()
        time.sleep(1)

    def click_submit(self):
        self.driver.find_element_by_class_name("govuk-button").click()

    def click_my_goods(self):
        self.driver.find_element_by_css_selector(self.my_goods_btn).click()

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector("button[type*='submit']").click()

    def verify_good_is_in_goods_list(self, description, part_number, control_code):
        goods_row = self.driver.find_element_by_xpath("//*[text()[contains(.,'" + description + "')]]")
        assert goods_row.is_displayed()
        assert goods_row.find_element_by_xpath(".//following-sibling::td").text == part_number
        assert goods_row.find_element_by_xpath(".//following-sibling::td[2]").text == control_code

    def click_users(self):
        self.driver.find_element_by_css_selector(self.users_btn).click()

    def click_add_a_user_btn(self):
        self.driver.find_element_by_css_selector("a[href*='/users/add']").click()

    def enter_first_name(self, first_name):
        self.driver.find_element_by_id("first_name").clear()
        self.driver.find_element_by_id("first_name").send_keys(first_name)

    def enter_last_name(self, last_name):
        self.driver.find_element_by_id("last_name").clear()
        self.driver.find_element_by_id("last_name").send_keys(last_name)

    def click_edit_for_user(self, user_name):
        element = self.driver.find_element_by_xpath("//*[text()[contains(.,'" + user_name + "')]]/following-sibling::td[last()]/a")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(1)
        element.click()

    def click_user_name_link(self, user_name):
        element = self.driver.find_element_by_xpath("//*[text()[contains(.,'" + user_name + "')]]")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(1)
        element.click()

    def click_deactivate_btn(self):
        self.driver.find_element_by_xpath("//*[text()[contains(.,'Deactivate')]]").click()
        self.driver.find_element_by_xpath("//*[text()[contains(.,'Deactivate User')]]").click()

    def click_reactivate_btn(self):
        self.driver.find_element_by_xpath("//*[text()[contains(.,'Reactivate')]]").click()
        self.driver.find_element_by_xpath("//*[text()[contains(.,'Reactivate User')]]").click()

    def logout(self):
        self.driver.get("https://great.uat.uktrade.io/sso/accounts/")
        self.driver.find_element_by_id("header-sign-out-link").click()
        self.driver.find_element_by_css_selector('.button').click()

    def click_user_profile(self):
        self.driver.find_element_by_css_selector("a[href*='/users/profile/']").click()

    def click_sites(self):
        self.driver.find_element_by_css_selector(self.sites_btn).click()

    def click_new_site(self):
        self.driver.find_element_by_css_selector("a[href*='/sites/new/']").click()

    def get_text_of_site(self, int):
        return self.driver.find_elements_by_css_selector(".govuk-checkboxes__label")[int].text

    def click_submit(self):
        self.driver.find_element_by_css_selector(".govuk-button").click()

    def click_start(self):
        self.driver.find_element_by_css_selector("a[href*='/start']").click()

    def enter_name_for_application(self, name):
        self.driver.find_element_by_id("name").clear()
        self.driver.find_element_by_id("name").send_keys(name)

    def enter_destination(self, destination):
        self.driver.find_element_by_id("destination").clear()
        self.driver.find_element_by_id("destination").send_keys(destination)

    def enter_usage(self, usage):
        self.driver.find_element_by_id("usage").clear()
        self.driver.find_element_by_id("usage").send_keys(usage)

    def enter_activity(self, activity):
        self.driver.find_element_by_id("activity").clear()
        self.driver.find_element_by_id("activity").send_keys(activity)

    def return_number_of_notifications(self):
        text_of_new_notifications = self.driver.find_element_by_css_selector('.lite-tiles [href="/applications/"] p').text
        total_of_notifications = int((text_of_new_notifications.split('have '))[1].split(' new')[0])
        return total_of_notifications

