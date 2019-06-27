import datetime
from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from pages.apply_for_a_licence_page import ApplyForALicencePage
from pages.application_goods_type_list import ApplicationGoodsTypeList
from pages.application_overview_page import ApplicationOverviewPage
from pages.application_goods_list import ApplicationGoodsList
import helpers.helpers as utils
from pages.exporter_hub_page import ExporterHubPage
from pages.hub_page import Hub
from pages.shared import Shared
from conftest import context
from selenium.webdriver.common.by import By

scenarios('../features/submit_application.feature', strict_gherkin=False)

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@when('I click on apply for a license button')
def click_apply_licence(driver):
    exporter = ExporterHubPage(driver)
    exporter.click_apply_for_a_licence()


@then('I see the application overview')
def i_see_the_application_overview(driver):
    time_date_submitted = datetime.datetime.now().strftime("%I:%M%p").lstrip("0").replace(" 0", " ").lower() + datetime.datetime.now().strftime(" %d %B %Y")
    apply = ApplyForALicencePage(driver)
    assert apply.get_text_of_application_headers(0) == "Name"
    assert apply.get_text_of_application_headers(1) == "Licence Type"
    assert apply.get_text_of_application_headers(2) == "Export Type"
    assert apply.get_text_of_application_headers(3) == "Reference Number"
    assert apply.get_text_of_application_headers(4) == "Created at"
    assert apply.get_text_of_application_results(1) == context.type+"_licence"
    assert apply.get_text_of_application_results(2) == context.perm_or_temp
    assert apply.get_text_of_application_results(3) == context.ref
    # assert apply_for_licence.get_text_of_application_results(3) == datetime.datetime.now().strftime("%b %d %Y, %H:%M%p")
    assert time_date_submitted in apply.get_text_of_application_results(4), "Created date is incorrect on draft overview"
    app_id = driver.current_url[-36:]
    context.app_id = app_id


@when('I click drafts')
def i_click_drafts(driver):
    hub_page = Hub(driver)
    hub_page.click_drafts()


@when('I click applications')
def i_click_applications(driver):
    hub_page = Hub(driver)
    hub_page.click_applications()


@when('I delete the application')
def i_delete_the_application(driver):
    apply = ApplyForALicencePage(driver)
    apply.click_delete_application()
    assert 'Exporter Hub - LITE' in driver.title, "failed to go to Exporter Hub page after deleting application from application overview page"


@when('I click the application')
def i_click_the_application(driver):
    drafts_table = driver.find_element_by_class_name("govuk-table")
    drafts_table.find_element_by_xpath(".//td/a[contains(@href,'" + context.app_id + "')]").click()
    assert "Overview" in driver.title
    appName = driver.find_element_by_css_selector(".lite-persistent-notice .govuk-link").text
    assert "Test Application" in appName


@when('I submit the application')
def submit_the_application(driver):
    apply = ApplyForALicencePage(driver)
    apply.click_submit_application()
    assert apply.get_text_of_success_message() == "Application submitted"


@then('I see no sites or external sites attached error message')
def i_see_no_sites_attached_error(driver):
    shared = Shared(driver)
    assert "Cannot create an application with no goods attached" in shared.get_text_of_error_message()
    assert "Cannot create an application with no sites or external sites attached" in shared.get_text_of_error_message_at_position_2()


@then('I see good types error messages')
def i_see_no_sites_attached_error(driver):
    shared = Shared(driver)
    assert "This field may not be blank." in shared.get_text_of_error_message()
    assert "This field is required." in shared.get_text_of_error_message_at_position_2()
    assert "This field is required." in shared.get_text_of_error_message_at_position_3()


@when(parsers.parse('I click add to application for the good at position "{no}"'))
def click_add_to_application_button(driver, no):

    context.goods_name = driver.find_elements_by_css_selector('.lite-card .govuk-heading-s')[int(no)-1].text
    context.part_number = driver.find_elements_by_css_selector('.lite-card .govuk-label')[int(no)-1].text
    driver.find_elements_by_css_selector('a.govuk-button')[int(no)-1].click()


