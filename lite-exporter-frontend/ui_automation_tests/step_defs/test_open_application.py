from pytest_bdd import scenarios, when, then, parsers

import helpers.helpers as utils
from pages.application_countries_list import ApplicationCountriesList
from pages.application_goods_list import ApplicationGoodsList
from pages.application_goods_type_list import ApplicationGoodsTypeList
from pages.application_overview_page import ApplicationOverviewPage
from pages.goods_countries_page import GoodsCountriesPage
from pages.shared import Shared


scenarios('../features/submit_open_application.feature', strict_gherkin=False)


@then('I see no sites good types or countries attached error message')
def i_see_open_licence_error(driver):
    shared = Shared(driver)
    assert "Cannot create an application with no good descriptions attached" in shared.get_text_of_error_messages()
    assert "Cannot create an application with no sites or external sites attached" in shared.get_text_of_error_messages()
    assert "Cannot create an application without countries being set" in shared.get_text_of_error_messages()


@then('I see good types error messages')
def goods_type_errors(driver):
    shared = Shared(driver)
    assert "This field may not be blank." in shared.get_text_of_error_messages()
    assert "This field is required." in shared.get_text_of_error_messages()


@when('I click overview')
def click_overview(driver):
    application_goods_list = ApplicationGoodsList(driver)
    application_goods_list.click_on_overview()


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
    assert 'Description' in good_type_table_overview
    assert 'Control List Classification' in good_type_table_overview
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
    assert driver.find_element_by_tag_name("h1").text == "Where are your goods going?", \
        "Failed to go to countries list page"


@when(parsers.parse('I select "{country}" from the country list'))
def i_select_country_from_the_country_list(driver, country):
    application_countries_list = ApplicationCountriesList(driver)
    application_countries_list.select_country(country)

    assert utils.find_element_by_href(driver, '#' + country).is_displayed()


@when(parsers.parse('I search for country "{country}"'))
def search_for_country(driver, country):
    ApplicationCountriesList(driver).search_for_country(country)


@then(parsers.parse('only "{country}" is displayed in country list'))
def search_country_result(driver, country):
    assert country == ApplicationCountriesList(driver).get_text_of_countries_list(), \
        "Country not searched correctly"


@when('I click on assign countries to goods')
def go_to_good_countries(driver):
    page = ApplicationOverviewPage(driver)
    page.click_goods_countries_link()


@when(parsers.parse('I "{assign_or_unassign}" all countries to all goods'))
def assign_all(driver, assign_or_unassign):
    countries_page = GoodsCountriesPage(driver)
    if assign_or_unassign == 'assign':
        countries_page.select_all()
    else:
        countries_page.deselect_all()
    Shared(driver).click_continue()


@then(parsers.parse('I see all countries are "{assigned_or_unassigned}" to all goods'))
def see_all_or_no_selected(driver, assigned_or_unassigned):
    countries_page = GoodsCountriesPage(driver)
    if assigned_or_unassigned == 'assigned':
        assert countries_page.all_selected()
    else:
        assert countries_page.all_deselected()

