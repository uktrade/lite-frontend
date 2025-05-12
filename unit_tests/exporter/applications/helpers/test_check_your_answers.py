import pytest
import re

from bs4 import BeautifulSoup
from django.urls import reverse

from core import client
from core.constants import CaseStatusEnum
from exporter.applications.helpers import check_your_answers

from exporter.core.objects import Application


@pytest.fixture
def application(data_standard_case):
    return data_standard_case["case"]["data"]


@pytest.fixture
def mock_application_get(requests_mock, data_standard_case):
    application = data_standard_case["case"]["data"]
    url = client._build_absolute_uri(f'/applications/{application["id"]}/')
    return requests_mock.get(url=url, json=application)


@pytest.fixture
def mock_application_history_get(requests_mock, data_standard_case):
    application = data_standard_case["case"]["data"]
    url = client._build_absolute_uri(f'/exporter/applications/{application["id"]}/history')
    return requests_mock.get(url=url, json={})


def test_convert_goods_on_application_no_answers(application, data_good_on_application):
    # given the canonical good does not have is_good_controlled set
    data_good_on_application["is_good_controlled"] = None
    data_good_on_application["control_list_entries"] = []
    data_good_on_application["good"]["is_good_controlled"] = None
    data_good_on_application["good"]["control_list_entries"] = []
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])

    # then the differences in export characteristics are highlighted
    assert len(actual) == 1
    assert actual[0]["Control list entries"] == '<span class="govuk-hint govuk-!-margin-0">N/A</span>'


def test_convert_goods_on_application_application_level_control_list_entries(application, data_good_on_application):
    data_good_on_application["control_list_entries"] = []
    data_good_on_application["good"]["control_list_entries"] = []

    # given the canonical good and good in application have different export control characteristics
    # when the shape is generated
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])

    # then the differences in export characteristics are highlighted
    assert len(actual) == 1
    assert actual[0]["Control list entries"] == '<span class="govuk-hint govuk-!-margin-0">N/A</span>'


def test_convert_goods_on_application_application_level_control_list_entries_same(
    application, data_good_on_application
):
    # given the canonical good and good in application have same export control characteristics
    data_good_on_application["good"]["is_good_controlled"] = data_good_on_application["is_good_controlled"]
    data_good_on_application["good"]["control_list_entries"] = data_good_on_application["control_list_entries"]

    # when the shape is generated
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])

    # then no difference is highlighted
    assert len(actual) == 1
    assert actual[0]["Control list entries"] == (
        "<span data-definition-title='ML1' data-definition-text='Smooth-bore weapons...'>ML1</span>, "
        "<span data-definition-title='ML2' data-definition-text='Smooth-bore weapons...'>ML2</span>"
    )


def test_convert_goods_on_application_good_level_control_list_entries(application, data_good_on_application):
    # given the good has not been reviewed at application level
    data_good_on_application["is_good_controlled"] = None
    data_good_on_application["control_list_entries"] = []
    data_good_on_application["good"]["control_list_entries"] = []

    # when the shape is generated
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])

    # then no difference is highlighted
    assert len(actual) == 1
    assert actual[0]["Control list entries"] == '<span class="govuk-hint govuk-!-margin-0">N/A</span>'


def test_add_serial_numbers_link(application, data_good_on_application):
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]

    assert "firearm_details" not in data_good_on_application
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]

    data_good_on_application["firearm_details"] = None
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]

    data_good_on_application["firearm_details"] = {
        "serial_numbers_available": "NOT_AVAILABLE",
    }
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]

    data_good_on_application["firearm_details"] = {
        "number_of_items": 3,
        "serial_numbers_available": "AVAILABLE",
        "serial_numbers": [],
    }
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
    assert '<span class="govuk-visually-hidden">Actions</a>' in actual[0]

    data_good_on_application["firearm_details"] = {
        "number_of_items": 3,
        "serial_numbers_available": "AVAILABLE",
        "serial_numbers": [],
    }
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application], is_summary=True)
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]

    data_good_on_application["firearm_details"] = {
        "number_of_items": 3,
        "serial_numbers_available": "AVAILABLE",
        "serial_numbers": ["111", "222", "333"],
    }
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]

    allowed_case_statuses = [CaseStatusEnum.SUBMITTED, CaseStatusEnum.FINALISED]
    for case_status in allowed_case_statuses:
        application["status"]["key"] = case_status
        data_good_on_application["firearm_details"] = {
            "number_of_items": 3,
            "serial_numbers_available": "AVAILABLE",
            "serial_numbers": [],
        }
        actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
        assert '<span class="govuk-visually-hidden">Actions</a>' in actual[0]

    disallowed_case_statuses = set(CaseStatusEnum.all()) - set(allowed_case_statuses)
    for case_status in disallowed_case_statuses:
        application["status"]["key"] = case_status
        data_good_on_application["firearm_details"] = {
            "number_of_items": 3,
            "serial_numbers_available": "AVAILABLE",
            "serial_numbers": [],
        }
        actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
        assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]


