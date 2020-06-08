from faker import Faker
from pytest_bdd import scenarios, when, then, given, parsers

from pages.organisation_page import OrganisationPage
from pages.organisations_form_page import OrganisationsFormPage
from pages.organisations_page import OrganisationsPage
from pages.shared import Shared
from shared import functions
from shared.tools.wait import wait_until_page_is_loaded
from ui_automation_tests.shared.api_client.libraries.request_data import build_organisation
from ui_automation_tests.shared.functions import click_submit
from ui_automation_tests.shared.tools.helpers import get_current_date_time

scenarios("../features/organisation.feature", strict_gherkin=False)

fake = Faker()


@then("commercial organisation is registered")
def verify_registered_organisation(driver, context):
    wait_until_page_is_loaded(driver)
    # Assert that the success info bar is visible
    assert functions.element_with_css_selector_exists(driver, Shared(driver).SNACKBAR_SELECTOR)
    OrganisationsPage(driver).search_for_org_in_filter(context.organisation_name)
    row = OrganisationPage(driver).get_organisation_row()
    assert context.organisation_name in row["name"]
    assert context.eori in row["eori-number"]
    assert context.sic in row["sic-number"]
    assert context.vat in row["vat-number"]


@then("organisation is edited")
def verify_edited_organisation(driver, context):
    body = Shared(driver).get_text_of_summary_list()
    assert context.organisation_name in body
    assert context.eori in body
    assert context.sic in body
    assert context.vat in body


@then(parsers.parse('the "{audit_type}" organisation appears in the audit trail'))
def verify_organisation_audit(driver, context, audit_type):
    body = Shared(driver).get_audit_trail_text()
    if audit_type == "updated":
        assert context.old_organisation_name in body
    assert context.organisation_name in body
    assert audit_type in body


@then("individual organisation is registered")
def verify_registered_individual_organisation(driver, context):
    wait_until_page_is_loaded(driver)
    # Assert that the success info bar is visible
    assert functions.element_with_css_selector_exists(driver, Shared(driver).SNACKBAR_SELECTOR)
    OrganisationsPage(driver).search_for_org_in_filter(context.organisation_name)
    row = OrganisationPage(driver).get_organisation_row()
    assert context.organisation_name in row["name"]


@then("HMRC organisation is registered")
def verify_hmrc_registered_organisation(driver, context):
    OrganisationsPage(driver).search_for_org_in_filter(context.organisation_name)
    assert context.organisation_name in Shared(driver).get_text_of_lite_table_body()


@when("I add a new commercial organisation")
def i_choose_to_add_a_new_commercial_organisation(driver, context):
    OrganisationsPage(driver).click_new_organisation_button()
    organisations_form_page = OrganisationsFormPage(driver)
    organisations_form_page.select_type("commercial")
    organisations_form_page.select_location("united_kingdom")
    organisations_form_page.fill_in_company_info_page_1(context)
    organisations_form_page = OrganisationsFormPage(driver)
    organisations_form_page.enter_site_details(context, "united_kingdom")
    context.email = fake.free_email()
    organisations_form_page.enter_email(context.email)


@when("I add a new individual organisation")
def i_choose_to_add_a_new_individual_organisation(driver, context):
    OrganisationsPage(driver).click_new_organisation_button()
    organisations_form_page = OrganisationsFormPage(driver)
    organisations_form_page.select_type("individual")
    organisations_form_page.select_location("abroad")
    organisations_form_page.fill_in_individual_info_page_1(context)
    organisations_form_page.enter_site_details(context, "abroad")


@when("I add a new HMRC organisation")
def i_choose_to_add_a_new_hmrc_organisation(driver, context):
    OrganisationsPage(driver).click_new_hmrc_organisation_button()
    context.organisation_name = fake.company() + " " + fake.company_suffix()
    organisations_form_page = OrganisationsFormPage(driver)
    organisations_form_page.enter_name(context.organisation_name)
    organisations_form_page.enter_site_details(context, "united_kingdom")
    context.email = fake.free_email()
    organisations_form_page.enter_email(context.email)


