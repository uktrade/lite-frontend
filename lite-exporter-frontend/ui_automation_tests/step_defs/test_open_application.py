from pytest_bdd import scenarios, when, then, parsers

import helpers.helpers as utils
from pages.application_countries_list import ApplicationCountriesList
from pages.application_goods_list import ApplicationGoodsList
from pages.application_goods_type_list import ApplicationGoodsTypeList
from pages.application_overview_page import ApplicationOverviewPage
from pages.shared import Shared


scenarios('../features/submit_open_application.feature', strict_gherkin=False)


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

    assert utils.find_element_by_href(driver, '#' + country).is_displayed()


@then(parsers.parse('I can see "{country_count}" countries selected on the overview page'))
def i_can_see_the_country_count_countries_selected_on_the_overview_page(driver, country_count):
    assert ApplicationOverviewPage(driver).get_text_of_countries_selected() == country_count + ' Countries Selected'


@when('I click on number of countries on the overview page')
def click_on_number_of_countries_selected(driver):
    utils.scroll_to_bottom_of_page(driver)
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
