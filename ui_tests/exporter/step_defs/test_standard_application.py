from pytest_bdd import scenarios, when, then, parsers, given
from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.end_use_details_form_page import EndUseDetailsFormPage
from ui_tests.exporter.conftest import (
    enter_type_of_application,
    enter_application_name,
    enter_permanent_or_temporary,
    enter_export_licence,
    enter_case_note_text,
    click_post_note,
)
from ui_tests.exporter.pages.add_new_external_location_form_page import AddNewExternalLocationFormPage
from ui_tests.exporter.pages.add_goods_details import AddGoodDetails
from ui_tests.exporter.pages.add_goods_page import AddGoodPage
from ui_tests.exporter.pages.apply_for_a_licence_page import ApplyForALicencePage
from ui_tests.exporter.pages.check_your_answers_page import CheckYourAnswers
from ui_tests.exporter.pages.exporter_hub_page import ExporterHubPage
from ui_tests.exporter.pages.location_type_page import LocationTypeFormPage
from ui_tests.exporter.pages.submitted_applications_page import SubmittedApplicationsPages
from ui_tests.exporter.pages.which_location_form_page import WhichLocationFormPage
from ui_tests.exporter.pages.add_end_user_pages import AddEndUserPages
from ui_tests.exporter.pages.attach_document_page import AttachDocumentPage
from ui_tests.exporter.pages.external_locations_page import ExternalLocationsPage
from ui_tests.exporter.pages.generic_application.ultimate_end_users import GenericApplicationUltimateEndUsers
from ui_tests.exporter.pages.preexisting_locations_page import PreexistingLocationsPage
from ui_tests.exporter.pages.shared import Shared
from ui_tests.exporter.pages.standard_application.good_details import StandardApplicationGoodDetails
from ui_tests.exporter.pages.standard_application.goods import StandardApplicationGoodsPage
from tests_common import functions

from ui_tests.exporter.pages.generic_application.task_list import TaskListPage

from faker import Faker

fake = Faker()

