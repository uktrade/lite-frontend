import datetime
from pytest_bdd import when, then, parsers, scenarios
from pages.apply_for_a_licence_page import ApplyForALicencePage
from pages.application_goods_type_list import ApplicationGoodsTypeList
from pages.add_end_user_pages import AddEndUserPages
from pages.application_overview_page import ApplicationOverviewPage
from pages.application_goods_list import ApplicationGoodsList
import helpers.helpers as utils
from pages.exporter_hub_page import ExporterHubPage
from pages.hub_page import Hub
from pages.shared import Shared
from pages.header import Header

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


#from core.builtins.custom_tags import get_string
#from core.services import get_countries
from helpers.helpers import find_element_by_href
from pages.application_countries_list import ApplicationCountriesList

from helpers.helpers import get_element_index_by_text

scenarios('../features/submit_application.feature', strict_gherkin=False)

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@when('I click on apply for a license button')
def click_apply_licence(driver, add_a_good):
    exporter = ExporterHubPage(driver)
    exporter.click_apply_for_a_licence()


@then('I see the application overview')
def i_see_the_application_overview(driver, context):
    time_date_submitted = datetime.datetime.now().strftime("%I:%M%p").lstrip("0").replace(" 0", " ").lower() + datetime.datetime.now().strftime(" %d %B %Y")
    apply = ApplyForALicencePage(driver)

    element = driver.find_element_by_css_selector(".govuk-table").text

    assert "Name" in element
    assert "Licence type" in element
    assert "Export type" in element
    assert "Reference Number" in element
    assert "Created at" in element
    assert context.type + "_licence" in element
    assert context.perm_or_temp in element
    assert context.ref in element

    # This can break if the minute changes between the five lines of code
    assert datetime.datetime.now().strftime("%M%p %d %B %Y").lower() in element.lower()

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
    assert 'Exporter hub - LITE' in driver.title, "failed to go to Exporter Hub page after deleting application from application overview page"


@when('I click countries')
def i_click_countries(driver):
    apply = ApplyForALicencePage(driver)
    apply.click_countries()


@when('I click the application')
def i_click_the_application(driver, context):
    drafts_table = driver.find_element_by_class_name("govuk-table")
    drafts_table.find_element_by_xpath(".//td/a[contains(@href,'" + context.app_id + "')]").click()
    assert "Overview" in driver.title
    app_name = Header(driver).get_text_of_app_name_in_header()
    assert "Test Application" in app_name


@when('I submit the application')
def submit_the_application(driver, context):
    apply = ApplyForALicencePage(driver)
    apply.click_submit_application()
    assert apply.get_text_of_success_message() == "Application submitted"
    context.time_date_submitted = datetime.datetime.now().strftime("%I:%M%p").lstrip("0").replace(" 0", " ").lower() + datetime.datetime.now().strftime(" %d %B %Y")


@then('I see no goods external sites or end user attached error message')
def i_see_no_sites_attached_error(driver):
    shared = Shared(driver)
    assert "Cannot create an application with no goods attached" in shared.get_text_of_error_message()
    assert "Cannot create an application with no sites or external sites attached" in shared.get_text_of_error_message(1)
    assert "Cannot create an application without an end user" in shared.get_text_of_error_message(2)


@then('I see no ultimate end user attached error message')
def i_see_no_ultimate_end_user_attached_error(driver):
    shared = Shared(driver)
    assert "Cannot create an application with no ultimate end users set when there is a good which is to be incorporated into an end product" in shared.get_text_of_error_message(2)


@then('I see no sites good types or countries attached error message')
def i_see_open_licence_error(driver):
    shared = Shared(driver)
    assert "Cannot create an application with no good descriptions attached" in shared.get_text_of_error_message()
    assert "Cannot create an application with no sites or external sites attached" in shared.get_text_of_error_message(1)
    assert "Cannot create an application without countries being set" in shared.get_text_of_error_message(2)


@then('I see good types error messages')
def goods_type_errors(driver):
    shared = Shared(driver)
    assert "This field may not be blank." in shared.get_text_of_error_message()
    assert "This field is required." in shared.get_text_of_error_message(1)
    assert "This field is required." in shared.get_text_of_error_message(2)


@when(parsers.parse('I click add to application for the good at position "{no}"'))
def click_add_to_application_button(driver, no, context):
    context.goods_name = driver.find_elements_by_css_selector('.lite-card .govuk-heading-s')[int(no)-1].text
    context.part_number = driver.find_elements_by_css_selector('.lite-card .govuk-label')[int(no)-1].text
    driver.find_elements_by_css_selector('a.govuk-button')[int(no)-1].click()


