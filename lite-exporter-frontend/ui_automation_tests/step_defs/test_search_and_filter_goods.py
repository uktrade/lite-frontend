from urllib.parse import urlencode

from pytest_bdd import when, then, parsers, scenarios
from ui_automation_tests.pages.standard_application.goods import StandardApplicationGoodsPage
from ui_automation_tests.shared.tools.utils import get_lite_client
from ui_automation_tests.shared.api_client.libraries.request_data import build_good

scenarios("../features/search_and_filter_goods.feature", strict_gherkin=False)


@when(parsers.parse('I filter by part number "{part_number}" and click filter'))
def filter_by_part_no(driver, context, part_number):
    goods = StandardApplicationGoodsPage(driver)
    goods.type_into_filter_part_number_search_box_and_filter(part_number)


@when(parsers.parse('I filter by description "{description}" and click filter'))
def filter_by_description(driver, context, description):
    goods = StandardApplicationGoodsPage(driver)
    goods.type_into_filter_description_search_box_and_filter(description)


@when(parsers.parse('I filter by control list entry "{control_list}" and click filter'))
def filter_by_description(driver, context, control_list):
    goods = StandardApplicationGoodsPage(driver)
    goods.type_into_filter_control_rating_search_box_and_filter(control_list)


@when(
    parsers.parse(
        'I create a good of description "{description}", control code "{control_code}" and part number "{part_number}" if it does not exist'
    )
)
def add_a_good(context, description, control_code, part_number, api_client_config):
    lite_client = get_lite_client(context, api_client_config=api_client_config)
    params = {"description": description, "control_rating": control_code, "part_number": part_number}
    goods = lite_client.goods.get_goods(urlencode(params))
    if not len(goods):
        good = build_good(description=description, control_code=control_code, part_number=part_number)
        lite_client.goods.add_good(good)
    context.total_goods = len(lite_client.goods.get_goods())  # gets count of paginated page


@then(parsers.parse('All goods have description "{description}"'))
def good_description_is_found(driver, description):
    goods_list = StandardApplicationGoodsPage(driver).get_good_descriptions()
    assert len(goods_list) > 0
    for good in goods_list:
        assert good.text == description


@then(parsers.parse('All goods have control code "{control_code}"'))
def good_control_code_is_found(driver, control_code):
    goods_list = StandardApplicationGoodsPage(driver).get_good_control_codes()
    assert len(goods_list) > 0
    for good in goods_list:
        assert good.text == control_code


@then(parsers.parse('All goods have part number "{part_number}"'))
def good_part_number_is_found(driver, part_number):
    goods_list = StandardApplicationGoodsPage(driver).get_good_part_numbers()
    assert len(goods_list) > 0
    for good in goods_list:
        assert good.text == part_number


@then(parsers.parse('"{total}" goods are found'))
def total_goods_found(driver, total):
    total_goods = len(StandardApplicationGoodsPage(driver).get_good_descriptions())
    assert total_goods == int(total), "Incorrect number of goods matching search criteria were found"


@when("I click the add from organisations goods button")  # noqa
def click_add_from_organisation_button(driver):  # noqa
    driver.find_element_by_css_selector('a[href*="add-preexisting"]').click()