scenarios(
    "../features/goods.feature",
    "../features/submit_standard_application.feature",
    "../features/edit_standard_application.feature",
    "../features/siel_firearm_application.feature",
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


@then(parsers.parse('"{button}" link is present'))
def download_and_delete_is_links_are_present(driver, button):
    shared = Shared(driver)
    latest_ueu_links = [link.text for link in shared.get_links_of_table_row(-1)]
    assert button in latest_ueu_links


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


@when("I add an incorporated good to the application")  # noqa
def i_add_a_non_incorporated_good_to_the_application(driver, context):  # noqa
    StandardApplicationGoodsPage(driver).click_add_preexisting_good_button()

    # Click the "Add to application" link on the first good
    driver.find_elements_by_id("add-to-application")[0].click()

    # Enter good details
    StandardApplicationGoodDetails(driver).enter_value("1")
    StandardApplicationGoodDetails(driver).enter_quantity("2")
    StandardApplicationGoodDetails(driver).select_unit("Number of articles")
    StandardApplicationGoodDetails(driver).check_is_good_incorporated_true()
    context.is_good_incorporated = "Yes"

    functions.click_submit(driver)


@when("I choose to add a new product")  # noqa
def i_choose_to_add_a_new_product(driver, context):  # noqa
    StandardApplicationGoodsPage(driver).click_add_new_good_button()


@when("I choose to add a product from product list")  # noqa
def i_choose_to_add_product_from_product_list(driver, context):  # noqa
    StandardApplicationGoodsPage(driver).click_add_preexisting_good_button()


@when(parsers.parse('I choose to review the product details of product "{index:d}"'))  # noqa
def i_choose_to_review_product_details(driver, index):  # noqa
    # Click the "View" link on the given good index
    detail_link = driver.find_element_by_id("import-product-view-product")
    detail_link.click()


@when("I see option to add product to application on details page")
def i_see_option_to_add_product_to_application(driver):
    add_to_application_btn = driver.find_element_by_id("button-add-good-to-application")


@when(parsers.parse('I append "{text}" to description and submit'))  # noqa
def i_update_description(driver, text):  # noqa
    change_description = driver.find_elements_by_id("link-edit-description")[0]
    change_description.click()

    desc_element = driver.find_element_by_id("description")
    updated_description = f"{desc_element.text} {text}"
    desc_element.clear()
    desc_element.send_keys(updated_description)

    functions.click_submit(driver)


@when("I add product to application")
def i_add_product_to_application(driver, context):
    add_to_application_btn = driver.find_element_by_id("button-add-good-to-application")
    add_to_application_btn.click()

    # Enter good details
    StandardApplicationGoodDetails(driver).enter_value("1")
    StandardApplicationGoodDetails(driver).enter_quantity("2")
    StandardApplicationGoodDetails(driver).select_unit("Number of articles")
    StandardApplicationGoodDetails(driver).check_is_good_incorporated_true()
    context.is_good_incorporated = "Yes"

    functions.click_submit(driver)


@given("I seed an end user for the draft")
def seed_end_user(add_end_user_to_application):
    pass


@when("I select that I want to copy an existing party")
def copy_existing_party_yes(driver):
    AddEndUserPages(driver).create_new_or_copy_existing(copy_existing=True)


@then("I can select the existing party in the table")
def party_table(driver, context):
    text = [context.end_user[key] for key in ["name", "address"]]
    text.append(context.end_user["country"]["name"])
    row = Shared(driver).get_table_row(1)

    for string in text:
        assert string in row.text


@when("I click copy party")
def copy_party(driver):
    AddEndUserPages(driver).click_copy_existing_button()


@then("I see the party name is already filled in")
def party_name_autofill(driver, context):
    assert AddEndUserPages(driver).get_name() == context.end_user["name"]


@then("I see the party website is already filled in")
def party_website_autofill(driver, context):
    assert AddEndUserPages(driver).get_website() == context.end_user["website"]


@then("I see the party address and country is already filled in")
def party_address_autofill(driver, context):
    assert AddEndUserPages(driver).get_address() == context.end_user["address"]
    assert AddEndUserPages(driver).get_country() == context.end_user["country"]["name"]


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


@given("I create a draft")  # noqa
def create_a_draft(add_a_draft):  # noqa
    pass


@when(parsers.parse('I create a standard application of a "{export_type}" export type'))  # noqa
def create_standard_application(driver, export_type, context):  # noqa
    ExporterHubPage(driver).click_apply_for_a_licence()
    ApplyForALicencePage(driver).select_licence_type("export_licence")
    functions.click_submit(driver)
    enter_type_of_application(driver, "siel", context)
    enter_permanent_or_temporary(driver, export_type, context)
    enter_application_name(driver, context)
    enter_export_licence(driver, "yes", "123456", context)


@when("I click apply")
def click_apply(driver):
    ExporterHubPage(driver).click_apply_for_a_licence()


@when("I select export licence")
def select_export_licence(driver):
    ApplyForALicencePage(driver).select_licence_type("export_licence")
    functions.click_submit(driver)


@when("I select SIEL")
def select_siel(driver):
    apply_page = ApplyForALicencePage(driver)
    apply_page.click_export_licence("siel")
    functions.click_submit(driver)


@when(parsers.parse('I enter "{app_name}" as name'))
def enter_application_name(driver, app_name):
    apply_page = ApplyForALicencePage(driver)
    apply_page.enter_name_or_reference_for_application(app_name)
    functions.click_submit(driver)


@when(parsers.parse('I select "{option}" to reusing an existing party'))
@when(parsers.parse('I select "{option}" to permanently exported'))
@when(parsers.parse('I select "{option}" to section 1 of the firearms act'))
@when(parsers.parse('I select "{option}" to registered firearms dealer'))
@when(parsers.parse('I select "{option}" to a replica firearm'))
@when(parsers.parse('I select "{option}" to receiving a letter'))
def select_yes_no_radio(driver, option):
    Shared(driver).click_on_radio_buttons({"yes": 0, "no": 1, "I don't know": 5}[option])
    functions.click_submit(driver)


@when(
    parsers.parse(
        'I enter "{product_name}" as name, "{clc_entry}" for control list, and "{grading}" for security grading'
    )
)
def enter_add_product_details(driver, product_name, clc_entry, grading):
    add_good_page = AddGoodPage(driver)
    add_good_page.enter_good_name(product_name)
    add_good_page.select_is_your_good_controlled(True)
    add_good_page.enter_control_list_entries(clc_entry)
    if grading != "yes":
        grading = "no"
    add_good_page.select_is_your_good_graded(grading)
    functions.click_submit(driver)


@when(
    parsers.parse(
        'I enter "{value}" as value, "{incorporated}" for incorporation, "{deactivated}" for deactivation, and "{proof_marks}" for proof marks'
    )
)
def enter_quantity_and_value(driver, value, incorporated, deactivated, proof_marks):
    good_details_page = StandardApplicationGoodDetails(driver)
    good_details_page.enter_value(value)
    bool_lookup = {"yes": True, "no": False}
    good_details_page.set_good_incorporated(bool_lookup[incorporated])
    good_details_page.set_deactivated_status(bool_lookup[deactivated])
    good_details_page.set_proof_marks(bool_lookup[proof_marks])
    functions.click_submit(driver)


@when(parsers.parse('I enter "{details}" for the intended end use'))
def enter_end_use_details(driver, details):
    end_use_page = EndUseDetailsFormPage(driver)
    end_use_page.answer_intended_end_use_details(details)
    functions.click_submit(driver)


@when(parsers.parse('I select "{option}" to where products begin export journey'))
def set_begin_export_journey(driver, option):
    Shared(driver).click_on_radio_buttons({"Great Britain": 0, "Northern Ireland": 1}[option])
    functions.click_submit(driver)


@when(parsers.parse('I select "{option}" to who products are going'))
def set_who_products_are_going(driver, option):
    Shared(driver).click_on_radio_buttons(
        {
            "directly to the end-user": 0,
            "to an end-user via a consignee": 1,
            "to an end-user via a consignee, with additional third parties": 2,
        }[option]
    )
    functions.click_submit(driver)


@when(parsers.parse('I select no and enter "{reason}" for end user document'))
def skip_end_user_document(driver, reason):
    select_yes_no_radio(driver, "no")
    AddEndUserPages(driver).enter_no_end_user_document_reason(reason)
    functions.click_submit(driver)


@then("I see the application overview")  # noqa
def i_see_the_application_overview(driver, context):  # noqa
    element = TaskListPage(driver).get_text_of_lite_task_list_items()
    assert context.app_name in element

    app_id = driver.current_url.split("/")[-3]
    context.app_id = app_id


@when(parsers.parse('I am on the application overview page entitled "{title}"'))  # noqa
def i_am_on_application_overview_with_title(driver, title):  # noqa
    heading = driver.find_element_by_xpath("//h1").text
    assert heading == title


@then(parsers.parse('I should be taken to the application overview page entitled "{title}"'))  # noqa
def taken_to_application_overview_page(driver, title):
    i_am_on_application_overview_with_title(driver, title)


@when("I delete the application")  # noqa
def i_delete_the_application(driver):  # noqa
    apply = ApplyForALicencePage(driver)
    apply.click_delete_application()
    assert "Applications - LITE" in driver.title, (
        "failed to go to Applications list page after deleting application " "from application overview page"
    )


@when("I add a note to the draft application")  # noqa
def add_a_note_to_draft_application(driver, context):  # noqa
    enter_case_note_text(driver, context)
    click_post_note(driver)
    SubmittedApplicationsPages(driver).assert_case_notes_exists([context.text])

    functions.click_back_link(driver)


@when(parsers.parse('I select "{choice}" for whether or not I want a new or existing location to be added'))  # noqa
def choose_location_type(driver, choice):  # noqa
    which_location_form = WhichLocationFormPage(driver)
    which_location_form.click_on_choice_radio_button(choice)
    functions.click_submit(driver)


@when(parsers.parse('I select a location type of "{location_type}"'))  # noqa
def choose_location_type(driver, location_type):  # noqa
    LocationTypeFormPage(driver).click_on_location_type_radiobutton(location_type)
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
    parsers.parse(
        'I fill in new external location form with name: "{name}", address: "{address}" and no country and continue'
    )
)
def add_new_external_location_without_country(driver, name, address):  # noqa
    add_new_external_location_form_page = AddNewExternalLocationFormPage(driver)
    add_new_external_location_form_page.enter_external_location_name(name)
    add_new_external_location_form_page.enter_external_location_address(address)
    functions.click_submit(driver)