@then("the previously created organisations flag is assigned")  # noqa
def assert_flag_is_assigned(driver, context):
    assert Shared(driver).is_flag_applied(context.flag_name), "Flag " + context.flag_name + " is not applied"


@when("I go to organisations")
def i_go_to_organisations(driver, internal_url, context):
    driver.get(internal_url.rstrip("/") + "/organisations")


@when("I click the organisation")
def click_organisation(driver, context):
    OrganisationsPage(driver).click_organisation(context.organisation_name)


@when("I edit the organisation")
def click_edit(driver, context):
    OrganisationPage(driver).click_edit_organisation_link()
    OrganisationsFormPage(driver).fill_in_company_info_page_1(context)


@given("an anonymous user applies for an organisation")
def in_review_organisation(context, api_test_client):
    data = build_organisation("Org-" + get_current_date_time(), "commercial", "Address-" + get_current_date_time())
    response = api_test_client.organisations.anonymous_user_create_org(data)
    context.organisation_id = response["id"]
    context.organisation_name = response["name"]
    context.organisation_type = response["type"]["value"]
    context.organisation_eori = response["eori_number"]
    context.organisation_sic = response["sic_number"]
    context.organisation_vat = response["vat_number"]
    context.organisation_registration = response["registration_number"]
    context.organisation_address = data["site"]["address"]["address_line_1"]


@when("I go to the in review tab")
def in_review_tab(driver):
    OrganisationsPage(driver).go_to_in_review_tab()


@when("I go to the active tab")
def in_review_tab(driver):
    OrganisationsPage(driver).go_to_active_tab()


@then("the organisation previously created is in the list")
def organisation_in_list(driver, context):
    OrganisationsPage(driver).search_for_org_in_filter(context.organisation_name)
    assert driver.find_element_by_id(context.organisation_id).is_displayed()


@when("I click review")
def click_review(driver):
    OrganisationPage(driver).click_review_organisation()


@then("I should see a summary of organisation details")
def organisation_summary(driver, context):
    summary = OrganisationPage(driver).get_organisation_summary()
    assert context.organisation_name in summary
    assert context.organisation_type in summary
    assert context.organisation_eori in summary
    assert context.organisation_sic in summary
    assert context.organisation_vat in summary
    assert context.organisation_registration in summary
    assert context.organisation_address in summary


@when("I approve the organisation")
def approve_organisation(driver):
    OrganisationPage(driver).select_approve_organisation()
    click_submit(driver)


@when("I reject the organisation")
def approve_organisation(driver):
    OrganisationPage(driver).select_reject_organisation()
    click_submit(driver)


@then(parsers.parse('the organisation should be set to "{status}"'))
def organisation_status(driver, status):
    assert status == OrganisationPage(driver).get_status(), "Status doesn't match what was expected"


@when("an organisation matching the existing organisation is created")
def create_matching_org(context, api_test_client):
    data = build_organisation(context.organisation_name, "commercial", context.organisation_address)
    response = api_test_client.organisations.anonymous_user_create_org(data)
    context.organisation_id = response["id"]


@when("I go to the organisation")
def organisation(driver, context, internal_url):
    driver.get(internal_url.rstrip("/") + "/organisations/" + context.organisation_id)


@then("I should be warned that this organisation matches an existing one")
def organisation_warning(driver):
    warning = OrganisationPage(driver).get_warning()
    matching_fields = ["Name", "EORI Number", "Registration Number", "Address"]
    for field in matching_fields:
        assert field in warning, "Missing field in organisation review warning"


@then("the previously created organisations flag is assigned to the case")
def step_impl(driver, context):
    pass
    # assert CasePage(driver).is_flag_applied(context.flag_name), "Flag " + context.flag_name + " is not applied"
