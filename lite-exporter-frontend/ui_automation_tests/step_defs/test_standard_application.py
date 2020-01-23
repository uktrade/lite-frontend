from pytest_bdd import scenarios, when, then, parsers, given

from conftest import enter_application_name, enter_export_licence
from pages.add_end_user_pages import AddEndUserPages
from pages.add_new_external_location_form_page import AddNewExternalLocationFormPage
from pages.attach_document_page import AttachDocumentPage
from pages.generic_application.task_list import GenericApplicationTaskListPage
from pages.external_locations_page import ExternalLocationsPage
from pages.preexisting_locations_page import PreexistingLocationsPage
from pages.shared import Shared
from pages.standard_application.good_details import StandardApplicationGoodDetails
from pages.standard_application.goods import StandardApplicationGoodsPage
from pages.standard_application.task_list import StandardApplicationTaskListPage
from pages.generic_application.ultimate_end_users import GenericApplicationUltimateEndUsers
from pages.which_location_form_page import WhichLocationFormPage
from shared import functions
from shared.tools.helpers import scroll_to_element_by_id
from shared.tools.wait import wait_for_download_button, wait_for_element

scenarios(
    "../features/submit_standard_application.feature",
    "../features/edit_standard_application.feature",
    strict_gherkin=False,
)


@when("I click on the add button")
def i_click_on_the_add_button(driver):
    GenericApplicationUltimateEndUsers(driver).click_add_ultimate_recipient_button()


@when("I remove an ultimate end user so there is one less")
def i_remove_an_ultimate_end_user(driver):
    no_of_ultimate_end_users = Shared(driver).get_size_of_table_rows()
    driver.find_element_by_link_text("Remove").click()
    total = no_of_ultimate_end_users - Shared(driver).get_size_of_table_rows()
    assert total == 1, "total on the ultimate end users summary is incorrect after removing ultimate end user"


@then("there is only one ultimate end user")
def one_ultimate_end_user(driver):
    assert (
        len(GenericApplicationUltimateEndUsers(driver).get_ultimate_recipients()) == 1
    ), "total on the application overview is incorrect after removing ultimate end user"
    functions.click_back_link(driver)


@then("I see end user on overview")
def end_user_on_overview(driver, context):
    app = GenericApplicationTaskListPage(driver)
    assert context.type_end_user.capitalize() in app.get_text_of_end_user_table()
    assert context.name_end_user in app.get_text_of_end_user_table()
    assert context.address_end_user in app.get_text_of_end_user_table()


@then(parsers.parse('"{button}" link is present'))
def download_and_delete_is_links_are_present(driver, button):
    shared = Shared(driver)
    latest_ueu_links = [link.text for link in shared.get_links_of_table_row(-1)]
    assert button in latest_ueu_links


@when("I click on attach a document")
def click_attach_a_document(driver):
    GenericApplicationUltimateEndUsers(driver).click_attach_document_link(-1)


@when("I delete the third party document")
def delete_ultimate_end_user_document(driver):
    third_party = GenericApplicationUltimateEndUsers(driver)
    third_party.click_delete_document_link(-1)
    third_party.click_confirm_delete_yes()
    functions.click_submit(driver)


@then("Wait for download link")
def wait_for_download_link(driver):
    assert wait_for_download_button(driver, page=Shared(driver))


@then(parsers.parse('Wait for "{id}" to be present'))
def wait_for_element_to_be_present(driver, id):
    assert wait_for_element(driver, id)


@when("I delete the end user document")
def end_user_document_delete_is_present(driver):
    scroll_to_element_by_id(Shared(driver).driver, "end_user_document_delete")
    GenericApplicationTaskListPage(driver).click_delete_end_user_document()
    GenericApplicationUltimateEndUsers(driver).click_confirm_delete_yes()
    functions.click_submit(driver)


@then("The end user document has been deleted")
def document_has_been_deleted(driver):
    assert GenericApplicationTaskListPage(driver).attach_end_user_document_is_present()


@when(  # noqa
    parsers.parse('I select the location at position "{position_number}" in external locations list and continue')
)
def assert_checkbox_at_position(driver, position_number):  # noqa
    preexisting_locations_page = PreexistingLocationsPage(driver)
    preexisting_locations_page.click_external_locations_checkbox(int(position_number) - 1)
    functions.click_submit(driver)


