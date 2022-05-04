import os
import time

from pytest_bdd import when, scenarios, then, parsers
import xml.etree.ElementTree as ET

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ui_tests.caseworker.pages.application_page import ApplicationPage
from ui_tests.caseworker.pages.case_list_page import CaseListPage
from ui_tests.caseworker.pages.shared import Shared


scenarios("../features/enforcement.feature", strict_gherkin=False)


@when("I click export enforcement xml")
def export_enforcement_xml(driver):
    CaseListPage(driver).click_export_enforcement_xml()


@then("the enforcement check is audited")
def enforcement_audit(driver, internal_url, context):
    ApplicationPage(driver).go_to_cases_activity_tab(internal_url, context)
    assert "exported the case for enforcement check" in Shared(driver).get_audit_trail_text()


@then(parsers.parse('the file "{filename}" is downloaded'))
def enforcement_file_download_check(filename):
    assert filename in os.listdir("/tmp")


@then("an XML file is downloaded onto my device")
def xml_file_downloaded(driver):
    i = 10
    EU_XML_PATH = "/tmp/enforcement_check.xml"
    while not os.path.exists(EU_XML_PATH) and i > 0:
        time.sleep(0.1)
        i -= 1

    assert os.path.exists(EU_XML_PATH)


@then(parsers.parse('the downloaded file should include "{party_type}" "{tag}" as "{value}"'))
def enforcement_file_content_check(party_type, tag, value):
    tree = ET.parse("/tmp/enforcement_check.xml")
    root = tree.getroot()

    # get values of all party_types as the file can contain multiple entries
    nodes = root.findall(f".//STAKEHOLDER[SH_TYPE='{party_type}']")
    party_values = set([child.text for node in nodes for child in node if child.tag == tag])
    assert value in party_values


@when(parsers.parse('I include "{party_type}" details and generate import file'))
def generate_enforcement_check_import_file(party_type):
    tree = ET.parse("/tmp/enforcement_check.xml")
    root = tree.getroot()

    # get values of all party_types as the file can contain multiple entries
    nodes = root.findall(f".//STAKEHOLDER[SH_TYPE='{party_type}']")
    assert len(nodes) >= 1
    code1_list = []
    code2_list = []
    for node in nodes:
        for item in list(node):
            if item.tag == "ELA_ID":
                code1_list.append(item.text)
            if item.tag == "SH_ID":
                code2_list.append(item.text)

    assert len(code1_list) > 0
    assert len(code2_list) > 0
    assert len(code1_list) == len(code2_list)
    import_xml_string = '<?xml version="1.0" ?>\n<SPIRE_UPLOAD_FILE>\n'
    for code1, code2 in zip(code1_list, code2_list):
        import_xml_string += (
            f"<SPIRE_RETURNS><CODE1>{code1}</CODE1><CODE2>{code2}</CODE2><FLAG>N</FLAG></SPIRE_RETURNS>\n"
        )

    import_xml_string += "</SPIRE_UPLOAD_FILE>\n"

    with open("/tmp/enforcement_check_import.xml", "w") as f:
        f.write(import_xml_string)


@then(parsers.parse('for FLAG the file has "{flag_value}"'))
def enforcement_file_content_check(flag_value):
    tree = ET.parse("/tmp/enforcement_check_import.xml")
    root = tree.getroot()

    # get values of all party_types as the file can contain multiple entries
    for node in root.findall(f".//SPIRE_RETURNS/FLAG"):
        assert node.text == flag_value


@then(parsers.parse('for "{import_tag}" the file has the "{party_type}" data "{export_tag}" number from export file'))
def compare_import_tags_with_export_tags(import_tag, party_type, export_tag):
    # Extract ELA_ID, SH_ID from the export xml file for given party
    tree = ET.parse("/tmp/enforcement_check.xml")
    root = tree.getroot()

    data = []
    for node in root.findall(f".//STAKEHOLDER[SH_TYPE='{party_type}']"):
        data.append(
            {
                f"{export_tag}": node.find(f".//{export_tag}").text,
            }
        )

    tree = ET.parse("/tmp/enforcement_check_import.xml")
    root = tree.getroot()

    # compare the values in the file to be imported for the given party
    for index, node in enumerate(root.findall(f".//SPIRE_RETURNS/{import_tag}")):
        assert node.text == data[index][export_tag]


@when(parsers.parse('I click on "{import_eu_btn_text}"'))
def import_enforcement_xml(driver, import_eu_btn_text):
    CaseListPage(driver).click_by_link_text(import_eu_btn_text)


@when("I attach the file above")
def i_attach_updated_file(driver):  # noqa
    file_input = driver.find_element(by=By.NAME, value="file")
    file_input.clear()
    file_input.send_keys("/tmp/enforcement_check_import.xml")
    upload_btn = driver.find_element(by=By.XPATH, value="//button[@type='submit']")
    upload_btn.click()

    banner = driver.find_element(by=By.CLASS_NAME, value="app-snackbar__content")
    assert "Enforcement XML imported successfully" in banner.text

    driver.find_element(by=By.LINK_TEXT, value="Back to queue").click()


@then(parsers.parse('the application is removed from "{queue}" queue'))
def application_removed_from_queue(driver, queue):
    ASSIGNED_QUEUES_ID = "assigned-queues"
    WebDriverWait(driver, 30).until(
        expected_conditions.presence_of_element_located((By.ID, ASSIGNED_QUEUES_ID))
    ).is_enabled()
    queue_list = driver.find_element(by=By.ID, value=ASSIGNED_QUEUES_ID).text.split("\n")
    assert queue not in queue_list


@when("I cleanup the temporary files created")
def clean_temporary_files():
    download_dir = "/tmp"
    for file in [f for f in os.listdir(download_dir) if f.endswith(".xml")]:
        try:
            os.remove(f"{download_dir}/{file}")
        except OSError:
            pass
