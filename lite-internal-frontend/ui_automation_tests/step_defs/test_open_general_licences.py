from faker import Faker
from pytest_bdd import scenarios, when, then, given

from pages.application_page import ApplicationPage
from pages.case_list_page import CaseListPage
from pages.open_general_licences_pages import (
    OpenGeneralLicencesListPage,
    OpenGeneralLicencesCreateEditPage,
    OpenGeneralLicencesDetailPage,
    OpenGeneralLicencesDeactivatePage,
    OpenGeneralLicencesCasePage,
)
from shared import functions

from ui_automation_tests.pages.case_page import CasePage, CaseTabs
from ui_automation_tests.pages.shared import Shared

scenarios("../features/open_general_licences.feature", strict_gherkin=False)


fake = Faker()


@when("I go to open general licences")
def go_to_open_general_licences(driver, internal_url):
    driver.get(internal_url.rstrip("/") + "/open-general-licences/")


@when("I click the new open general licence button")
def click_the_open_general_licence_button(driver):
    OpenGeneralLicencesListPage(driver).click_new_open_general_licence_button()


@when("I select Open General Export Licence")
def select_open_general_export_licence(driver):
    OpenGeneralLicencesCreateEditPage(driver).select_open_general_export_licence_radiobutton()
    functions.click_submit(driver)


@when("I fill in details about the licence")
def fill_in_details(driver, context):
    context.ogl_name = fake.bs()
    context.ogl_description = fake.bs()
    context.ogl_link = (
        "https://www.gov.uk/government/publications/open-general-export-licence-military-"
        "goods-government-or-nato-end-use--6"
    )

    create_page = OpenGeneralLicencesCreateEditPage(driver)
    create_page.enter_name(context.ogl_name)
    create_page.enter_description(context.ogl_description)
    create_page.enter_link(context.ogl_link)
    create_page.select_registration_required_yes()
    functions.click_submit(driver)


@when("I select the tree Controlled Radioactive Sources")
def select_control_list_entry(driver):
    OpenGeneralLicencesCreateEditPage(driver).click_controlled_radioactive_tree()
    functions.click_submit(driver)


@when("I select the country United Kingdom")
def select_united_kingdom(driver):
    OpenGeneralLicencesCreateEditPage(driver).click_united_kingdom_checkbox()
    functions.click_submit(driver)


@then("I see the summary list")
def see_the_summary_list(driver, context):
    summary_list_text = OpenGeneralLicencesCreateEditPage(driver).get_text_of_summary_list()
    assert context.ogl_name in summary_list_text
    assert context.ogl_description in summary_list_text
    assert context.ogl_link in summary_list_text
    assert "Yes" in summary_list_text
    assert "Controlled Radioactive Sources" in summary_list_text
    assert "United Kingdom" in summary_list_text


@when("I click submit")
def click_submit(driver):
    functions.click_submit(driver, button_value="finish")


@when("I open the open general licence")
def open_the_open_general_licence(driver, context):
    open_general_licences_list_page = OpenGeneralLicencesListPage(driver)
    open_general_licences_list_page.filter_by_name(context.ogl_name)
    open_general_licences_list_page.click_view_first_ogl_link()


@when("I click change name")
def click_change_name(driver):
    OpenGeneralLicencesDetailPage(driver).click_change_name_link()


@when("I change the OGL name")
def change_the_ogl_name(driver, context):
    context.ogl_name = fake.bs()
    OpenGeneralLicencesCreateEditPage(driver).enter_name(context.ogl_name)
    functions.click_submit(driver)


@when("I deactivate the open general licence")
def deactivate_the_open_general_licence(driver, context):
    OpenGeneralLicencesDetailPage(driver).click_deactivate_link()
    OpenGeneralLicencesDeactivatePage(driver).select_yes()
    functions.click_submit(driver)
    context.ogl_status = "Deactivated"


@then("I see the new open general export licence")
@then("I see the updated open general export licence")
def see_the_newly_generated_open_general_export_licence(driver, context):
    summary_list_text = OpenGeneralLicencesDetailPage(driver).get_text_of_summary_list()
    assert context.ogl_name in summary_list_text
    assert context.ogl_description in summary_list_text
    assert context.ogl_link in summary_list_text
    assert "Yes" in summary_list_text
    assert "Controlled Radioactive Sources" in summary_list_text
    assert "United Kingdom" in summary_list_text
    assert getattr(context, "ogl_status", "Active") in summary_list_text


@given("an ogel licence has been added")  # noqa
def ogel_licence_created(apply_for_ogel):  # noqa
    pass


@given("an ogel application has been added")  # noqa
def ogel_application_created(apply_for_ogel_application):  # noqa
    pass


@when("I filter by OGEL type")
def filter_by_ogel(driver):
    functions.try_open_filters(driver)
    CaseListPage(driver).select_filter_case_type_from_dropdown("Open General Export Licence")
    functions.click_apply_filters(driver)


@then("I see OGEL case")
def see_ogel(driver, context, api_test_client):
    response = api_test_client.cases.get_case_info(context.ogel_case_id)
    assert response["reference_code"] in driver.find_element_by_id(ApplicationPage.HEADING_ID).text
    site_info = OpenGeneralLicencesCasePage(driver).get_text_of_site()
    assert response["data"]["site"]["name"] in site_info
    assert response["data"]["site"]["address"]["address_line_1"] in site_info


@when("I go to ogel site registration case automatically created")  # noqa
def click_on_created_ogel_app(driver, context, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/cases/" + context.ogel_case_id)


@then("I see the reissue button")
def see_reissue_button(driver):
    assert OpenGeneralLicencesCasePage(driver).reissue_button_is_present()


@when("I reissue the ogel")
def click_reissue_button(driver, context):
    ogl_page = OpenGeneralLicencesCasePage(driver)
    ogl_page.click_reissue_button()
    ogl_page.accept_reissue_confirmation()
    functions.click_submit(driver)


@then("the ogel is reissued")
def case_is_finalised(driver):
    CasePage(driver).change_tab(CaseTabs.ACTIVITY)
    assert "reissued" in Shared(driver).get_audit_trail_text()