def test_actions_column_is_balanced_across_rows(application, data_good_on_application):
    with_serial_numbers = {
        **data_good_on_application,
        **{
            "firearm_details": {
                "number_of_items": 3,
                "serial_numbers_available": "AVAILABLE",
                "serial_numbers": ["111", "222", "333"],
            }
        },
    }
    later_serial_numbers = {
        **data_good_on_application,
        **{
            "firearm_details": {
                "number_of_items": 3,
                "serial_numbers_available": "LATER",
                "serial_numbers": [],
            }
        },
    }

    actual = check_your_answers.convert_goods_on_application(application, [with_serial_numbers, with_serial_numbers])
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[1]

    actual = check_your_answers.convert_goods_on_application(application, [later_serial_numbers, later_serial_numbers])
    assert '<span class="govuk-visually-hidden">Actions</a>' in actual[0]
    assert '<span class="govuk-visually-hidden">Actions</a>' in actual[1]

    actual = check_your_answers.convert_goods_on_application(application, [with_serial_numbers, later_serial_numbers])
    assert '<span class="govuk-visually-hidden">Actions</a>' in actual[0]
    assert '<span class="govuk-visually-hidden">Actions</a>' in actual[1]


@pytest.mark.parametrize(
    "security_data, expected",
    (
        ({"is_mod_security_approved": False}, {"Do you have an MOD security approval, such as F680 or F1686?": "No"}),
        (
            {
                "is_mod_security_approved": True,
                "security_approvals": ["F680"],
                "subject_to_itar_controls": True,
                "f680_reference_number": "Test Ref",
            },
            {
                "Do you have an MOD security approval, such as F680 or F1686?": "Yes",
                "What type of approval do you have?": "F680",
                "Are any products on this application subject to ITAR controls?": "Yes",
                "What is the F680 reference number?": "Test Ref",
            },
        ),
        (
            {
                "is_mod_security_approved": True,
                "security_approvals": ["F1686"],
                "f1686_reference_number": "Test Ref f1686",
                "f1686_approval_date": "2020-02-02",
            },
            {
                "Do you have an MOD security approval, such as F680 or F1686?": "Yes",
                "What type of approval do you have?": "F1686",
                "What is the F1686 reference number?": "Test Ref f1686",
                "When was the F1686 approved?": "2 February 2020",
            },
        ),
        (
            {
                "is_mod_security_approved": True,
                "security_approvals": ["Other"],
                "other_security_approval_details": "other approval details",
            },
            {
                "Do you have an MOD security approval, such as F680 or F1686?": "Yes",
                "What type of approval do you have?": "Other written approval",
                "Provide details of your written approval": "other approval details",
            },
        ),
    ),
)
def test_get_security_approvals(security_data, expected):
    application = Application(security_data)
    actual = check_your_answers._get_security_approvals(application)
    assert actual == expected


def test_convert_standard_application_has_security_approvals(application):
    test_application = Application(application)
    actual = check_your_answers.convert_application_to_check_your_answers(test_application)
    assert "Do you have a security approval?" in actual.keys()


def test_application_detail_shows_correct_cles(
    authorized_client, mock_application_get, mock_application_history_get, application
):
    url = reverse("applications:application", kwargs={"pk": application["id"]})
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    products_table = soup.find("table", attrs={"id": "table-application-products"})
    products_cles = []
    body = products_table.find("tbody")
    rows = body.find_all("tr")

    for row in rows:
        product_line = row.text.replace("\t", "").strip()
        product_line = re.sub(r"([\W_])\1+", r"\1", product_line)
        lines = product_line.split("\n")
        products_cles.append(lines[3])

    for index, good_on_application in enumerate(application["goods"]):
        expected_cles = ", ".join(item["rating"] for item in good_on_application["control_list_entries"])
        assert expected_cles == products_cles[index]
