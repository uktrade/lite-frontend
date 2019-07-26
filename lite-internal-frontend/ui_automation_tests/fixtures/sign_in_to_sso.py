from pytest import fixture


@fixture(scope="function")
def sign_in_to_internal_sso(driver, internal_url, sso_sign_in_url, sso_login_info):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(sso_login_info['email'])
    driver.find_element_by_name("password").send_keys(sso_login_info['password'])
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)
