import os
from pytest_bdd import when, scenarios, then, parsers
import xml.etree.ElementTree as ET

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


@then(parsers.parse('the downloaded file should include "{party_type}" "{tag}" as "{value}"'))
def enforcement_file_content_check(party_type, tag, value):
    tree = ET.parse("/tmp/enforcement_check.xml")
    root = tree.getroot()

    # get values of all party_types as the file can contain multiple entries
    nodes = root.findall(f".//STAKEHOLDER[SH_TYPE='{party_type}']")
    party_values = set([child.text for node in nodes for child in node.getchildren() if child.tag == tag])
    assert value in party_values
