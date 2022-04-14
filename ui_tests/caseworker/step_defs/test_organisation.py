from random import randint

from faker import Faker
from pytest import fixture
from pytest_bdd import scenarios, when, then, given, parsers
from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.header_page import HeaderPage
from ui_tests.caseworker.pages.shared import Shared
from ui_tests.caseworker.pages.organisation_page import OrganisationPage
from ui_tests.caseworker.pages.organisations_form_page import OrganisationsFormPage
from ui_tests.caseworker.pages.organisations_page import OrganisationsPage
from tests_common import functions
from tests_common.tools.wait import wait_until_page_is_loaded
from tests_common.api_client.libraries.request_data import build_organisation, build_organisation_with_primary_site
from tests_common.functions import click_submit
from tests_common.tools.helpers import get_current_date_time


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


@when("I navigate to organisations")
def i_go_to_organisations(driver):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_organisations()


@when("I click on the organisation and click Review")
def click_organisation(driver, context):
    OrganisationsPage(driver).click_organisation(context.organisation_name)
    OrganisationPage(driver).click_review_organisation()


@when("I click on the organisation")
def click_organisation(driver, context):
    OrganisationsPage(driver).click_organisation(context.organisation_name)


@when("I edit the organisation")
def click_edit(driver, context):
    OrganisationPage(driver).click_edit_organisation_link()
    OrganisationsFormPage(driver).fill_in_company_info_page_1(context)


@given("an anonymous user applies for an organisation")
def in_review_organisation(context, api_test_client, get_eori_number, get_registration_number):
    data = build_organisation(
        f"Org-{get_current_date_time()}",
        "commercial",
        "Address-" + get_current_date_time(),
        get_eori_number,
        get_registration_number,
    )
    response = api_test_client.organisations.anonymous_user_create_org(data)
    context.organisation_id = response["id"]
    context.organisation_name = response["name"]
    context.organisation_type = response["type"]["value"]
    context.organisation_eori = response["eori_number"]
    context.organisation_sic = response["sic_number"]
    context.organisation_vat = response["vat_number"]
    context.organisation_registration = response["registration_number"]
    context.organisation_address = data["site"]["address"]["address_line_1"]


@given(
    "an anonymous user creates and organisation for review with <eori_number>,<uk_vat_number>,<primary_site>,<phone_number>"
)
def create_organisation_with_primary_site(
    context, api_test_client, eori_number, uk_vat_number, primary_site, phone_number
):
    data = build_organisation_with_primary_site(
        f"Org-{get_current_date_time()}", "commercial", eori_number, uk_vat_number, primary_site, phone_number
    )
    response = api_test_client.organisations.anonymous_user_create_org(data)
    context.organisation_id = response["id"]
    context.organisation_name = response["name"]
    context.organisation_type = response["type"]["value"]
    context.organisation_eori = response["eori_number"]
    context.organisation_sic = response["sic_number"]
    context.organisation_vat = response["vat_number"]
    context.organisation_registration = response["registration_number"]
    context.organisation_primary_site = data["site"]["name"]
    context.organisation_address = data["site"]["address"]["address_line_1"]


@when("I click on In review tab")
def click_in_review_tab(driver):
    OrganisationsPage(driver).go_to_in_review_tab()


@when("I click on Active tab")
def click_active_tab(driver):
    OrganisationsPage(driver).go_to_active_tab()


@then("I should see details of organisation previously created")
def organisation_in_list(driver, context):
    OrganisationsPage(driver).search_for_org_in_filter(context.organisation_name)
    assert driver.find_element(by=By.ID, value=context.organisation_id).is_displayed()


@when("I click review")
def click_review(driver):
    OrganisationPage(driver).click_review_organisation()


@then("I should see a summary and option to approve or reject organisation")
def organisation_summary(driver, context):
    summary = OrganisationPage(driver).get_organisation_summary()
    assert context.organisation_name in summary
    assert context.organisation_type in summary
    assert context.organisation_eori in summary
    assert context.organisation_sic in summary
    assert context.organisation_vat in summary
    assert context.organisation_registration in summary
    assert context.organisation_address in summary

    assert driver.find_element(by=By.ID, value="status-active").is_enabled()
    assert driver.find_element(by=By.ID, value="status-rejected").is_enabled()


@then("I should see a summary along with primary site")
def organisation_primaty_site(driver, context):
    summary = OrganisationPage(driver).get_organisation_summary()
    assert context.organisation_name in summary
    assert context.organisation_type in summary
    assert context.organisation_eori in summary
    assert context.organisation_sic in summary
    assert context.organisation_vat in summary
    assert context.organisation_registration in summary
    assert context.organisation_address in summary
    assert context.organisation_primary_site in summary

    assert driver.find_element_by_id("status-active").is_enabled()
    assert driver.find_element_by_id("status-rejected").is_enabled()


@when("I select approve and Save")
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


@fixture(scope="function")
def get_eori_number():
    return "GB" + "".join(["{}".format(randint(0, 9)) for _ in range(12)])


@fixture(scope="function")
def get_registration_number():
    return "".join([str(randint(0, 9)) for _ in range(8)])
