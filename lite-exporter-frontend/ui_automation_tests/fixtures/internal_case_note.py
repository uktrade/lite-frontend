from pytest import fixture
from pages.application_page import ApplicationPage
from conf.settings import env


@fixture(scope="module")
def internal_case_note(driver, request, internal_url, sso_sign_in_url, context):
    driver.get(sso_sign_in_url)
    sso_email = env('TEST_SSO_EMAIL')
    sso_password = env('TEST_SSO_PASSWORD')
    driver.find_element_by_name("username").send_keys(sso_email)
    driver.find_element_by_name("password").send_keys(sso_password)
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)
    driver.find_element_by_xpath("//*[text()[contains(.,'" + context.app_id + "')]]").click()
    application_page = ApplicationPage(driver)
    text = "I love toast"
    context.text = text
    application_page.enter_case_note(text)
    application_page.click_visible_to_exporter_checkbox()
    application_page.click_post_note_btn()
    alert = driver.switch_to_alert()
    alert.accept()
