import datetime
from pytest import fixture
from pages.add_end_user_pages import AddEndUserPages
from pages.add_goods_page import AddGoodPage
from pages.add_new_external_location_form_page import AddNewExternalLocationFormPage
from pages.application_goods_list import ApplicationGoodsList
from pages.application_overview_page import ApplicationOverviewPage
from pages.apply_for_a_licence_page import ApplyForALicencePage
from pages.exporter_hub_page import ExporterHubPage
from pages.external_locations_page import ExternalLocationsPage
from pages.preexisting_locations_page import PreexistingLocationsPage
from pages.which_location_form_page import WhichLocationFormPage
import helpers.helpers as utils


@fixture(scope="module")
def add_an_application(driver, request, exporter_url, context):

    apply = ApplyForALicencePage(driver)
    exporter_hub = ExporterHubPage(driver)
    add_goods_page = AddGoodPage(driver)
    which_location_form = WhichLocationFormPage(driver)
    external_locations_page = ExternalLocationsPage(driver)
    add_new_external_location_form_page = AddNewExternalLocationFormPage(driver)
    preexisting_locations_page = PreexistingLocationsPage(driver)
    overview_page = ApplicationOverviewPage(driver)
    add_end_user_pages = AddEndUserPages(driver)

    type = "standard"
    permanent_or_temporary = "permanent"
    yes_or_no = "yes"
    reference = "123456"
    organisation_or_external = "external"
    name = "32 Lime Street"
    address = "London"
    country = "Ukraine"

    exporter_hub.click_my_goods()
    add_goods_page.click_add_a_good()

    description = "Chinook"
    controlled = "Yes"
    control_code = "1234"
    incorporated = "Yes"
    part = "321"

    add_goods_page = AddGoodPage(driver)
    date_time = utils.get_current_date_time_string()
    good_description = "%s %s" % (description, date_time)
    good_part = "%s %s" % (part, date_time)
    context.good_description = good_description
    context.part = good_part
    context.control_code = control_code
    add_goods_page.enter_description_of_goods(good_description)
    add_goods_page.select_is_your_good_controlled(controlled)
    add_goods_page.select_is_your_good_intended_to_be_incorporated_into_an_end_product(incorporated)
    if "empty" not in good_part:
        add_goods_page.enter_part_number(good_part)
    if controlled.lower() == 'unsure':
        add_goods_page.enter_control_code_unsure(control_code)
        add_goods_page.enter_control_unsure_details(description + " unsure")
        exporter_hub.click_save_and_continue()
        add_goods_page.select_control_unsure_confirmation("yes")
    else:
        add_goods_page.enter_control_code(control_code)
    exporter_hub.click_save_and_continue()
    driver.get(exporter_url)
    exporter_hub.click_apply_for_a_licence()
    apply.click_start_now_btn()
    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context.app_time_id = app_time_id
    app_name = "Request for Nimbus 2000" + app_time_id
    apply.enter_name_or_reference_for_application(app_name)
    context.app_id = app_name
    apply.click_save_and_continue()
    context.type = type
    # type needs to be standard or open
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence(type)
    apply.click_continue()
    context.perm_or_temp = permanent_or_temporary
    # type needs to be permanent or temporary
    apply = ApplyForALicencePage(driver)
    apply.click_permanent_or_temporary_button(permanent_or_temporary)
    apply.click_continue()
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence_yes_or_no(yes_or_no)
    context.ref = reference
    apply.type_into_reference_number(reference)
    apply.click_continue()
    overview_page.click_application_locations_link()
    which_location_form.click_on_organisation_or_external_radio_button(organisation_or_external)
    which_location_form.click_continue()
    external_locations_page.click_add_new_address()
    add_new_external_location_form_page.enter_external_location_name(name)
    add_new_external_location_form_page.enter_external_location_address(address)
    add_new_external_location_form_page.enter_external_location_country(country)
    add_new_external_location_form_page.click_continue()
    external_locations_page.click_add_new_address()
    name = "place"
    address = "1 Paris Road"
    country = "Ukraine"
    add_new_external_location_form_page.enter_external_location_name(name)
    add_new_external_location_form_page.enter_external_location_address(address)
    add_new_external_location_form_page.enter_external_location_country(country)
    add_new_external_location_form_page.click_continue()
    external_locations_page.click_preexisting_locations()
    preexisting_locations_page.click_external_locations_checkbox(int("2") - 1)
    preexisting_locations_page.click_continue()
    driver.find_element_by_css_selector("a[href*='overview'").click()
    driver.execute_script("document.getElementById('goods').scrollIntoView(true);")
    overview_page.click_goods_link()
    driver.find_element_by_css_selector('a[href*="add-preexisting"]').click()
    no = 1
    context.goods_name = driver.find_elements_by_css_selector('.lite-card .govuk-heading-s')[int(no) - 1].text
    context.part_number = driver.find_elements_by_css_selector('.lite-card .govuk-label')[int(no) - 1].text
    driver.find_elements_by_css_selector('a.govuk-button')[int(no) - 1].click()
    quantity = "1"
    value = "123"
    unit = "Metre"
    context.quantity = quantity
    context.value = value
    context.unit = unit
    application_goods_list = ApplicationGoodsList(driver)
    application_goods_list.add_values_to_good(str(value), str(quantity), unit)
    driver.find_element_by_css_selector("button[type*='submit']").click()
    application_goods_list.click_on_overview()
    overview_page.click_end_user_link()
    type = "government"
    name = "Mr Smith"
    website = "https://www.smith.com"
    address = "London"
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
    apply.click_submit_application()
    url = driver.current_url.replace('/overview/', '')
    context.app_id = url[-36:]
