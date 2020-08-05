from faker import Faker
from pytest_bdd import when, then, scenarios

from ui_automation_tests.pages.goods_list import GoodsListPage
from ui_automation_tests.shared import functions
from ui_automation_tests.shared.api_client.libraries.request_data import build_good

fake = Faker()

scenarios("../features/search_and_filter_goods.feature", strict_gherkin=False)


@when("I create a good")
def add_a_good(context, api_test_client):
    context.description = fake.bs()
    context.control_list_entry = "ML1a"
    context.part_number = fake.ean8()

    good = build_good(
        description=context.description, control_list_entry=context.control_list_entry, part_number=context.part_number
    )
    api_test_client.goods.add_good(good)


@when("I filter by the good's description and click filter")
def filter_by_description(driver, context):
    GoodsListPage(driver).filter_by_description(context.description)


@when("I filter by the good's part number and click filter")
def filter_by_part_number(driver, context):
    GoodsListPage(driver).filter_by_part_number(context.part_number)


@when("I filter by the good's control list entry and click filter")
def filter_by_control_list_entry(driver, context):
    GoodsListPage(driver).filter_by_control_list_entry(context.control_list_entry)


@then("all goods have the description")
def good_description_is_found(driver, context):
    for row in functions.get_table_rows(driver, raise_exception_if_empty=True):
        assert context.description in row.text


@then("all goods have the control list entry")
def good_control_code_is_found(driver, context):
    for row in functions.get_table_rows(driver, raise_exception_if_empty=True):
        assert context.control_list_entry in row.text


@then("all goods have the part number")
def good_part_number_is_found(driver, context):
    for row in functions.get_table_rows(driver, raise_exception_if_empty=True):
        assert context.part_number in row.text


@then("only one good matches the filters")
def total_goods_found(driver):
    assert len(functions.get_table_rows(driver, raise_exception_if_empty=True)) == 1
