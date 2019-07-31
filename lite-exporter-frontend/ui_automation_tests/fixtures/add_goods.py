from pytest import fixture
from pages.add_goods_page import AddGoodPage
from pages.exporter_hub_page import ExporterHubPage
import helpers.helpers as utils
from pages.application_overview_page import ApplicationOverviewPage
from pages.application_goods_list import ApplicationGoodsList


@fixture(scope="session")
def add_a_good(driver, request):
    exporter_hub = ExporterHubPage(driver)
    good_name = "1Widget"
    exporter_hub.click_my_goods()
    add_goods_page = AddGoodPage(driver)
    if good_name not in driver.find_element_by_css_selector('.govuk-table').text:
        add_goods_page.click_add_a_good()
        exporter_hub = ExporterHubPage(driver)
        add_goods_page = AddGoodPage(driver)
        add_goods_page.enter_description_of_goods(good_name)
        add_goods_page.select_is_your_good_controlled("Yes")
        add_goods_page.select_is_your_good_intended_to_be_incorporated_into_an_end_product("no")
        add_goods_page.enter_control_code("1234")
        exporter_hub.click_save_and_continue()
    driver.get(request.config.getoption("--exporter_url"))


@fixture(scope="function")
def add_an_incorporated_good_to_application(driver, request, context):
    url = driver.current_url
    good_name = "Incorporated Seat"
    context.goods_name = good_name
    exporter_hub = ExporterHubPage(driver)
    driver.get(request.config.getoption("--exporter_url"))
    exporter_hub.click_my_goods()
    add_goods_page = AddGoodPage(driver)
    overview_page = ApplicationOverviewPage(driver)
    if good_name not in driver.find_element_by_css_selector('.govuk-table').text:
        add_goods_page.click_add_a_good()
        exporter_hub = ExporterHubPage(driver)
        add_goods_page = AddGoodPage(driver)
        add_goods_page.enter_description_of_goods(good_name)
        add_goods_page.select_is_your_good_controlled("Yes")
        add_goods_page.select_is_your_good_intended_to_be_incorporated_into_an_end_product("Yes")
        add_goods_page.enter_control_code("1234")
        exporter_hub.click_save_and_continue()
    driver.get(url)
    driver.execute_script("document.getElementById('goods').scrollIntoView(true);")
    overview_page.click_goods_link()
    driver.find_element_by_css_selector('a[href*="add-preexisting"]').click()
    elements = driver.find_elements_by_css_selector('.lite-card')
    no = utils.get_element_index_by_partial_text(elements, good_name)
    driver.find_elements_by_css_selector('.lite-card .govuk-button')[no].click()
    application_goods_list = ApplicationGoodsList(driver)
    context.unit = "Number of articles"
    context.value ="11"
    application_goods_list.add_values_to_good(str(context.value), str(context.value), context.unit)
    driver.find_element_by_css_selector("button[type*='submit']").click()
    driver.get(url)


@fixture(scope="function")
def add_a_non_incorporated_good_to_application(driver, request, context):
    url = driver.current_url
    good_name = "Jet Fuel"
    context.goods_name = good_name
    exporter_hub = ExporterHubPage(driver)
    driver.get(request.config.getoption("--exporter_url"))
    exporter_hub.click_my_goods()
    add_goods_page = AddGoodPage(driver)
    overview_page = ApplicationOverviewPage(driver)
    if good_name not in driver.find_element_by_css_selector('table').text:
        add_goods_page.click_add_a_good()
        exporter_hub = ExporterHubPage(driver)
        add_goods_page = AddGoodPage(driver)
        add_goods_page.enter_description_of_goods(good_name)
        add_goods_page.select_is_your_good_controlled("Yes")
        add_goods_page.select_is_your_good_intended_to_be_incorporated_into_an_end_product("No")
        add_goods_page.enter_control_code("1234")
        exporter_hub.click_save_and_continue()
    driver.get(url)
    driver.execute_script("document.getElementById('goods').scrollIntoView(true);")
    overview_page.click_goods_link()
    driver.find_element_by_css_selector('a[href*="add-preexisting"]').click()
    elements = driver.find_elements_by_css_selector('.lite-card')
    no = utils.get_element_index_by_partial_text(elements, good_name)
    driver.find_elements_by_css_selector('.lite-card .govuk-button')[no].click()
    application_goods_list = ApplicationGoodsList(driver)
    context.unit = "Number of articles"
    context.value ="11"
    application_goods_list.add_values_to_good(str(context.value), str(context.value), context.unit)
    driver.find_element_by_css_selector("button[type*='submit']").click()
    driver.get(url)
