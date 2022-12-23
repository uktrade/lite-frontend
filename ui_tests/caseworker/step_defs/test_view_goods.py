from pytest_bdd import scenarios, when, then

scenarios("../features/view_goods.feature", strict_gherkin=False)


@when("I click the first good on the case")  # noqa
def click_good_on_case(driver, context):
    driver.find_element_by_link_text(context.goods[0]["good"]["name"]).click()


@then("I see the good details")  # noqa
def good_details_visible(driver, context):
    assert driver.find_element_by_tag_name("h2").text == "Product details"
    assert driver.find_element_by_css_selector("div.govuk-caption-l").text == context.goods[0]["good"]["name"]
