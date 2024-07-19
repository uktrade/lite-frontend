import json
import re

from faker import Faker
from pytest_bdd import given, when, then, parsers, scenarios
from selenium.webdriver.common.by import By

from tests_common import functions


scenarios("../../features/amendments/siel_amendments.feature", strict_gherkin=False)

faker = Faker()


@given(parsers.parse('I create a standard draft application with "{reference}" as reference'))
def create_standard_draft_with_reference(api_test_client, context, reference):
    draft = {
        "name": reference,
        "application_type": "siel",
        "export_type": "permanent",
        "have_you_been_informed": "yes",
        "reference_number_on_information_form": "1234",
    }
    draft_id = api_test_client.applications.create_draft(draft)

    end_use_details = {
        "intended_end_use": "Research and development",
        "is_military_end_use_controls": False,
        "is_informed_wmd": False,
        "is_suspected_wmd": False,
        "is_eu_military": False,
    }
    route_of_goods = {
        "goods_starting_point": "GB",
        "is_shipped_waybill_or_lading": True,
        "goods_recipients": "via_consignee",
    }
    additional_information = {"is_mod_security_approved": False}

    api_test_client.applications.add_end_use_details(draft_id=draft_id, details=end_use_details)
    api_test_client.applications.add_route_of_goods(draft_id=draft_id, route_of_goods=route_of_goods)
    api_test_client.applications.add_additional_information(draft_id=draft_id, json=additional_information)

    context.application_id = draft_id
    context.exporter_reference = reference


@when(parsers.parse("I go to task list of the draft application"))
def application_task_list(driver, context):
    driver.find_element(by=By.ID, value="link-applications").click()
    driver.find_element(by=By.ID, value="applications-tab-drafts").click()

    # There could be multiple drafts with the same reference so use the
    # application_id to find the correct element
    assert context.application_id
    task_list_url = f"/applications/{context.application_id}/task-list/"
    driver.find_element(by=By.XPATH, value=f'//a[@href="{task_list_url}"]').click()


@when(parsers.parse('I add Consignee with details "{name}", "{address}", "{country}"'))
def add_consignee_to_application(api_test_client, context, name, address, country):
    party_type = "consignee"
    consignee = {
        "type": party_type,
        "name": name,
        "address": address,
        "country": country,
        "sub_type": "government",
        "website": faker.uri(),
    }
    api_test_client.applications.parties.add_party(context.application_id, party_type, consignee)


@when(parsers.parse('I add End-user with details "{name}", "{address}", "{country}"'))
def add_end_user_to_application(api_test_client, context, name, address, country):
    party_type = "end_user"
    end_user = {
        "type": party_type,
        "name": name,
        "address": address,
        "country": country,
        "sub_type": "government",
        "website": faker.uri(),
        "signatory_name_euu": name,
        "end_user_document_available": False,
        "end_user_document_missing_reason": "document not available",
    }
    api_test_client.applications.parties.add_party(context.application_id, party_type, end_user)


@when(parsers.parse("I add a set of products to the application as json:\n{products_data}"))
def add_products_to_application(api_test_client, context, products_data):
    good_on_application_ids = []
    products = json.loads(products_data.replace("\n", ""))
    for product in products:
        data = {
            **product,
            "is_good_controlled": True,
            "is_pv_graded": "no",
            "item_category": "group2_firearms",
        }
        good = api_test_client.applications.goods.post_good(data)

        data = {
            "good_id": good["id"],
            "quantity": 64,
            "unit": "NAR",
            "value": 256.32,
            "is_good_incorporated": False,
        }
        if "firearm_details" in product:
            details = {
                **product["firearm_details"],
                "number_of_items": 2,
                "year_of_manufacture": 2000,
                "serial_numbers_available": "AVAILABLE",
            }
            data["firearm_details"] = details
        good_on_application = api_test_client.applications.goods.add_good_to_draft(context.application_id, data)
        good_on_application_ids.append(good_on_application["id"])

    context.good_on_application_ids = good_on_application_ids


@when("I continue to submit application")
def continue_submitting_application(driver):
    functions.click_submit(driver)


@then("I record application reference code")
def record_application_reference_code(driver, context):
    message = driver.find_element(by=By.ID, value="application-processing-message-value").text
    matches = re.findall(r"GBSIEL/[0-9]+/[0-9]+/[P|T]", message)
    assert len(matches) == 1
    context.reference_code = matches[0]


@when("I go to my list of applications")
def goto_list_of_applications(driver):
    driver.find_element(by=By.CLASS_NAME, value="govuk-header__link--service-name").click()
    driver.find_element(by=By.ID, value="link-applications").click()

    # Sort by latest first in case our target application is in next page
    url = f"{driver.current_url}?sort_by=-submitted_at"
    driver.get(url)


@when("I click on the application previously submitted")
def click_previously_selected_application(driver, context):
    assert context.reference_code
    application_row = [
        row for row in driver.find_elements(by=By.XPATH, value="//table/tbody/tr") if context.reference_code in row.text
    ]
    assert len(application_row) == 1
    application_row = application_row[0]

    application_link = application_row.find_element(by=By.XPATH, value=".//td/a")
    application_link.click()