@then(parsers.parse('I see "{number_of_locations}" locations'))  # noqa
def i_see_a_number_of_locations(driver, number_of_locations):  # noqa
    assert len(driver.find_elements_by_css_selector("tbody tr")) == int(number_of_locations)


@when("I click on add new address")  # noqa
def i_click_on_add_new_address(driver):  # noqa
    external_locations_page = ExternalLocationsPage(driver)
    external_locations_page.click_add_new_address()


@when("I click on preexisting locations")  # noqa
def i_click_add_preexisting_locations(driver):  # noqa
    external_locations_page = ExternalLocationsPage(driver)
    external_locations_page.click_preexisting_locations()


@when("I click on goods")  # noqa
def i_click_on_goods(driver):  # noqa
    StandardApplicationTaskListPage(driver).click_goods_link()


@when("I add a non-incorporated good to the application")  # noqa
def i_add_a_non_incorporated_good_to_the_application(driver, context):  # noqa
    StandardApplicationGoodsPage(driver).click_add_preexisting_good_button()

    # Click the "Add to application" link on the first good
    driver.find_elements_by_css_selector(".govuk-table__row .govuk-link")[0].click()

    # Enter good details
    StandardApplicationGoodDetails(driver).enter_value("1")
    StandardApplicationGoodDetails(driver).enter_quantity("2")
    StandardApplicationGoodDetails(driver).select_unit("Number of articles")
    StandardApplicationGoodDetails(driver).check_is_good_incorporated_false()
    context.is_good_incorporated = "No"

    functions.click_submit(driver)


@when("I add an incorporated good to the application")  # noqa
def i_add_a_non_incorporated_good_to_the_application(driver, context):  # noqa
    StandardApplicationGoodsPage(driver).click_add_preexisting_good_button()

    # Click the "Add to application" link on the first good
    driver.find_elements_by_css_selector(".govuk-table__row .govuk-link")[0].click()

    # Enter good details
    StandardApplicationGoodDetails(driver).enter_value("1")
    StandardApplicationGoodDetails(driver).enter_quantity("2")
    StandardApplicationGoodDetails(driver).select_unit("Number of articles")
    StandardApplicationGoodDetails(driver).check_is_good_incorporated_true()
    context.is_good_incorporated = "Yes"

    functions.click_submit(driver)


@then("the good is added to the application")  # noqa
def the_good_is_added_to_the_application(driver, context):  # noqa
    body_text = Shared(driver).get_text_of_body()

    assert len(StandardApplicationGoodsPage(driver).get_goods()) == 1  # Only one good added
    assert StandardApplicationGoodsPage(driver).get_goods_total_value() == "£1.00"  # Value
    assert "2.0" in body_text  # Quantity
    assert "Number of articles" in body_text  # Unit
    assert context.is_good_incorporated in body_text  # Incorporated

    # Go back to task list
    functions.click_back_link(driver)


@when("I click on ultimate end users")
def i_click_on_application_overview(driver):
    StandardApplicationTaskListPage(driver).click_ultimate_recipients_link()


@when("I click on the application third parties link")
def i_click_on_application_third_parties_link(driver):
    StandardApplicationTaskListPage(driver).click_third_parties_link()


@when("I remove a third party from the application")
def i_remove_a_third_party_from_the_application(driver):
    remove_good_link = GenericApplicationTaskListPage(driver).find_remove_third_party_link()
    driver.execute_script("arguments[0].click();", remove_good_link)
    functions.click_back_link(driver)


@then("the third party has been removed from the application")
def no_third_parties_are_left_on_the_application(driver):
    assert not functions.element_with_css_selector_exists(
        driver, GenericApplicationTaskListPage(driver).REMOVE_THIRD_PARTY_LINK
    )


@when("I remove a good from the application")
def i_remove_a_good_from_the_application(driver):
    GenericApplicationTaskListPage(driver).get_remove_good_link().click()


@then("the good has been removed from the application")
def no_goods_are_left_on_the_application(driver):
    assert not functions.element_with_css_selector_exists(
        driver, GenericApplicationTaskListPage(driver).REMOVE_GOOD_LINK
    )


