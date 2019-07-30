from pytest import fixture
import helpers.helpers as utils
from conf.settings import env
from pages.header_page import HeaderPage
from pages.organisations_page import OrganisationsPage
from pages.organisations_form_page import OrganisationsFormPage
from selenium.webdriver.common.by import By


@fixture(scope="session")
def register_organisation(driver, request, sso_login_info, context):
    context.org_name = "Test Org"
    driver.get(request.config.getoption("--sso_sign_in_url"))
    driver.find_element_by_name("username").send_keys(sso_login_info['email'])
    driver.find_element_by_name("password").send_keys(sso_login_info['password'])
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(request.config.getoption("--internal_url"))
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_organisations()
    context.org_registered_status = False
    organisations_page = OrganisationsPage(driver)
    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + context.org_name + "')]]")
    if exists:
        context.org_registered_status = True
    else:
        organisations_page.click_new_organisation_btn()
        organisations_form_page = OrganisationsFormPage(driver)
        organisations_form_page.enter_name(context.org_name)
        organisations_form_page.enter_eori_number("1234567890AAA")
        organisations_form_page.enter_sic_number("2345")
        organisations_form_page.enter_vat_number("GB1234567")
        organisations_form_page.enter_registration_number("09876543")
        organisations_form_page.click_submit()
        organisations_form_page = OrganisationsFormPage(driver)
        organisations_form_page.enter_site_name("Headquarters")
        context.site_name = "Headquarters"
        organisations_form_page.enter_address_line_1("42 Question Road")
        organisations_form_page.enter_region("London")
        organisations_form_page.enter_post_code("Islington")
        organisations_form_page.enter_city("London")
        organisations_form_page.enter_country("Ukraine")
        organisations_form_page.click_submit()
        organisations_form_page = OrganisationsFormPage(driver)
        organisations_form_page.enter_email(env('TEST_EXPORTER_SSO_EMAIL'))
        context.email = env('TEST_EXPORTER_SSO_EMAIL')
        organisations_form_page.enter_first_name("Trinity")
        organisations_form_page.enter_last_name("Fishburne")
        organisations_form_page.click_submit()
