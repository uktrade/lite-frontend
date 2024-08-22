from pytest_bdd import when, scenarios
from selenium.webdriver.common.by import By


scenarios("../../features/give_advice/lu_licence_change_status.feature", strict_gherkin=False)


@when("I log out as current user")
def click_the_logout_link(driver):
    driver.find_element(by=By.LINK_TEXT, value="Sign out").click()


# Log out as current user
# Log in as a user with the role "Licensing Unit Senior Manager"
# Go to the "Cases" page
# Filter for the case with licence status "finalised"
# Click on the case
# Click on the "Change licence status" button
# Select the new licence status "suspended"
# Assert that it's visible in the UI