@when("I remove the end user off the application")
def i_remove_the_end_user_off_the_application(driver):
    remove_end_user_link = GenericApplicationTaskListPage(driver).find_remove_end_user_link()
    driver.execute_script("arguments[0].click();", remove_end_user_link)
    functions.click_back_link(driver)


@then("no end user is set on the application")
def no_end_user_is_set_on_the_application(driver):
    assert not GenericApplicationTaskListPage(driver).does_remove_end_user_exist(driver)


@when("I remove the consignee off the application")
def i_remove_the_consignee_off_the_application(driver):
    remove_consignee_link = GenericApplicationTaskListPage(driver).find_remove_consignee_link()
    driver.execute_script("arguments[0].click();", remove_consignee_link)
    functions.click_back_link(driver)


@then("no consignee is set on the application")
def no_consignee_is_set_on_the_application(driver):
    assert not GenericApplicationTaskListPage(driver).does_remove_consignee_exist(driver)


@when("I remove an additional document")
def i_remove_an_additional_document(driver):
    driver.set_timeout_to(0)
    remove_consignee_link = GenericApplicationTaskListPage(driver).find_remove_additional_document_link()
    driver.set_timeout_to(10)
    driver.execute_script("arguments[0].click();", remove_consignee_link)


@when("I confirm I want to delete the document")
def i_click_confirm(driver):
    GenericApplicationTaskListPage(driver).confirm_delete_additional_document()


@then("the document is removed from the application")
def no_documents_are_set_on_the_application(driver):
    assert not GenericApplicationTaskListPage(driver).does_remove_additional_document_exist(driver)


@when("I change my reference name")
def change_ref_name(driver, context):
    driver.find_element_by_id("link-reference-name").click()
    enter_application_name(driver, context)


@when("I change my reference number")
def change_ref_num(driver, context):
    driver.find_element_by_id("link-told-by-an-official").click()
    enter_export_licence(driver, "yes", "12345678", context)


@then("I see my edited reference name")
def assert_ref_name(context, driver):
    assert context.app_name in driver.find_element_by_css_selector(".lite-task-list").text


@then("I see my edited reference number")
def assert_ref_num(driver):
    assert "12345678" in driver.find_element_by_css_selector(".lite-task-list").text


@given("I seed an end user for the draft")
def seed_end_user(add_end_user_to_application):
    pass


@when("I select that I want to copy an existing party")
def copy_existing_party_yes(driver):
    AddEndUserPages(driver).create_new_or_copy_existing(copy_existing=True)


@then("I can select the existing party in the table")
def party_table(driver, context):
    text = [context.end_user[key] for key in ["name", "address", "website"]]
    text.append(context.end_user["country"]["name"])
    row = Shared(driver).get_table_row(1)

    for string in text:
        assert string in row.text


@when("I click copy party")
def copy_party(driver):
    AddEndUserPages(driver).click_copy_existing_button()


@when("I select a party type and continue")
def select_party_type(driver, context):
    type = "government"
    AddEndUserPages(driver).select_type(type)
    context.type_end_user = type
    functions.click_submit(driver)


@then("I see the party name is already filled in")
def party_name_autofill(driver, context):
    assert AddEndUserPages(driver).get_name() == context.end_user["name"]


@then("I see the party website is already filled in")
def party_website_autofill(driver, context):
    assert AddEndUserPages(driver).get_website() == context.end_user["website"]


@then("I see the party address and country is already filled in")
def party_address_autofill(driver, context):
    assert AddEndUserPages(driver).get_address() == context.end_user["address"]
    assert AddEndUserPages(driver).get_country() == context.end_user["country"]["id"]


@when("I skip uploading a document")
def skip_document_upload(driver, context):
    AttachDocumentPage(driver).click_save_and_return_to_overview_link()
    # Setup for checking on overview page
    context.type_end_user = context.end_user["sub_type"]["value"]
    context.name_end_user = context.end_user["name"]
    context.address_end_user = context.end_user["address"]


@when("I filter for my previously created end user")
def filter_for_party(driver, context):
    parties_page = AddEndUserPages(driver)
    parties_page.open_parties_filter()
    parties_page.filter_name(context.end_user["name"])
    parties_page.filter_address(context.end_user["address"])
    parties_page.filter_country(context.end_user["country"]["name"])
    parties_page.submit_filter()