@when("I proceed to edit this application")
def edit_this_application(driver):
    driver.find_element(by=By.LINK_TEXT, value="Edit").click()


@then("I see confirmation page to open application for editing")
def confirmation_page_editing_application(driver, context):
    assert (
        driver.find_element(by=By.CSS_SELECTOR, value="h1").text
        == "Are you sure you want to open your application for editing?"
    )
    body = "\n".join(element.text for element in driver.find_elements(by=By.CLASS_NAME, value="govuk-body"))
    assert f"Your own application reference '{context.exporter_reference}' will remain the same" in body


@when("I confirm to edit the application")
def confirm_editing_application(driver):
    functions.click_submit(driver)


@then("I see task list of amended application")
def amended_application_task_list(driver, context):
    assert "task-list" in driver.current_url
    assert driver.find_elements(by=By.CLASS_NAME, value="lite-task-list")

    amended_application_id = re.findall(r"/applications/([A-Za-z0-9\-]+)", driver.current_url)
    assert amended_application_id

    context.amended_application_id = amended_application_id[0]


@then("the application cannot be opened for editing")
def cannot_edit_application(driver, context):
    all_links = driver.find_elements(by=By.CSS_SELECTOR, value="a")
    assert "Edit" not in [item.text for item in all_links]

    edit_url = f"/applications/{context.application_id}/major-edit-confirm/"
    assert edit_url not in [item.get_property("href") for item in all_links]


@then(parsers.parse('the application status is "{status}"'))
def confirm_editing_application(driver, status):
    assert driver.find_element(by=By.ID, value="label-application-status").text == status


@then("I see new application ready for amendments under drafts")
def amended_application_under_drafts(driver, context):
    driver.find_element(by=By.ID, value="applications-tab-drafts").click()

    assert context.amended_application_id
    task_list_url = f"/applications/{context.amended_application_id}/task-list/"
    assert driver.find_element(by=By.XPATH, value=f'//a[@href="{task_list_url}"]')


@when(parsers.parse("I go to task list of the amended draft application"))
def amended_application_task_list(driver, context):
    driver.find_element(by=By.CLASS_NAME, value="govuk-header__link--service-name").click()
    driver.find_element(by=By.ID, value="link-applications").click()
    driver.find_element(by=By.ID, value="applications-tab-drafts").click()

    # There could be multiple drafts with the same reference so use the
    # application_id to find the correct element
    assert context.amended_application_id
    task_list_url = f"/applications/{context.amended_application_id}/task-list/"
    driver.find_element(by=By.XPATH, value=f'//a[@href="{task_list_url}"]').click()


@when(parsers.parse('I click on "{link_text}" section'))
def click_link_by_text(driver, link_text):
    driver.find_element(by=By.LINK_TEXT, value=link_text).click()


@then(parsers.parse("I see products with below details as json:\n{product_details}"))
def add_products_to_application(driver, context, product_details):

    product_details = json.loads(product_details)

    product_rows = driver.find_elements(by=By.XPATH, value="//table/tbody/tr")
    assert len(product_rows) == len(context.good_on_application_ids)

    names = [row.find_element(by=By.XPATH, value=".//th").text for row in product_rows]
    assert names == product_details

    remove_urls = [row.find_elements(by=By.XPATH, value=".//td/a")[-1].get_property("href") for row in product_rows]
    amended_good_on_application_ids = [
        re.findall(r"/good-on-application/([A-Za-z0-9\-]+)/remove", url)[0] for url in remove_urls
    ]

    assert set(amended_good_on_application_ids).isdisjoint(set(context.good_on_application_ids))


@then(parsers.parse('I see Consignee with details "{consignee_name}", "{consignee_address}"'))
def check_consignee_details(driver, consignee_name, consignee_address):
    assert driver.find_element(by=By.ID, value="name").text.strip() == consignee_name
    assert driver.find_element(by=By.ID, value="address").text.strip() == consignee_address


@then(parsers.parse('I see End-user with details "{end_user_name}", "{end_user_address}"'))
def check_end_user_details(driver, end_user_name, end_user_address):
    all_values = driver.find_elements(by=By.CLASS_NAME, value="govuk-summary-list__value")
    assert all_values[1].text.strip() == end_user_name
    assert all_values[3].text.strip() == end_user_address


@when(parsers.parse('I edit exporter reference as "{reference}" and submit'))
def edit_exporter_reference(driver, reference):
    name = driver.find_element(by=By.ID, value="name")
    name.clear()
    name.send_keys(reference)
    functions.click_submit(driver)


@then(parsers.parse('I see exporter reference updated as "{expected}"'))
def check_updated_exporter_reference(driver, expected):
    all_elements = driver.find_elements(by=By.CLASS_NAME, value="lite-task-list__item-details")
    assert len(all_elements) > 0

    actual = all_elements[0].find_element(by=By.XPATH, value=".//p").text
    assert actual == expected
