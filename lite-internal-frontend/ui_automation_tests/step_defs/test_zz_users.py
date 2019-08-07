from selenium.webdriver.common.by import By
import helpers.helpers as utils
import pytest
from conf.settings import env
import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)
from pages.users_page import UsersPage
from pages.header_page import HeaderPage
from pages.users_page import UsersPage


sso_email=env('TEST_SSO_EMAIL')
sso_password=env('TEST_SSO_PASSWORD')


@pytest.fixture(scope="function")
def open_internal_hub(driver, internal_url, sso_sign_in_url):
    driver.get(internal_url)
    if "login" in driver.current_url:
        driver.get(sso_sign_in_url)
        driver.find_element_by_name("username").send_keys(sso_email)
        driver.find_element_by_name("password").send_keys(sso_password)
        driver.find_element_by_css_selector("[type='submit']").click()
        driver.get(internal_url)


def test_manage_users(driver, open_internal_hub, context):
    time = utils.get_formatted_date_time_m_d_h_s()
    email = time + "@mail.com"
    context.email_to_search = email
    header = HeaderPage(driver)
    user_page = UsersPage(driver)
    header.open_users()

    user_page.click_add_a_user_btn()
    user_page.enter_email(email)
    user_page.select_option_from_team_drop_down_by_visible_text("Admin")
    user_page.select_option_from_role_drop_down_by_visible_text("Default")

    user_page.click_save_and_continue()

    assert driver.find_element_by_tag_name("h1").text == "Users", \
        "Failed to return to Users list page after Adding user"

    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='" + context.email_to_search + "']/following-sibling::td[text()='Active']")

    email_edited = "edited" + email
    user_page.click_edit_for_user(email)
    # invalid checks
    user_page.enter_email(sso_email)
    user_page.select_option_from_team_drop_down_by_visible_text("Admin")
    user_page.click_save_and_continue()
    assert "This field must be unique." in driver.find_element_by_css_selector(".govuk-error-message").text
    user_page.enter_email("invalidemail")
    user_page.click_save_and_continue()
    assert "Enter an email address in the correct format, like name@example.com" in driver.find_element_by_css_selector(".govuk-error-message").text
    # valid edit checks
    user_page.enter_email(email_edited)

    user_page.select_option_from_team_drop_down_by_value()
    user_page.select_option_from_role_drop_down_by_visible_text('Default')

    # When I Save
    user_page.click_save_and_continue()

    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + email_edited + "')]]")
    assert "Admin" not in driver.find_element_by_xpath("//td[text()='" + email_edited + "']/following-sibling::td[text()]").text


def test_inability_to_deactivate_oneself(driver, open_internal_hub):
    header = HeaderPage(driver)
    header.click_user_profile()
    deactivate = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Deactivate')]]")
    assert not deactivate


def test_invalid(driver, open_internal_hub):
    header = HeaderPage(driver)
    user_page = UsersPage(driver)

    header.open_users()
    user_page.click_add_a_user_btn()
    user_page.enter_email(sso_email)
    user_page.select_option_from_team_drop_down_by_visible_text("Admin")
    user_page.select_option_from_role_drop_down_by_visible_text("Default")
    user_page.click_save_and_continue()
    assert "This field must be unique." in driver.find_element_by_css_selector(".govuk-error-message").text
    user_page.enter_email("invalidemail")
    user_page.click_save_and_continue()
    assert "Enter an email address in the correct format, like name@example.com" in driver.find_element_by_css_selector(".govuk-error-message").text
    user_page.enter_email("")
    user_page.select_option_from_team_drop_down_by_visible_text("Select")
    user_page.click_save_and_continue()
    assert "Enter an email address in the correct format, like name@example.com" in driver.find_element_by_css_selector(".govuk-error-message").text
    #TODO uncomment this when error message bug is fixed
    # assert "Select a team" in driver.find_elements_by_css_selector(".govuk-error-message")[1].text


def test_teardown(driver):
    driver.quit()
