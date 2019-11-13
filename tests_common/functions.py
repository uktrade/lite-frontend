import conftest


def click_submit(driver: conftest):
    element = driver.find_element_by_css_selector("button[value='submit']")
    driver.execute_script("arguments[0].click();", element)


def click_back_link(driver: conftest):
    driver.find_element_by_id("back-link").click()
