from pytest_bdd import scenarios, when, then, parsers

from selenium.webdriver.common.by import By

from tests_common import functions

scenarios("../features/goods_archive_restore.feature", strict_gherkin=False)


def get_product_row(driver, context, name):
    assert context.good_ids
    good_id = context.good_ids[name]

    product_rows = [
        item
        for item in driver.find_elements(by=By.CLASS_NAME, value="govuk-link")
        if good_id in item.get_property("href")
    ]
    return product_rows[0] if len(product_rows) > 0 else None


@when("I go to my products list")
def goto_products_list(driver):
    driver.find_element(by=By.CLASS_NAME, value="govuk-header__link--service-name").click()
    driver.find_element(by=By.ID, value="link-products").click()


@when(parsers.parse('I select the product "{name}" from the list to view details'))
def click_to_view_product_details(driver, context, name):
    product_row = get_product_row(driver, context, name)
    assert product_row

    product_row.click()


@then("I see an option to archive the product")
def see_archive_option(driver):
    assert driver.find_element(by=By.ID, value="archive-good").is_displayed()


@then("I see an option to restore the product")
def see_archive_option(driver):
    assert driver.find_element(by=By.ID, value="restore-good").is_displayed()


@when("I click to archive the product")
def click_archive_product(driver):
    driver.find_element(by=By.ID, value="archive-good").click()


@when("I click to restore the product")
def click_archive_product(driver):
    driver.find_element(by=By.ID, value="restore-good").click()


@then("I see a confirmation page to archive the product")
def confirmation_page_archive_product(driver, context):
    assert driver.find_element(by=By.CSS_SELECTOR, value="h1").text == "Are you sure you want to archive this product?"
    assert driver.find_element(by=By.ID, value="submit-id-submit").is_displayed()


@then("I see a confirmation page to restore the product")
def confirmation_page_archive_product(driver, context):
    assert driver.find_element(by=By.CSS_SELECTOR, value="h1").text == "Are you sure you want to restore this product?"
    assert driver.find_element(by=By.ID, value="submit-id-submit").is_displayed()


@when("I continue to archive the product")
@when("I continue to restore the product")
def continue_archive_restore_product(driver):
    functions.click_submit(driver)


@then(parsers.parse('the product "{name}" is archived'))
def product_is_archived(driver, context, name):
    driver.find_element(by=By.CLASS_NAME, value="govuk-header__link--service-name").click()
    driver.find_element(by=By.ID, value="link-products").click()

    # Archived products are not displayed in the products list so we should not
    # see any link to view product details
    assert get_product_row(driver, context, name) is None


@then(parsers.parse('the product "{name}" is restored'))
def product_is_archived(driver, context, name):
    driver.find_element(by=By.CLASS_NAME, value="govuk-header__link--service-name").click()
    driver.find_element(by=By.ID, value="link-products").click()

    # Restored products are again displayed in the products list
    assert get_product_row(driver, context, name)


@then(parsers.parse('I see the product "{name}" in the archived products list'))
def product_in_archived_list(driver, context, name):
    app_bar = driver.find_element(by=By.CLASS_NAME, value="lite-app-bar")
    archived_products = app_bar.find_element(by=By.XPATH, value=".//a")
    archived_products.click()

    product_row = get_product_row(driver, context, name)
    assert product_row


@then(parsers.parse('I do not see the product "{name}" in the archived products list'))
def product_not_in_archived_list(driver, context, name):
    app_bar = driver.find_element(by=By.CLASS_NAME, value="lite-app-bar")
    archived_products = app_bar.find_element(by=By.XPATH, value=".//a")
    archived_products.click()

    product_row = get_product_row(driver, context, name)
    assert product_row is None


@then(parsers.parse('I see archive history for the product with "{num_revisions:d}" revisions'))
def check_archive_history(driver, num_revisions):
    history = driver.find_element(by=By.ID, value="archive_history")
    history_items = history.find_elements(by=By.XPATH, value=".//p")
    assert len(history_items) == num_revisions