@when("I create a standard individual transhipment application")  # noqa
def create_standard_individual_transhipment_application(driver, context):  # noqa
    ExporterHubPage(driver).click_apply_for_a_licence()
    ApplyForALicencePage(driver).select_licence_type("transhipment")
    functions.click_submit(driver)
    enter_type_of_application(driver, "sitl", context)
    enter_application_name(driver, context)
    enter_export_licence(driver, "yes", "123456", context)


@when("I create a standard individual trade control draft application")  # noqa
def create_standard_individual_trade_control_application(driver, context):  # noqa
    ExporterHubPage(driver).click_apply_for_a_licence()
    apply_for_licence_page = ApplyForALicencePage(driver)
    apply_for_licence_page.select_licence_type("trade_control_licence")
    functions.click_submit(driver)
    enter_type_of_application(driver, "sicl", context)
    enter_application_name(driver, context)
    apply_for_licence_page.select_trade_control_activity()
    apply_for_licence_page.select_trade_control_product_category()


@when("I change my reference number")
def change_ref_num(driver, context):  # noqa
    enter_export_licence(driver, "yes", "12345678", context)


@then("I see my edited reference number")
def assert_ref_num(driver):  # noqa
    assert "12345678" in driver.find_element_by_css_selector(".lite-task-list").text