@then('I see enter valid quantity and valid value error message')
def valid_quantity_value_error_message(driver):
    shared = Shared(driver)
    assert "Error:\nEnter a valid value" in shared.get_text_of_error_message()
    assert "Error:\nEnter a valid quantity" in shared.get_text_of_error_message_at_position_2()


@when('I click on the goods link from overview')
def click_goods_link_overview(driver):
    overview_page = ApplicationOverviewPage(driver)
    driver.execute_script("document.getElementById('goods').scrollIntoView(true);")
    overview_page.click_goods_link()


@when(parsers.parse('I add values to my good of "{value}" quantity "{quantity}" and unit of measurement "{unit}"'))
def enter_values_for_good(driver, value, quantity, unit):
    context.quantity = quantity
    context.value = value
    context.unit = unit
    application_goods_list = ApplicationGoodsList(driver)
    application_goods_list.add_values_to_good(str(value), str(quantity), unit)


@then('good is added to application')
def good_is_added(driver):
    unit = str(context.unit)
    unit = unit.lower()
    assert utils.is_element_present(driver, By.XPATH, "//*[text()='" + str(context.goods_name) + "']")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()='" + str(context.quantity) + ".0 " + unit + "']")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()='£" + str(context.value) + "']")


@when('I click overview')
def click_overview(driver):
    application_goods_list = ApplicationGoodsList(driver)
    application_goods_list.click_on_overview()


@then('application is submitted')
def application_is_submitted(driver):
    apply = ApplyForALicencePage(driver)
    assert "Application submitted" in apply.application_submitted_text()


@then('I see submitted application')
def application_is_submitted(driver):
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + context.app_time_id + "')]]")
    log.info("application found in submitted applications list")

    # Check application status is Submitted
    log.info("verifying application status is Submitted")
    status = driver.find_element_by_xpath("//*[text()[contains(.,'" + context.app_time_id + "')]]/following-sibling::td[last()]")
    last_updated = driver.find_element_by_xpath("//*[text()[contains(.,'" + context.app_time_id + "')]]/following-sibling::td[last()-1]")
    goods = driver.find_element_by_xpath("//*[text()[contains(.,'" + context.app_time_id + "')]]/following-sibling::td[last()-2]")
    assert status.is_displayed()
    assert last_updated.is_displayed()
    assert goods.is_displayed()
    assert status.text == "Submitted", "Expected Status of application is to be 'Submitted' but is not"
    assert "Good" in goods.text
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Status')]]").is_displayed()
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Last Updated')]]").is_displayed()
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Goods')]]").is_displayed()
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Reference')]]").is_displayed()

    logging.info("Test Complete")


@then('I see the homepage')
def i_see_the_homepage(driver):
    assert 'Exporter Hub - LITE' in driver.title, "Delete Application link on overview page failed to go to Exporter Hub page"


@when('I click Add goods type button')
def click_goods_type_button(driver):
    goods_type_page = ApplicationGoodsTypeList(driver)
    goods_type_page.click_goods_type_button()


@then(parsers.parse('I see my goods type added at position "{position}" with a description and a control code'))
def i_see_the_goods_types_list(driver, position):
    goods_type_page = ApplicationGoodsTypeList(driver)
    good_type = goods_type_page.get_text_of_goods_type_info(int(position))
    assert context.good_description in good_type
    assert "Control Code: " + context.controlcode in good_type


@then('I see my goods type added to the overview page with a description and a control code')
def i_see_the_goods_types_list_overview(driver):
    goods_type_page = ApplicationGoodsTypeList(driver)
    good_type_table_overview = goods_type_page.get_text_of_goods_type_info_overview()
    assert "Description" in good_type_table_overview
    assert "Control Code" in good_type_table_overview
    assert context.good_description in good_type_table_overview
    assert context.controlcode in good_type_table_overview