@then('I see enter valid quantity and valid value error message')
def valid_quantity_value_error_message(driver):
    shared = Shared(driver)
    assert "A valid number is required." in shared.get_text_of_error_message()
    assert "Enter a valid quantity" in shared.get_text_of_error_message(1)
    assert "Select a unit" in shared.get_text_of_error_message(2)


@when('I click on the goods link from overview')
def click_goods_link_overview(driver):
    overview_page = ApplicationOverviewPage(driver)
    driver.execute_script("document.getElementById('goods').scrollIntoView(true);")
    overview_page.click_goods_link()


@when(parsers.parse('I add values to my good of "{value}" quantity "{quantity}" and unit of measurement "{unit}"'))
def enter_values_for_good(driver, value, quantity, unit, context):
    context.quantity = quantity
    context.value = value
    context.unit = unit
    application_goods_list = ApplicationGoodsList(driver)
    application_goods_list.add_values_to_good(str(value), str(quantity), unit)


@then('good is added to application')
def good_is_added(driver, context):
    unit = str(context.unit)
    unit = unit.lower()
    assert utils.is_element_present(driver, By.XPATH, "//*[text()='" + str(context.goods_name) + "']")
    # TODO put this back when bug is fixed - showing mtr instead of metres
    #assert utils.is_element_present(driver, By.XPATH, "//*[text()='" + str(context.quantity) + ".0 " + unit + "']")
    if "." not in context.value:
        assert utils.is_element_present(driver, By.XPATH, "//*[text()='£" + str(context.value) + ".00']")
    else:
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
def application_is_submitted(driver, context):
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + context.app_time_id + "')]]")
    log.info("application found in submitted applications list")

    # Check application status is Submitted
    log.info("verifying application status is Submitted")

    elements = driver.find_elements_by_css_selector('tr')
    element_number = get_element_index_by_text(elements, context.app_time_id)
    element_row = elements[element_number].text
    assert "Submitted" in element_row
    assert context.time_date_submitted.split(":")[1] in element_row
    assert "0 Goods" or "1 Good" or "2 Goods" in element_row
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Status')]]").is_displayed()
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Last updated')]]").is_displayed()
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Goods')]]").is_displayed()
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Reference')]]").is_displayed()

    logging.info("Test Complete")


@then('I see the homepage')
def i_see_the_homepage(driver):
    assert 'Exporter hub - LITE' in driver.title, "Delete Application link on overview page failed to go to Exporter Hub page"


@when('I click Add goods type button')
def click_goods_type_button(driver):
    goods_type_page = ApplicationGoodsTypeList(driver)
    goods_type_page.click_goods_type_button()


@then(parsers.parse('I see my goods type added at position "{position}" with a description and a control code'))
def i_see_the_goods_types_list(driver, position, context):
    goods_type_page = ApplicationGoodsTypeList(driver)
    good_type = goods_type_page.get_text_of_goods_type_info(int(position))
    assert context.good_description in good_type
    assert "Control list classification: " + context.control_code in good_type


@then('I see my goods type added to the overview page with a description and a control code')
def i_see_the_goods_types_list_overview(driver, context):
    goods_type_page = ApplicationGoodsTypeList(driver)
    good_type_table_overview = goods_type_page.get_text_of_goods_type_info_overview()
    assert "Description" in good_type_table_overview
    assert "Control List Classification" in good_type_table_overview
    assert context.good_description in good_type_table_overview
    assert context.control_code in good_type_table_overview


@when('I click on countries')
def i_click_on_countries(driver):
    page = ApplicationOverviewPage(driver)
    page.click_countries_link()


@then('I should see a list of countries')
def i_should_see_a_list_of_countries(driver):
    application_countries_list = ApplicationCountriesList(driver)
    page_countries = application_countries_list.get_countries_names()
 #   api_data, status_code = get_countries(None)
    assert len(page_countries) == 274
 #   assert len(page_countries) == len(api_data['countries'])
    assert driver.find_element_by_tag_name("h2").text == "Where are your goods going?", \
        "Failed to go to countries list page"


@when(parsers.parse('I select "{country}" from the country list'))
def i_select_country_from_the_country_list(driver, country):
    application_countries_list = ApplicationCountriesList(driver)
    application_countries_list.select_country(country)

    assert find_element_by_href(driver, '#' + country).is_displayed()


@then(parsers.parse('I can see "{country_count}" countries selected on the overview page'))
def i_can_see_the_country_count_countries_selected_on_the_overview_page(driver, country_count):
    assert ApplicationOverviewPage(driver).get_text_of_countries_selected() == country_count + ' Countries Selected'