@when(parsers.parse('I answer "{choice}" for compliance with the terms of export from the EU'))  # noqa
def eu_compliant_limitations_end_use_details(driver, choice):  # noqa
    end_use_details = EndUseDetailsFormPage(driver)
    if choice == "Yes":
        end_use_details.answer_is_compliant_limitations_eu(True)
    else:
        end_use_details.answer_is_compliant_limitations_eu(False, fake.sentence(nb_words=30))
    functions.click_submit(driver)


@when(parsers.parse('I select "{choice}" to products received under transfer licence from the EU'))  # noqa
def eu_military_end_use_details(driver, choice):  # noqa
    end_use_details = EndUseDetailsFormPage(driver)
    if choice == "Yes":
        end_use_details.answer_is_eu_military(True)
    else:
        end_use_details.answer_is_eu_military(False)
    functions.click_submit(driver)


@when(parsers.parse('I select no to product document and enter "{reason}"'))
def select_product_document_available(driver, reason):
    Shared(driver).click_on_radio_buttons(1)
    good_details_page = AddGoodDetails(driver)
    good_details_page.enter_related_field_details("no_document_comments", text=reason)
    functions.click_submit(driver)


@when(parsers.parse('I select "{choice}" to document available question'))
def check_product_document_available(driver, choice):
    good_details_page = AddGoodDetails(driver)
    good_details_page.set_product_document_availability(choice)
    functions.click_submit(driver)


@when(parsers.parse('I select "{choice}" to document is above official sensitive question'))
def check_product_document_available(driver, choice):
    good_details_page = AddGoodDetails(driver)
    good_details_page.set_product_document_sensitive(choice)
    functions.click_submit(driver)


@when(parsers.parse('I select "{choice}" to registered firearms dealer question'))
def check_product_document_available(driver, choice):
    good_details_page = AddGoodDetails(driver)
    good_details_page.set_registered_firearms_dealer(choice)
    functions.click_submit(driver)


@then("my answers are played back to me")
def answers_played_back_to_me():
    pass


@then(parsers.parse('I see "{licence}" as the Licence'))
def check_licence_type_full(driver, licence):
    answers_page = CheckYourAnswers(driver)
    assert licence == answers_page.get_summary_row_value("Licence")


@then(parsers.parse('I see "{licence_type}" as the type'))
def check_licence_type(driver, licence_type):
    answers_page = CheckYourAnswers(driver)
    assert licence_type == answers_page.get_summary_row_value("Type")


