import os

from pytest import fixture
from pages.add_goods_page import AddGoodPage
from pages.attach_document_page import AttachDocumentPage
from pages.exporter_hub_page import ExporterHubPage
import helpers.helpers as utils
from pages.application_overview_page import ApplicationOverviewPage
from pages.application_goods_list import ApplicationGoodsList
from pages.shared import Shared


@fixture(scope="session")
def add_a_good(driver, request):
    exporter_hub = ExporterHubPage(driver)
    good_name = "What Widget"
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
    good_name = "Incorporated Fuel"
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
        attach_document_page = AttachDocumentPage(driver)

        # Path gymnastics to get the absolute path for $PWD/../resources/(file_to_upload_x) that works everywhere
        file_to_upload_abs_path = \
            os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'resources', 'file_for_doc_upload_test_1.txt'))
        if 'ui_automation_tests' not in file_to_upload_abs_path:
            file_to_upload_abs_path = \
                os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'ui_automation_tests/resources', 'file_for_doc_upload_test_1.txt'))

        attach_document_page.choose_file(file_to_upload_abs_path)
        attach_document_page.enter_description('nothing')
        Shared(driver).click_continue()
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
    good_name = "More Fuel"
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
        attach_document_page = AttachDocumentPage(driver)

        # Path gymnastics to get the absolute path for $PWD/../resources/(file_to_upload_x) that works everywhere
        file_to_upload_abs_path = \
            os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'resources', 'file_for_doc_upload_test_1.txt'))
        if 'ui_automation_tests' not in file_to_upload_abs_path:
            file_to_upload_abs_path = \
                os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'ui_automation_tests/resources', 'file_for_doc_upload_test_1.txt'))

        attach_document_page.choose_file(file_to_upload_abs_path)
        attach_document_page.enter_description('nothing')
        Shared(driver).click_continue()
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


@fixture(scope='function')
def create_non_incorporated_good(driver, request, context):
    good_name = "Modifiable Good " + utils.get_formatted_date_time_m_d_h_s()
    context.goods_name = good_name
    exporter_hub = ExporterHubPage(driver)
    driver.get(request.config.getoption("--exporter_url"))
    exporter_hub.click_my_goods()
    add_goods_page = AddGoodPage(driver)
    add_goods_page.click_add_a_good()
    exporter_hub = ExporterHubPage(driver)
    add_goods_page = AddGoodPage(driver)
    add_goods_page.enter_description_of_goods(good_name)
    add_goods_page.select_is_your_good_controlled("Yes")
    add_goods_page.select_is_your_good_intended_to_be_incorporated_into_an_end_product("No")
    add_goods_page.enter_control_code("1234")
    exporter_hub.click_save_and_continue()
    context.file_to_be_deleted_name = 'file_for_doc_upload_test_2.txt'
    # Path gymnastics to get the absolute path for $PWD/../resources/(file_to_upload_x) that works everywhere
    file_to_upload_abs_path = \
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'resources', context.file_to_be_deleted_name))
    if 'ui_automation_tests' not in file_to_upload_abs_path:
        file_to_upload_abs_path = \
            os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'ui_automation_tests/resources', context.file_to_be_deleted_name))

    attach_document_page = AttachDocumentPage(driver)
    attach_document_page.choose_file(file_to_upload_abs_path)
    context.document_description = utils.get_formatted_date_time_m_d_h_s()
    attach_document_page.enter_description(context.document_description)
    Shared(driver).click_continue()
