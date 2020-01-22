import os

from pytest_bdd import scenarios, when, then, parsers

from conftest import get_file_upload_path
from pages.add_goods_page import AddGoodPage
from pages.attach_document_page import AttachDocumentPage
from pages.goods_list import GoodsListPage
from pages.goods_page import GoodsPage
from pages.shared import Shared
from pages.standard_application.goods import StandardApplicationGoodsPage
from pages.standard_application.good_details import StandardApplicationGoodDetails
from pages.standard_application.task_list import StandardApplicationTaskListPage
from shared import functions

scenarios("../features/goods.feature", strict_gherkin=False)


@then("I see good in goods list")
def assert_good_is_in_list(driver, context, exporter_url):
    driver.get(exporter_url.rstrip("/") + "/goods/")
    goods_row = Shared(driver).get_text_of_gov_table()

    assert context.good_description in goods_row
    assert context.part in goods_row
    assert context.control_code in goods_row


@then("I see the clc query in goods list")
def assert_clc_is_in_list(driver, context, exporter_url):
    goods_row = Shared(driver).get_text_of_gov_table()

    assert context.good_description in goods_row
    assert context.part in goods_row
    assert context.control_code in goods_row
    assert "Control List Classification Query" in goods_row


@when(
    parsers.parse(
        'I edit a good to description "{description}" controlled "{controlled}" '
        'control code "{control_code}" and part number "{part}"'
    )
)
def edit_good(driver, description, controlled, control_code, part, context):
    add_goods_page = AddGoodPage(driver)
    goods_list = GoodsListPage(driver)
    goods_list.select_a_draft_good()
    goods_page = GoodsPage(driver)
    goods_page.click_on_goods_edit_link()
    context.edited_description = context.good_description + " " + description
    add_goods_page.enter_description_of_goods(context.edited_description)
    functions.click_submit(driver)


@when("I delete my good")
def delete_my_good_in_list(driver, context):
    goods_page = GoodsPage(driver)
    goods_page.click_on_goods_edit_link()
    goods_page.click_on_delete_link()
    goods_page.confirm_delete()


@then("my good is no longer in the goods list")
def good_is_no_longer_in_list(driver, context):
    driver.set_timeout_to(0)
    assert len(driver.find_elements_by_id("delete-" + context.good_id_from_url)) == 0
    driver.set_timeout_to(10)


@then("I see my edited good details in the good page")
def click_on_draft_good(driver):
    text = driver.find_element_by_css_selector(".govuk-summary-list").text
    assert "edited" in text
    assert "Yes" in text
    assert "321" in text


@when("I click to manage goods on a standard application")
def i_click_to_manage_goods_on_a_standard_application(driver):
    StandardApplicationTaskListPage(driver).click_goods_link()


@then("I see there are no goods on the application")
def i_see_there_are_no_goods_on_the_application(driver):
    driver.set_timeout_to(0)
    assert StandardApplicationGoodsPage(driver).get_goods_count() == 0
    driver.set_timeout_to(10)


@when("I click Add a new good")
def i_click_add_a_new_good(driver):
    StandardApplicationGoodsPage(driver).click_add_new_good_button()


@when(parsers.parse('I attach a document to the good with description "{description}"'))  # noqa
def i_attach_a_document_to_the_good(driver, description):
    file_to_be_deleted_name = "file_for_doc_upload_test_2.txt"

    # Path gymnastics to get the absolute path for $PWD/../resources/(file_to_upload_x) that works everywhere
    file_to_upload_abs_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, "resources", file_to_be_deleted_name)
    )
    if "ui_automation_tests" not in file_to_upload_abs_path:
        file_to_upload_abs_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, "ui_automation_tests/resources", file_to_be_deleted_name)
        )

    attach_document_page = AttachDocumentPage(driver)
    attach_document_page.choose_file(file_to_upload_abs_path)
    attach_document_page.enter_description(description)
    functions.click_submit(driver)


@then("A new good has been added to the application")
def a_new_good_has_been_added_to_the_application(driver):
    assert StandardApplicationGoodsPage(driver).get_goods_count() == 1


@when(
    parsers.parse(
        'I add a new good with description "{description}" controlled "{controlled}" control code "{control_code}" and part number "{part_number}"'
    )
)  # noqa
def create_a_new_good_in_application(driver, description, controlled, control_code, part_number):
    add_goods_page = AddGoodPage(driver)
    add_goods_page.enter_description_of_goods(description)
    add_goods_page.select_is_your_good_controlled(controlled)
    add_goods_page.enter_control_code(control_code)
    functions.click_submit(driver)


@when(
    parsers.parse(
        'I enter details for the new good on an application with value "{value}", quantity "{quantity}" and unit of measurement "{unit}" and I click Continue'
    )
)  # noqa
def i_enter_detail_for_the_good_on_the_application(driver, value, quantity, unit):
    StandardApplicationGoodDetails(driver).enter_value(value)
    StandardApplicationGoodDetails(driver).enter_quantity(quantity)
    StandardApplicationGoodDetails(driver).select_unit(unit)
    StandardApplicationGoodDetails(driver).check_is_good_incorporated_false()

    functions.click_submit(driver)


@when("I confirm I can upload a document")
def confirm_can_upload_document(driver):
    # Confirm you have a document that is not sensitive
    AddGoodPage(driver).confirm_can_upload_good_document()
    functions.click_submit(driver)


@when("I select that I cannot attach a document")
def select_cannot_attach_a_document(driver):
    AddGoodPage(driver).confirm_cannot_upload_good_document()


@then("I see ECJU helpline details")
def ecju_helpline(driver):
    assert AddGoodPage(driver).get_ecju_help()


@when("I select a valid missing document reason")
def select_missing_document_reason(driver):
    AddGoodPage(driver).select_valid_missing_document_reason()
    functions.click_submit(driver)


@then("My good is created")
def good_created(driver, context):
    summary = AddGoodPage(driver).get_good_summary_text()
    assert context.good_description in summary
    assert context.part in summary
    assert context.control_code in summary


@when("I click add a good button")  # noqa
def click_add_from_organisation_button(driver):  # noqa
    GoodsListPage(driver).click_add_a_good()


@when(parsers.parse('I upload file "{filename}" with description "{description}"'))  # noqa
def upload_a_file_with_description(driver, filename, description):  # noqa
    attach_document_page = AttachDocumentPage(driver)
    file_path = get_file_upload_path(filename)
    attach_document_page.choose_file(file_path)
    attach_document_page.enter_description(description)
    functions.click_submit(driver)


@when(parsers.parse('I raise a clc query control code "{control_code}" description "{description}"'))  # noqa
def raise_clc_query(driver, control_code, description):  # noqa
    raise_clc_query_page = AddGoodPage(driver)
    raise_clc_query_page.enter_control_code_unsure(control_code)
    raise_clc_query_page.enter_control_unsure_details(description)
    functions.click_submit(driver)


@when("I go to good from goods list")
def go_to_good_goods_list(driver, context):
    driver.find_element_by_link_text(context.good_description).click()


@then("I see good information")
def see_good_info(driver, context):
    body = Shared(driver).get_text_of_body()
    assert context.good_description in body
    assert context.part in body
    assert context.control_code in body
