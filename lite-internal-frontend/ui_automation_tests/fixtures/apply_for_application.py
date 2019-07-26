from pytest import fixture
import datetime
from pages.add_goods_page import AddGoodPage
from pages.exporter_hub import ExporterHub
from conf.settings import env
import helpers.helpers as utils


@fixture(scope="session")
def apply_for_standard_application(driver, request, context):
    exporter_hub = ExporterHub(driver)
    driver.get(request.config.getoption("--exporter_url"))
    if "login" in driver.current_url:
        exporter_hub.login(env('TEST_EXPORTER_SSO_EMAIL'),
                           env('TEST_EXPORTER_SSO_PASSWORD'))
    exporter_hub = ExporterHub(driver)
    exporter_hub.click_goods_tile()
    exporter_hub.click_add_a_good()
    exporter_hub.enter_description_of_goods("MPG 2.")
    exporter_hub.select_is_your_good_controlled("Yes")
    exporter_hub.enter_control_code("1234")
    exporter_hub.select_is_your_good_intended_to_be_incorporated_into_an_end_product("Yes")
    exporter_hub.enter_part_number("1234")
    exporter_hub.click_save_and_continue()
    driver.get(request.config.getoption("--exporter_url"))
    exporter_hub.click_apply_for_a_licence()
    exporter_hub.click_start_now_btn()
    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context.app_time_id = app_time_id
    app_name = "Test Application " + app_time_id
    exporter_hub.enter_name_or_reference_for_application(app_name)
    context.app_id = app_name
    exporter_hub.click_save_and_continue()
    exporter_hub.click_export_licence("standard")
    exporter_hub.click_continue()
    exporter_hub.click_permanent_or_temporary_button("permanent")
    exporter_hub.click_continue()
    exporter_hub.click_export_licence_yes_or_no("yes")
    exporter_hub.type_into_reference_number("1234")
    exporter_hub.click_continue()
    exporter_hub.click_application_locations_link()
    exporter_hub.click_on_organisation_or_external_radio_button("organisation")
    exporter_hub.click_continue()
    exporter_hub.click_sites_checkbox(int(1) - 1)
    exporter_hub.click_continue()
    driver.execute_script("document.getElementById('goods').scrollIntoView(true);")
    exporter_hub.click_goods_link()
    driver.find_element_by_css_selector('.govuk-button[href*="add-preexisting"]').click()
    driver.find_elements_by_css_selector('a.govuk-button')[int(1) - 1].click()
    exporter_hub.add_values_to_good(str("1"), str("123"), "Metres")
    exporter_hub.click_continue()
    exporter_hub.click_on_overview()
    exporter_hub.click_end_user_link()
    exporter_hub.select_end_user_type("government")
    exporter_hub.click_continue()
    exporter_hub.enter_end_user_name("Mr Smith")
    exporter_hub.click_continue()
    exporter_hub.enter_end_user_website("https://www.smith.com")
    exporter_hub.click_continue()
    exporter_hub.enter_end_user_address("London")
    exporter_hub.enter_end_user_country("Ukraine")
    exporter_hub.click_continue()
    exporter_hub.click_submit_application()
    assert "Application submitted" in exporter_hub.application_submitted_text()
    # /TODO find better way of getting ID./
    url = driver.current_url.replace('/overview/', '')
    context.app_id = url[-36:]
    driver.get(request.config.getoption("--internal_url"))


@fixture(scope="session")
def apply_for_clc_query(driver, request, context):
    exporter_hub = ExporterHub(driver)
    driver.get(request.config.getoption("--exporter_url"))
    if "login" in driver.current_url:
        exporter_hub.login(env('TEST_EXPORTER_SSO_EMAIL'),
                           env('TEST_EXPORTER_SSO_PASSWORD'))
    exporter_hub.click_goods_button()
    add_goods_page = AddGoodPage(driver)
    add_goods_page.click_add_a_good()
    exporter_hub = ExporterHub(driver)
    add_goods_page = AddGoodPage(driver)
    date_time = utils.get_current_date_time_string()
    good_description = "%s %s" % ("MPG 2.9", date_time)
    context.good_description = good_description
    add_goods_page.enter_description_of_goods(good_description)
    add_goods_page.select_is_your_good_controlled()
    add_goods_page.enter_control_unsure_details("%s unsure" % "MPG 2.9")
    add_goods_page.select_is_your_good_intended_to_be_incorporated_into_an_end_product()
    exporter_hub.click_save_and_continue()
    add_goods_page.select_control_unsure_confirmation()
    exporter_hub.click_save_and_continue()
    case_id = add_goods_page.assert_good_is_displayed_and_return_case_id(context.good_description)
    context.case_id = case_id
    driver.get(request.config.getoption("--internal_url"))
