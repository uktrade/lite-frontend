import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import helpers.helpers as utils


class ExporterHub():

    # called every time you create an object for this class
    def __init__(self, driver):
        self.driver = driver
        self.apply_for_a_licence_btn = "a[href*='/apply-for-a-licence/']"
        self.drafts_btn = "a[href*='/drafts/']"
        self.applications_btn = "a[href*='/applications/']"
        self.my_goods_btn = "a[href*='/goods/']"  # css
        self.add_a_good_btn = "a[href*='/goods/add/']"
        self.users_btn = "a[href='/users/']"
        self.sites_btn = "a[href='/sites/']"
        self.sites_link = "a[href*='sites']"
        self.name_or_reference_input_id = "name"
        self.control_code_input_id = "control_code"
        self.destination_input_id = "destination"
        self.usage_input_id = "usage"
        self.activity_input_id = "activity"
        self.standard_licence_button = "input#licence_type-standard_licence"
        self.open_licence_button = "input#licence_type-open_licence"
        self.submit_button = "button[type*='submit']"
        self.export_button = "export_type-"
        self.export_licence_yes_or_no = "have_you_been_informed-"
        self.reference_number = "reference_number_on_information_form"
        self.licence_application_headers = ".govuk-table__header"
        self.success_message = ".govuk-panel__title"
        self.licence_application_values = ".govuk-table__cell"
        self.start_now_btn = "a[href*='/start']"
        self.application_is_submitted = '.govuk-panel__title'
        self.delete_application_button = '.cancel-link'  # css
        self.goods_link = "goods"  # id
        self.goods_tile = "a[href*='/goods/']"
        self.sites_link = "a[href*='sites']"
        self.quantity_field = 'quantity'  # id
        self.unit_dropdown = 'unit'  # id
        self.value_field = 'value'  # id
        self.overview_link = '.govuk-back-link' # css
        self.organisation_or_external_radio_button = "organisation_or_external-"
        self.sites_checkbox = ".govuk-checkboxes__input"
        self.type_choices = "type-"
        self.location_link = "location"
        self.end_user_link = "end_users"
        self.ultimate_end_users_link = "ultimate_end_users"
        self.new_sites_link = ".govuk-button[href*='new']"
        self.name = "name"
        self.address_line_1 = "address.address_line_1"
        self.postcode = "address.postcode"
        self.city = "address.city"
        self.region = "address.region"
        self.country = "address.country"


    def click_apply_for_a_licence(self):
        self.driver.find_element_by_css_selector(self.apply_for_a_licence_btn).click()

    def click_applications(self):
        self.driver.find_element_by_css_selector(self.applications_btn).click()

    def enter_email(self, email):
        email_tb = self.driver.find_element_by_name("login")
        email_tb.clear()
        email_tb.send_keys(email)

    def enter_password(self, password):
        password_tb = self.driver.find_element_by_name("password")
        password_tb.send_keys(password)

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.driver.find_element_by_class_name("button").click()
        time.sleep(1)

    def click_submit(self):
        self.driver.find_element_by_class_name("govuk-button").click()

    def click_goods_button(self, ):
        self.driver.find_element_by_css_selector(self.my_goods_btn).click()

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector("button[type*='submit']").click()

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

    def click_user_profile(self):
        self.driver.find_element_by_css_selector("a[href*='/users/profile/']").click()

    def click_sites(self):
        self.driver.find_element_by_css_selector(self.sites_btn).click()

    def click_new_site(self):
        self.driver.find_element_by_css_selector("a[href*='/sites/new/']").click()

    def get_text_of_site(self, int):
        return self.driver.find_elements_by_css_selector(".govuk-checkboxes__label")[int].text

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

    #def click_submit_application(self):
     #   self.driver.find_element_by_css_selector("button[type*='submit']").click()

    # Old flow
    def create_application(self, name, destination, usage, activity):
        self.click_apply_for_a_licence()
        self.click_start()
        self.enter_name_for_application(name)
        self.click_save_and_continue()
        self.enter_destination(destination)
        self.click_save_and_continue()
        self.enter_usage(usage)
        self.click_save_and_continue()
        self.enter_activity(activity)
        self.click_submit()


    def enter_name_or_reference_for_application(self, name):
        self.driver.find_element_by_id(self.name_or_reference_input_id).clear()
        self.driver.find_element_by_id(self.name_or_reference_input_id).send_keys(name)

    def click_start_now_btn(self):
        self.driver.find_element_by_css_selector(self.start_now_btn).click()


    def click_submit_application(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def click_continue(self):
        self.click_save_and_continue()

    def click_go_to_overview(self):
        self.driver.find_element_by_xpath("//a[text()[contains(.,'Overview')]]").click()

    def click_delete_application(self):
        self.driver.find_element_by_css_selector(self.delete_application_button).click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_css_selector(".govuk-button--warning").click()

    def click_goods_tile(self):
        utils.wait_until_page_is_loaded(self.driver)
        element = self.driver.find_element_by_css_selector(self.goods_tile)
        self.driver.execute_script("arguments[0].click();", element)

    def click_add_from_organisations_goods(self):
        self.driver.find_element_by_xpath("//*[text()[contains(.,'Add from organisations goods')]]").click()

    def add_good_to_application(self, des):
        good = self.driver.find_element_by_xpath("//div[@class='lite-card']/h4[text()='" + des + "']")
        # goods = self.driver.find_elements_by_xpath("//div[@class='lite-card']")
        # for good in goods:
        #     if good.find_element(By.TAG_NAME, "h4").text == des:
        good.find_element(By.XPATH, "./following::div[1]/a[text()='Add to application']").click()

    def enter_quantity(self, qty):
        self.driver.find_element_by_id("quantity").clear()
        self.driver.find_element_by_id("quantity").send_keys(qty)

    def enter_value(self, value):
        self.driver.find_element_by_id("value").clear()
        self.driver.find_element_by_id("value").send_keys(value)

    def select_unit_of_measurement(self, unit):
        select = Select(self.driver.find_element_by_id('unit'))
        select.select_by_visible_text(unit)

    def enter_description(self, description):
        self.driver.find_element_by_id("description").clear()
        self.driver.find_element_by_id("description").send_keys(description)


    def click_filter_btn(self):
        self.driver.find_element_by_xpath("//button[text()[contains(.,'Filter')]]").click()

    def click_permanent_or_temporary_button(self, string):
        self.driver.find_element_by_id(self.export_button + string).click()

    def click_export_licence_yes_or_no(self, string):
        self.driver.find_element_by_id(self.export_licence_yes_or_no + string).click()

    def get_text_of_application_headers(self, no):
        return self.driver.find_elements_by_css_selector(self.licence_application_headers)[no].text

    def get_text_of_application_results(self, no):
        return self.driver.find_elements_by_css_selector(self.licence_application_values)[no].text

    def click_export_licence(self, string):
        if (string == "standard"):
            self.driver.find_element_by_css_selector(self.standard_licence_button).click()
        elif (string == "open"):
            self.driver.find_element_by_css_selector(self.open_license_button).click()

    def get_text_of_success_message(self):
        return self.driver.find_element_by_css_selector(self.success_message).text

    def type_into_reference_number(self, string):
        self.driver.find_element_by_id(self.reference_number).send_keys(string)

    def enter_application_details_new(self, name, licence_type, temp_or_perm, need_licence, ref_number):
        self.enter_name_or_reference_for_application(name)
        self.click_save_and_continue()
        self.click_export_licence(licence_type)
        self.click_continue()
        self.click_permanent_or_temporary_button(temp_or_perm)
        self.click_continue()
        self.click_export_licence_yes_or_no(need_licence)
        self.type_into_reference_number(ref_number)

    def application_submitted_text(self):
        return self.driver.find_element_by_css_selector(self.application_is_submitted).text

    def click_goods_link(self):
        element = self.driver.find_element_by_id(self.goods_link)
        self.driver.execute_script("arguments[0].click();", element)

    def click_add_a_good(self):
        utils.wait_until_page_is_loaded(self.driver)
        self.driver.find_element_by_css_selector(self.add_a_good_btn).click()

    def enter_description_of_goods(self, description):
        description_tb = self.driver.find_element_by_id("description")
        description_tb.clear()
        description_tb.send_keys(description)

    def select_is_your_good_controlled(self, option):
        if option == "Yes":
            self.driver.find_element_by_id("is_good_controlled-yes").click()
        else:
            self.driver.find_element_by_id("is_good_controlled-no").click()

    def enter_control_code(self, code):
        control_code_tb = self.driver.find_element_by_id("control_code")
        control_code_tb.clear()
        control_code_tb.send_keys(code)

    def select_is_your_good_intended_to_be_incorporated_into_an_end_product(self, option):
        if option == "Yes":
            self.driver.find_element_by_id("is_good_end_product-no").click()
        else:
            self.driver.find_element_by_id("is_good_end_product-yes").click()

    def enter_part_number(self, part_number):
        part_number_tb = self.driver.find_element_by_id("part_number")
        part_number_tb.clear()
        part_number_tb.send_keys(part_number)

    def add_values_to_good(self, value, quantity, unit):
        self.driver.find_element_by_id(self.value_field).send_keys(value)
        self.driver.find_element_by_id(self.quantity_field).send_keys(quantity)
        select = Select(self.driver.find_element_by_id(self.unit_dropdown))
        select.select_by_visible_text(unit)

    def click_on_overview(self):
        self.driver.find_element_by_css_selector(self.overview_link).click()

    def click_on_organisation_or_external_radio_button(self, string):
        self.driver.find_element_by_id(self.organisation_or_external_radio_button + string).click()

    def click_sites_link(self):
        self.driver.find_element_by_css_selector(self.sites_link).click()

    def enter_end_user_name(self, name):
        name_tb = self.driver.find_element_by_id("name")
        name_tb.clear()
        name_tb.send_keys(name)

    def enter_end_user_address(self, address):
        address_tb = self.driver.find_element_by_id("address")
        address_tb.clear()
        address_tb.send_keys(address)

    def enter_end_user_website(self, website):
        address_tb = self.driver.find_element_by_id("website")
        address_tb.clear()
        address_tb.send_keys(website)

    def enter_end_user_country(self, country):
        country_tb = self.driver.find_element_by_id("country")
        country_tb.clear()
        country_tb.send_keys(country)
        self.driver.find_element_by_id("country").send_keys(Keys.RETURN)

    def select_end_user_type(self, string):
        self.driver.find_element_by_id(self.type_choices + string).click()

    def click_application_locations_link(self):
        self.driver.execute_script("document.getElementById('" + self.location_link + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.location_link).click()

    def click_sites_checkbox(self, no):
        self.driver.find_elements_by_css_selector(self.sites_checkbox)[no].click()

    def click_end_user_link(self):
        element = self.driver.find_element_by_id(self.end_user_link)
        self.driver.execute_script("arguments[0].click();", element)

    def click_ultimate_end_user_link(self):
        element = self.driver.find_element_by_id(self.ultimate_end_users_link)
        self.driver.execute_script("arguments[0].click();", element)

    def click_add_ultimate_end_user(self):
        element = self.driver.find_element_by_css_selector("a[href*='add']")
        self.driver.execute_script("arguments[0].click();", element)

    def click_new_sites_link(self):
        self.driver.find_element_by_css_selector(self.new_sites_link).click()

    def enter_info_for_new_site(self, name, address, postcode, city, region, country):
        self.driver.find_element_by_id(self.name).send_keys(name)
        self.driver.find_element_by_id(self.address_line_1).send_keys(address)
        self.driver.find_element_by_id(self.postcode).send_keys(postcode)
        self.driver.find_element_by_id(self.city).send_keys(city)
        self.driver.find_element_by_id(self.region).send_keys(region)
        self.driver.find_element_by_id(self.country).send_keys(country)
        self.driver.find_element_by_id(self.country).send_keys(Keys.ENTER)