from datetime import datetime

from pytest_bdd import when, then, scenarios, parsers
from selenium.webdriver.common.by import By


scenarios("../../features/give_advice/siel_licence_document.feature", strict_gherkin=False)


@when("I start generating licence approval document")
def generate_licence_approval_document(driver):
    generate = driver.find_element(by=By.ID, value="generate-document-approve")
    generate.click()


@when("I start generating no licence required document")
def generate_nlr_document(driver):
    generate = driver.find_element(by=By.ID, value="generate-document-no_licence_required")
    generate.click()


def check_document_status(driver, decision_type):
    document_row = driver.find_element(by=By.ID, value=f"decision-{decision_type}")
    status = driver.find_element(by=By.ID, value=f"status-{decision_type}")
    assert status.text == "DONE"

    # Check that document regenerate and view links are displayed
    for link in document_row.find_elements(by=By.XPATH, value=".//td/a"):
        assert link.is_displayed()
        assert link.text in ["Regenerate", "View"]


@then("licence approval document is generated")
def licence_approval_document_generated(driver):
    check_document_status(driver, "approve")


@then("NLR letter is generated")
def nlr_letter_generated(driver):
    check_document_status(driver, "no_licence_required")


@then(parsers.parse('I check that licence is valid for "{valid_years:d}" years'))
def check_licence_validity_period(driver, valid_years):
    start_date_column = driver.find_element(by=By.ID, value="licence-start-date")
    start_date_string = start_date_column.find_element(
        by=By.XPATH, value=".//span[contains(@class, 'cell__uppercase')]"
    ).text
    start_date = datetime.strptime(start_date_string, "%d %B %Y")

    end_date_column = driver.find_element(by=By.ID, value="licence-end-date")
    end_date_string = end_date_column.find_element(
        by=By.XPATH, value=".//span[contains(@class, 'cell__uppercase')]"
    ).text
    end_date = datetime.strptime(end_date_string, "%d %B %Y")

    assert (end_date.year - start_date.year) == valid_years


@then(parsers.parse('I check that export type is "{export_type}"'))
def check_export_type(driver, export_type):
    element = driver.find_element(by=By.ID, value="export-type")
    actual_export_type = element.find_element(by=By.XPATH, value=".//span[contains(@class, 'cell__uppercase')]").text

    assert export_type.lower() == actual_export_type.lower()


@then(parsers.parse('I check that consignee details as "{expected_name}", "{expected_address}", "{expected_country}"'))
def check_consignee_details(driver, expected_name, expected_address, expected_country):
    consignee_column = driver.find_element(by=By.ID, value="consignee-details")
    details_text = consignee_column.find_element(by=By.XPATH, value=".//span[contains(@class, 'cell__uppercase')]").text
    actual_name, actual_address, actual_country = details_text.split("\n")

    assert expected_name.lower() == actual_name.strip().lower()
    assert expected_address.lower() == actual_address.strip().lower()
    assert expected_country.lower() == actual_country.strip().lower()


@then(parsers.parse('I check that end-user details as "{expected_name}", "{expected_address}", "{expected_country}"'))
def check_end_user_details(driver, expected_name, expected_address, expected_country):
    end_user_column = driver.find_element(by=By.ID, value="end-user-details")
    details_text = end_user_column.find_element(by=By.XPATH, value=".//span[contains(@class, 'cell__uppercase')]").text
    actual_name, actual_address, actual_country = details_text.split("\n")

    assert expected_name.lower() == actual_name.strip().lower()
    assert expected_address.lower() == actual_address.strip().lower()
    assert expected_country.lower() == actual_country.strip().lower()


@then(parsers.parse('I check that licence document contains "{num_products:d}" products'))
def check_number_of_licenceable_products(driver, num_products):
    products_table = driver.find_element(by=By.ID, value="products-table")
    product_rows = products_table.find_elements(by=By.XPATH, value=".//tr[contains(@id, 'product-row-')]")

    assert len(product_rows) == num_products


@then(
    parsers.parse(
        'I check that product "{index}" name is "{name}", part number "{part_number}", serial numbers "{serial_numbers}"'
    )
)
def check_product_details_on_the_document(driver, index, name, part_number, serial_numbers):
    product = driver.find_element(by=By.ID, value=f"product-row-{index}")
    name_row = product.find_element(by=By.ID, value=f"row-{index}-description-name")
    part_number_row = product.find_element(by=By.ID, value=f"row-{index}-description-part-number")

    # we display serial numbers as numbered
    # 12345 - 1
    # SN123 - 2
    sn_string = "\n".join([f"{num} - {index}" for index, num in enumerate(serial_numbers.split(","), start=1) if num])
    serial_numbers_row = product.find_element(by=By.ID, value=f"row-{index}-description-serial-numbers")

    assert f"Name: {name}" == name_row.text
    assert f"Part number: {part_number}" == part_number_row.text
    assert f"Serial number: {sn_string}" == serial_numbers_row.text


@then(parsers.parse('I check that product "{index}" name is "{name}", part number "{part_number}", no serial numbers'))
def check_product_details_on_the_document_no_serial_numbers(driver, index, name, part_number):
    product = driver.find_element(by=By.ID, value=f"product-row-{index}")
    name_row = product.find_element(by=By.ID, value=f"row-{index}-description-name")
    part_number_row = product.find_element(by=By.ID, value=f"row-{index}-description-part-number")
    serial_numbers_row = product.find_element(by=By.ID, value=f"row-{index}-description-serial-numbers-na")

    assert f"Name: {name}" == name_row.text
    assert f"Part number: {part_number}" == part_number_row.text
    assert f"Serial number: N/A" == serial_numbers_row.text


@then(
    parsers.parse('I check that product "{index}" control entries are "{cles}", value "{value}", quantity "{quantity}"')
)
def check_product_cle_value_quantity(driver, index, cles, value, quantity):
    product = driver.find_element(by=By.ID, value=f"product-row-{index}")
    cles_row = product.find_element(by=By.ID, value=f"row-{index}-control-list-entries")
    value_row = product.find_element(by=By.ID, value=f"row-{index}-value")
    quantity_row = product.find_element(by=By.ID, value=f"row-{index}-quantity")

    assert cles == cles_row.text
    assert value == value_row.text
    assert quantity == quantity_row.text


@then(parsers.parse('I check that licence has additional conditions as "{provisos}"'))
def check_licence_provisos(driver, provisos):
    conditions = driver.find_element(by=By.ID, value="terms-and-conditions-table-last-row")
    assert conditions.is_displayed()

    conditions_text = driver.find_element(by=By.CLASS_NAME, value="terms-and-conditions-paragraph")
    assert conditions_text.text == provisos


@then(parsers.parse('I check that no licence required letter contains "{num_products:d}" products'))
def check_number_of_nlr_products(driver, num_products):
    products_table = driver.find_element(by=By.ID, value="nlr-products-table")
    product_rows = products_table.find_elements(by=By.XPATH, value=".//tr[contains(@id, 'nlr-product-row-')]")

    assert len(product_rows) == num_products


@then(parsers.parse('I check that NLR product "{index}" name is "{name}", part number "{part_number}"'))
def check_nlr_product_details_on_the_document(driver, index, name, part_number):
    product = driver.find_element(by=By.ID, value=f"nlr-product-row-{index}")
    assert product.text == f"{index} {name} {part_number}"