@when('I click on number of countries on the overview page')
def click_on_number_of_countries_selected(driver):
    utils.scroll_down_page(driver, 0, 1080)
    ApplicationOverviewPage(driver).click_on_countries_selected()


@when('I close the modal')
def close_modal(driver):
    ApplicationOverviewPage(driver).click_on_modal_close()


@when(parsers.parse('I search for country "{country}"'))
def search_for_country(driver, country):
    ApplicationCountriesList(driver).search_for_country(country)


@then(parsers.parse('only "{country}" is displayed in country list'))
def search_country_result(driver, country):
    assert country == ApplicationCountriesList(driver).get_text_of_countries_list(), \
        "Country not searched correctly"


@then(parsers.parse('I see "{country}" in a modal'))
def selected_countries_in_modal(driver, country):
    assert country in ApplicationOverviewPage(driver).get_text_of_country_modal_content(), \
        "Country not added to modal"


@when(parsers.parse('I add end user of type: "{type}"'))
def add_new_end_user_type(driver, type, context):
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.select_type(type)
    context.type_end_user = type
    add_end_user_pages.click_continue()


@when(parsers.parse('I add end user of name: "{name}"'))
def add_new_end_user_name(driver, name, context):
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.enter_name(name)
    context.name_end_user = name
    add_end_user_pages.click_continue()


@when(parsers.parse('I add end user of website "{website}"'))
def add_new_end_user_website(driver, website):
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.enter_website(website)
    add_end_user_pages.click_continue()


@when(parsers.parse('I add end user of address: "{address}" and country "{country}"'))
def add_new_end_user_address(driver, address, country, context):
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.enter_address(address)
    context.address_end_user = address
    add_end_user_pages.enter_country(country)
    add_end_user_pages.click_continue()


@when(parsers.parse('I add an end user of type: "{type}", name: "{name}", website: "{website}", address: "{address}" and country "{country}"'))
def add_new_end_user(driver, type, name, website, address, country, context):
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.select_type(type)
    context.type_end_user = type
    add_end_user_pages.click_continue()
    add_end_user_pages.enter_name(name)
    context.name_end_user = name
    add_end_user_pages.click_continue()
    add_end_user_pages.enter_website(website)
    add_end_user_pages.click_continue()
    add_end_user_pages.enter_address(address)
    context.address_end_user = address
    add_end_user_pages.enter_country(country)
    add_end_user_pages.click_continue()


@when('I click on end user')
def i_click_on_end_user(driver):
    app = ApplicationOverviewPage(driver)
    app.click_end_user_link()


@when('I click on application overview')
def i_click_on_application_overview(driver):
    driver.find_element_by_css_selector("a[href*='overview'").click()


@when('I click on ultimate end users')
def i_click_on_application_overview(driver, add_an_incorporated_good_to_application):
    app = ApplicationOverviewPage(driver)
    app.click_ultimate_end_user_link()


@when('I click on back to overview')
def i_go_to_the_overview(driver):
    app = ApplicationOverviewPage(driver)
    app.click_on_back_to_overview_text()

@when('I add a non incorporated good to application')
def add_a_non_incorporated_good(driver, add_a_non_incorporated_good_to_application):
    pass

@when('I remove an ultimate end user so there is one less and return to the overview')
def i_remove_an_ultimate_end_user(driver):
    no_of_ultimate_end_users = len(driver.find_elements_by_css_selector('.govuk-table__row'))
    driver.find_element_by_link_text('Remove').click()
    total = no_of_ultimate_end_users-len(driver.find_elements_by_css_selector('.govuk-table__row'))
    assert total == 1, "total on the ultimate end users summary is incorrect after removing ultimate end user"
    app = ApplicationOverviewPage(driver)
    app.click_on_back_to_overview_text()


@when('I click on ultimate end users add button')
def i_click_on_ultimate_end_user(driver):
    driver.find_element_by_css_selector(".govuk-button").click()


@then('there is only one ultimate end user')
def one_ultimate_end_user(driver):
    elements = driver.find_elements_by_css_selector(".lite-section")
    no = utils.get_element_index_by_partial_text(elements, "Ultimate End Users")
    assert len(elements[no].find_elements_by_css_selector(".govuk-table__row")) == 2, "total on the application overview is incorrect after removing ultimate end user"


@then('I see end user on overview')
def end_user_on_overview(driver, context):
    app = ApplicationOverviewPage(driver)
    assert "Type" in app.get_text_of_end_user_table()
    assert "Name" in app.get_text_of_end_user_table()
    assert "Address" in app.get_text_of_end_user_table()
    assert context.type_end_user in app.get_text_of_end_user_table()
    assert context.name_end_user in app.get_text_of_end_user_table()
    assert context.address_end_user in app.get_text_of_end_user_table()
