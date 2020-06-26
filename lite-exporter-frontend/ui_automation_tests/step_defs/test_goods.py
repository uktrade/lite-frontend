import os

from pytest_bdd import scenarios, when, then, parsers

from ui_automation_tests.shared.tools import helpers
from ui_automation_tests.pages.add_goods_details import AddGoodDetails
from ui_automation_tests.pages.add_goods_grading_page import AddGoodGradingPage
from ui_automation_tests.conftest import get_file_upload_path
from ui_automation_tests.pages.add_goods_page import AddGoodPage
from ui_automation_tests.pages.attach_document_page import AttachDocumentPage
from ui_automation_tests.pages.goods_list import GoodsListPage
from ui_automation_tests.pages.goods_page import GoodsPage
from ui_automation_tests.pages.shared import Shared
from ui_automation_tests.pages.standard_application.goods import StandardApplicationGoodsPage
from ui_automation_tests.pages.standard_application.good_details import StandardApplicationGoodDetails
from ui_automation_tests.shared import functions
import ui_automation_tests.shared.tools.helpers as utils

scenarios("../features/goods.feature", strict_gherkin=False)


@then("I see good in goods list")
def assert_good_is_in_list(driver, context, exporter_url):
    driver.get(exporter_url.rstrip("/") + "/goods/")
    goods_row = Shared(driver).get_text_of_gov_table()

    assert context.good_description in goods_row
    assert context.part in goods_row
    assert context.control_code in goods_row
    assert driver.find_element_by_css_selector("[href*='goods/" + context.good_id_from_url + "']").is_displayed()


@then("I see the good is in a query")
def assert_good_contain_query_details(driver, context, exporter_url):
    goods_list = GoodsPage(driver)
    assert goods_list.get_text_of_query_details()


@when(
    parsers.parse(
        'I edit the good to description "{description}" part number "{part}" controlled "{controlled}" and '
        'control list entry "{control_list_entry}"'
    )
)
def edit_good(driver, description, part, controlled, control_list_entry, context):
    goods_list = GoodsListPage(driver)
    add_goods_page = AddGoodPage(driver)

    goods_list.filter_by_description(context.good_description)
    goods_list.click_view_good(0)

    goods_page = GoodsPage(driver)
    goods_page.click_on_goods_description_edit_link()

    context.edited_description = context.good_description + " " + description
    add_goods_page.enter_description_of_goods(context.edited_description)
    add_goods_page.enter_part_number(part)
    add_goods_page.select_is_your_good_controlled(controlled)
    add_goods_page.enter_control_list_entries(control_list_entry)

    functions.click_submit(driver)


@when(  # noqa
    parsers.parse(
        'I edit the "{category}" good details to military use "{military_use}" component "{component}" information security "{infosec}"'
    )
)
def edit_good_details(driver, category, military_use, component, infosec, context):  # noqa
    goods_page = GoodsPage(driver)
    good_details_page = AddGoodDetails(driver)

    goods_page.click_on_good_edit_military_use_link()
    good_details_page.select_is_product_for_military_use(military_use)
    functions.click_submit(driver)

    if category == "category 1":
        goods_page.click_on_good_edit_is_component_link()
        good_details_page.select_is_product_a_component(component)
        functions.click_submit(driver)

    goods_page.click_on_good_edit_uses_information_security_link()
    good_details_page.does_product_employ_information_security(infosec)
    functions.click_submit(driver)


@when("I delete my good")
def delete_my_good_in_list(driver, context):
    goods_page = GoodsPage(driver)
    goods_page.click_delete_button()

    functions.click_submit(driver)


@then("my good is no longer in the goods list")
def good_is_no_longer_in_list(driver, context):
    assert context.good_description not in Shared(driver).get_text_of_gov_table()


@then("I see my edited good details in the good page")
def click_on_draft_good(driver, context, exporter_url):
    good_id = driver.current_url.split("/goods/")[1].split("/")[0]
    driver.get(exporter_url.rstrip("/") + "/goods/" + good_id)
    text = driver.find_element_by_css_selector(".govuk-summary-list").text
    assert "edited" in text
    assert "Yes" in text
    assert "321" in text
    elements = driver.find_elements_by_css_selector(".govuk-summary-list__row")
    military_use_row_text = helpers.get_element_row_text_from_table(elements, "Military use")
    component_row_text = helpers.get_element_row_text_from_table(elements, "Component")
    infosec_row_text = helpers.get_element_row_text_from_table(elements, "Information security features")
    software_technology_details_row_text = helpers.get_element_row_text_from_table(elements, "Purpose")
    assert "Yes, specially designed for military use" in military_use_row_text
    if component_row_text:
        assert "Yes, it's designed specially for hardware" in component_row_text
    assert "No" in infosec_row_text
    if software_technology_details_row_text:
        assert "edited software purpose" in software_technology_details_row_text


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
        'I add a new good with description "{description}" part number "{part_number}" controlled "{controlled}" control code "{control_code}" and graded "{graded}"'
    )
)  # noqa
def create_a_new_good_in_application(driver, description, part_number, controlled, control_code, graded):
    add_goods_page = AddGoodPage(driver)
    add_goods_page.enter_description_of_goods(description)
    add_goods_page.select_is_your_good_controlled(controlled)
    add_goods_page.enter_control_list_entries(control_code)
    add_goods_page.select_is_your_good_graded(graded)
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