@then(parsers.parse('I see "{name}" as reference name'))
def check_application_name(driver, name):
    answers_page = CheckYourAnswers(driver)
    assert name == answers_page.get_summary_row_value("Reference name")


@then(parsers.parse('I see "{informed_status}" as informed to apply'))
def check_informed_status(driver, informed_status):
    answers_page = CheckYourAnswers(driver)
    assert informed_status == answers_page.get_summary_row_value("Informed to apply")


@then(parsers.parse('I see "{origin}" as product journey origin'))
def check_application_name(driver, origin):
    label = "Where will the products begin their export journey?"
    answers_page = CheckYourAnswers(driver)
    assert origin == answers_page.get_row_value(label)


@then(parsers.parse('I see "{value}" as product permanently exported'))
def check_export_status(driver, value):
    label = "Are the products being permanently exported?"
    answers_page = CheckYourAnswers(driver)
    assert value == answers_page.get_row_value(label)


@then(parsers.parse('I see "{waybill_status}" as way bill'))
def check_way_bill(driver, waybill_status):
    label = "Are the products being shipped from the UK on an air waybill or bill of lading?"
    answers_page = CheckYourAnswers(driver)
    assert waybill_status == answers_page.get_row_value(label)


@then(parsers.parse('I see "{transit_status}" as who are the products going to'))
def check_party(driver, transit_status):
    label = "Who are the products going to?"
    answers_page = CheckYourAnswers(driver)
    assert transit_status == answers_page.get_row_value(label)


@then(parsers.parse('I see "{product_name}" as name'))
def check_product_name(driver, product_name):
    answers_page = CheckYourAnswers(driver)
    assert product_name == answers_page.get_product_field_value("Name")


@then(parsers.parse('I see "{part_number}" as part number'))
def check_product_part_number(driver, part_number):
    answers_page = CheckYourAnswers(driver)
    assert part_number == answers_page.get_product_field_value("Part number")


@then(parsers.parse('I see "{controlled}" as controlled'))
def check_product_controlled_status(driver, controlled):
    answers_page = CheckYourAnswers(driver)
    assert controlled == answers_page.get_product_field_value("Controlled")


@then(parsers.parse('I see "{clc_entry}" as control list entry'))
def check_product_clc_entry(driver, clc_entry):
    answers_page = CheckYourAnswers(driver)
    assert clc_entry == answers_page.get_product_field_value("Control list entries")


@then(parsers.parse('I see "{incorporated}" as incorporated'))
def check_product_incorporation(driver, incorporated):
    answers_page = CheckYourAnswers(driver)
    assert incorporated == answers_page.get_product_field_value("Incorporated")


@then(parsers.parse('I see "{quantity}" as quantity'))
def check_product_quantity(driver, quantity):
    answers_page = CheckYourAnswers(driver)
    assert quantity == answers_page.get_product_field_value("Quantity")


@then(parsers.parse('I see "{value}" as value'))
def check_product_value(driver, value):
    answers_page = CheckYourAnswers(driver)
    assert value == answers_page.get_product_field_value("Value")


@then(parsers.parse('I see "{end_use}" as intended end use'))
def check_end_use(driver, end_use):
    answers_page = CheckYourAnswers(driver)
    assert end_use == answers_page.get_end_use_field_value("Intended end use")


@then(parsers.parse('I see "{inform_status}" for informed to apply'))
def check_informed_to_apply(driver, inform_status):
    answers_page = CheckYourAnswers(driver)
    assert inform_status == answers_page.get_end_use_field_value("Informed to apply")


@then(parsers.parse('I see "{inform_wmd}" for informed WMD'))
def check_informed_wmd(driver, inform_wmd):
    answers_page = CheckYourAnswers(driver)
    assert inform_wmd == answers_page.get_end_use_field_value("Informed WMD")


@then(parsers.parse('I see "{suspect_wmd}" for suspect WMD'))
def check_suspect_wmd(driver, suspect_wmd):
    answers_page = CheckYourAnswers(driver)
    assert suspect_wmd == answers_page.get_end_use_field_value("Suspect WMD")


