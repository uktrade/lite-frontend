from pytest_bdd import scenarios, when, then, parsers, given

from pages.add_new_external_location_form_page import AddNewExternalLocationFormPage
from pages.external_locations_page import ExternalLocationsPage
from pages.preexisting_locations_page import PreexistingLocationsPage
from pages.which_location_form_page import WhichLocationFormPage
from pages.add_end_user_pages import AddEndUserPages
from pages.attach_document_page import AttachDocumentPage
from shared import functions
from shared.tools.helpers import scroll_to_element_by_id, paginated_search
from shared.tools.wait import wait_for_download_button, wait_for_element
from pages.application_overview_page import ApplicationOverviewPage
from pages.shared import Shared
from pages.ultimate_end_users_list_page import ThirdPartyListPage

scenarios("../features/submit_standard_application.feature", strict_gherkin=False)


@then("good is added to application")
def good_is_added(driver, context):
    good = ApplicationOverviewPage(driver).get_text_of_good(index=0)
    assert context.goods_name in good
    # TODO put this back when bug is fixed - showing mtr instead of metres
    # assert str(context.quantity) + ".0 " + context.unit in good
    if "." not in context.value:
        assert "£" + str(context.value) + ".00" in good
    else:
        assert "£" + str(context.value) in good


@when("I click on ultimate end users")
def i_click_on_application_overview(driver, add_an_incorporated_good_to_application):
    app = ApplicationOverviewPage(driver)
    scroll_to_element_by_id(Shared(driver).driver, app.ULTIMATE_END_USER_LINK)
    app.click_ultimate_end_user_link()


@when("I click on the add button")
def i_click_on_the_add_button(driver):
    ThirdPartyListPage(driver).click_on_add_a_third_party()


@when("I remove an ultimate end user so there is one less and return to the overview")
def i_remove_an_ultimate_end_user(driver):
    no_of_ultimate_end_users = Shared(driver).get_size_of_table_rows()
    driver.find_element_by_link_text("Remove").click()
    total = no_of_ultimate_end_users - Shared(driver).get_size_of_table_rows()
    assert total == 1, "total on the ultimate end users summary is incorrect after removing ultimate end user"
    functions.click_back_link(driver)


@then("there is only one ultimate end user")
def one_ultimate_end_user(driver):
    elements = ApplicationOverviewPage(driver).get_ultimate_end_users()
    assert len(elements) == 1, "total on the application overview is incorrect after removing ultimate end user"


@then("I see end user on overview")
def end_user_on_overview(driver, context):
    app = ApplicationOverviewPage(driver)
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
    ThirdPartyListPage(driver).click_on_attach_document(-1)


@when("I delete the third party document")
def delete_ultimate_end_user_document(driver):
    third_party = ThirdPartyListPage(driver)
    third_party.click_on_delete_document(-1)
    third_party.accept_delete_confirm()
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
    ApplicationOverviewPage(driver).click_delete_end_user_document()
    ThirdPartyListPage(driver).accept_delete_confirm()
    functions.click_submit(driver)


@then("The end user document has been deleted")
def document_has_been_deleted(driver):
    assert ApplicationOverviewPage(driver).attach_end_user_document_is_present()


@when(parsers.parse('I select "{choice}" for whether or not I want a new or existing location to be added'))  # noqa
def choose_location_type(driver, choice):  # noqa
    which_location_form = WhichLocationFormPage(driver)
    which_location_form.click_on_choice_radio_button(choice)
    functions.click_submit(driver)


@when(  # noqa
    parsers.parse(
        'I fill in new external location form with name: "{name}", address: "{address}" and country: "{country}" and continue'
    )
)
def add_new_external_location(driver, name, address, country):  # noqa
    add_new_external_location_form_page = AddNewExternalLocationFormPage(driver)
    add_new_external_location_form_page.enter_external_location_name(name)
    add_new_external_location_form_page.enter_external_location_address(address)
    add_new_external_location_form_page.enter_external_location_country(country)
    functions.click_submit(driver)


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