@when(
    parsers.parse(
        'I raise a clc query control code "{control_code}" clc description "{clc_reason}" and pv grading reason "{pv_grading_reason}"'
    )
)  # noqa
def raise_clc_query(driver, control_code, clc_reason, pv_grading_reason):  # noqa
    raise_clc_query_page = AddGoodPage(driver)
    raise_clc_query_page.enter_control_code_unsure(control_code)
    raise_clc_query_page.enter_control_unsure_details(clc_reason)
    raise_clc_query_page.enter_grading_unsure_details(pv_grading_reason)
    functions.click_submit(driver)


@then("I see good information")
def see_good_info(driver, context):
    body = Shared(driver).get_text_of_body()
    assert context.good_description in body
    assert context.part in body
    assert context.control_code in body


@when(  # noqa
    parsers.parse(
        'I add a good with description "{description}" part number "{part}" controlled "{controlled}" control code "{control_code}" and graded "{graded}"'
    )
)
def add_new_good(driver, description, part, controlled, control_code, graded, context):  # noqa
    good_part_needed = True
    add_goods_page = AddGoodPage(driver)
    date_time = utils.get_current_date_time_string()
    good_description = "%s %s" % (description, date_time)
    good_part = "%s %s" % (part, date_time)
    context.good_description = good_description
    context.part = good_part
    context.control_code = control_code
    add_goods_page.enter_description_of_goods(good_description)
    add_goods_page.select_is_your_good_controlled(controlled)
    if "not needed" in good_part:
        good_part_needed = False
    elif "empty" not in good_part:
        add_goods_page.enter_part_number(good_part)
    if controlled.lower() == "yes":
        add_goods_page.enter_control_list_entries(control_code)
    add_goods_page.select_is_your_good_graded(graded)
    functions.click_submit(driver)


@when(  # noqa
    parsers.parse(
        'I add the goods grading with prefix "{prefix}" grading "{grading}" suffix "{suffix}" '
        'issuing authority "{issuing_authority}" reference "{reference}" Date of issue "{date_of_issue}"'
    )
)
def add_good_grading(driver, prefix, grading, suffix, issuing_authority, reference, date_of_issue, context):  # noqa
    goods_grading_page = AddGoodGradingPage(driver)
    goods_grading_page.enter_prefix_of_goods_grading(prefix)
    goods_grading_page.enter_good_grading(grading)
    goods_grading_page.enter_suffix_of_goods_grading(suffix)
    goods_grading_page.enter_issuing_authority(issuing_authority)
    goods_grading_page.enter_reference(reference)
    date = date_of_issue.split("-")
    goods_grading_page.enter_date_of_issue(date[0], date[1], date[2])
    functions.click_submit(driver)


@when(parsers.parse('I select product category "{category}" for a good'))  # noqa
def select_product_category(driver, category, context):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.select_product_category(category)
    functions.click_submit(driver)


@when(  # noqa
    parsers.parse(
        'I specify the "{category}" good details military use "{military_use}" component "{component}" and information security "{infosec}"'
    )
)
def add_good_details(driver, category, military_use, component, infosec, context):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.select_is_product_for_military_use(military_use)
    functions.click_submit(driver)
    if category == "category 1":
        good_details_page.select_is_product_a_component(component)
        functions.click_submit(driver)
    good_details_page.does_product_employ_information_security(infosec)
    functions.click_submit(driver)


@when("I specify software and technology purpose details for a good that is in those categories")  # noqa
def add_good_software_technology_purpose_details(driver):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.enter_software_technology_purpose_details()
    functions.click_submit(driver)


@when(parsers.parse('I edit the software and technology purpose details for a good to "{edited_details}"'))  # noqa
def add_good_software_technology_purpose_details(driver, edited_details, context):  # noqa
    goods_page = GoodsPage(driver)
    good_details_page = AddGoodDetails(driver)

    goods_page.click_on_good_edit_software_technology_details()
    good_details_page.enter_software_technology_purpose_details(text=edited_details)
    functions.click_submit(driver)


@when("I get the goods ID")
def get_id(driver, context):
    context.good_id_from_url = driver.current_url.split("/goods/")[1].split("/")[0]