@then(parsers.parse('I see "{eu_transfer}" for EU transfer'))
def check_eu_transfer(driver, eu_transfer):
    answers_page = CheckYourAnswers(driver)
    assert eu_transfer == answers_page.get_end_use_field_value("EU transfer licence")


@then(parsers.parse('I see "{end_user_name}" for end user name'))
def check_end_user_name(driver, end_user_name):
    answers_page = CheckYourAnswers(driver)
    assert end_user_name == answers_page.get_end_user_row_value("Name")


@then(parsers.parse('I see "{end_user_type}" for type'))
def check_end_user_type(driver, end_user_type):
    answers_page = CheckYourAnswers(driver)
    assert end_user_type == answers_page.get_end_user_row_value("Type")


@then(parsers.parse('I see "{end_user_address}" as address'))
def check_end_user_address(driver, end_user_address):
    answers_page = CheckYourAnswers(driver)
    assert end_user_address == answers_page.get_end_user_row_value("Address")


@then(parsers.parse('I see "{end_user_website}" as website'))
def check_end_user_website(driver, end_user_website):
    answers_page = CheckYourAnswers(driver)
    assert end_user_website == answers_page.get_end_user_row_value("Website")


@then(parsers.parse('I see "{end_user_signatory}" as signatory'))
def check_end_user_signatory(driver, end_user_signatory):
    answers_page = CheckYourAnswers(driver)
    assert end_user_signatory == answers_page.get_end_user_row_value("Signatory name")


@then(parsers.parse('I see "{end_user_document_status}" for end user document'))
def check_end_user_undertaking_document(driver, end_user_document_status):
    label = "Do you have an end-user document?"
    answers_page = CheckYourAnswers(driver)
    assert end_user_document_status == answers_page.get_end_user_row_value(label)


@then(parsers.parse('I see "{reason}" for the explanation'))
def check_end_user_document_missing_reason(driver, reason):
    label = "Explain why you do not have an end-user undertaking or stockist undertaking"
    answers_page = CheckYourAnswers(driver)
    assert reason == answers_page.get_end_user_row_value(label)


@then(parsers.parse('I see "{no_info_text}" for "{party_type}"'))
def check_party_section_text(driver, no_info_text, party_type):
    answers_page = CheckYourAnswers(driver)
    assert no_info_text == answers_page.get_party_section_text(party_type)


@then(parsers.parse('I see "{no_info_text}" for Notes'))
def check_notes(driver, no_info_text):
    assert no_info_text == CheckYourAnswers(driver).get_notes_text()


@then("I see a banner reminding me to add serial numbers")
def add_serial_numbers_reminder_banner(driver):
    banner = driver.find_element(by=By.ID, value="govuk-notification-banner-title")
    assert banner.text == "Important"
    banner_heading = driver.find_element(by=By.CLASS_NAME, value="govuk-notification-banner__heading")
    assert "You need to provide serial numbers for your products before you can export them." in banner_heading.text


@then("I don't see a banner reminding me to add serial numbers")
def check_serial_numbers_banner_missing(driver):
    elements = driver.find_elements(by=By.XPATH, value="//*[@id]")
    elements = [item.get_attribute("id") for item in elements]

    assert "govuk-notification-banner-title" not in elements


@when(parsers.parse('I click on "{link_text}"'))
def click_add_serial_numbers_link(driver, link_text):
    serial_numbers_link = driver.find_element(by=By.LINK_TEXT, value=link_text)
    serial_numbers_link.click()


@when(parsers.parse('I input "{serial_number}" as serial numbers for items "{items}" and press submit'))
def enter_serial_numbers(driver, serial_number, items):
    for item in items.split(","):
        index = int(item) - 1
        input_element = driver.find_element(by=By.ID, value=f"id_serial_numbers_{index}")
        input_element.clear()
        input_element.send_keys(serial_number.strip())

    functions.click_submit(driver)


@then(parsers.parse('I see serial numbers for items "{items}" as "{serial_number}"'))
def verify_serial_numbers(driver, serial_number, items):
    for item in items.split(","):
        index = int(item) - 1
        input_element = driver.find_element(by=By.ID, value=f"id_serial_numbers_{index}")
        assert input_element.get_property("value") == serial_number
