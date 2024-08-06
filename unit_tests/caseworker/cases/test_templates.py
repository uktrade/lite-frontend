import pytest
from django.http import HttpRequest

from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from caseworker.core.constants import LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID

from caseworker.cases.objects import Case


def test_good_on_application_detail_unverified_product(data_good_on_application, data_standard_case):
    # given the product is not yet reviewed
    good_on_application = {**data_good_on_application}
    good_on_application["is_good_controlled"] = None

    # and the exporter told us the good is controlled
    good_on_application["good"]["is_good_controlled"] = {"key": "True", "value": "Yes"}

    context = {
        "good_on_application": good_on_application,
        "good_on_application_documents": [],
        "case": Case(data_standard_case["case"]),
        "other_cases": [],
        "data": {},
        "organisation_documents": {},
        "queue": {"id": "00000000-0000-0000-0000-000000000001"},
    }
    # then we show the is_good_controlled value that the exporter originally gave
    html = render_to_string("case/product-on-case.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert "Yes" in soup.find(id="is-licensable-value").text


def test_good_on_application_detail_verified_product(data_good_on_application, data_standard_case):
    # given the product has been reviewed
    good_on_application = {**data_good_on_application}
    good_on_application["is_good_controlled"] = {"key": "False", "value": "No"}

    # and the exporter told us the good is controlled
    good_on_application["good"]["is_good_controlled"] = {"key": "True", "value": "Yes"}

    context = {
        "good_on_application": good_on_application,
        "good_on_application_documents": [],
        "case": Case(data_standard_case["case"]),
        "other_cases": [],
        "data": {},
        "organisation_documents": {},
        "queue": {"id": "00000000-0000-0000-0000-000000000001"},
    }

    # then we show the is_good_controlled value that the reviewer gave
    html = render_to_string("case/product-on-case.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert "No" in soup.find(id="is-licensable-value").text


@pytest.mark.parametrize(
    "quantity, unit, expected_value",
    [
        (256, {"key": "NAR", "value": "Items"}, "256 items"),
        (1, {"key": "NAR", "value": "Items"}, "1 item"),
        (123.45, {"key": "GRM", "value": "Grams"}, "123.45 grams"),
        (128.64, {"key": "KGM", "value": "Kilograms"}, "128.64 kilograms"),
        (1150.32, {"key": "MTK", "value": "Square metres"}, "1150.32 square metres"),
        (100.00, {"key": "MTR", "value": "Metres"}, "100.0 metres"),
        (2500.25, {"key": "LTR", "value": "Litres"}, "2500.25 litres"),
        (123.45, {"key": "MTQ", "value": "Cubic metres"}, "123.45 cubic metres"),
    ],
)
def test_good_on_application_display_quantity(data_good_on_application, quantity, unit, expected_value):
    good_on_application = {**data_good_on_application}
    good_on_application["quantity"] = quantity
    good_on_application["unit"] = unit

    context = {
        "queue": {"id": "00000000-0000-0000-0000-000000000001"},
        "case": {"id": "8fb76bed-fd45-4293-95b8-eda9468aa254", "goods": []},
        "goods": [good_on_application],
    }

    html = render_to_string("case/slices/goods.html", context)
    soup = BeautifulSoup(html, "html.parser")
    actual_quantity = soup.find(id="quantity-value").text
    assert expected_value == actual_quantity


@pytest.mark.parametrize(
    ("agreed_to_foi", "agreed_to_foi_display_value", "foi_reason"),
    [
        (True, "No", "internal details"),
        (False, "Yes", ""),
    ],
)
def test_foi_details_on_summary_page(data_standard_case, agreed_to_foi, agreed_to_foi_display_value, foi_reason):
    case = data_standard_case["case"]
    case["data"]["agreed_to_foi"] = agreed_to_foi
    case["data"]["foi_reason"] = foi_reason
    context = {"case": case}

    html = render_to_string("case/slices/freedom-of-information.html", context)
    soup = BeautifulSoup(html, "html.parser")
    actual_foi_value = soup.find(id="agreed-to-foi-value").text
    actual_foi_reason_value = soup.find(id="foi-reason-value").text
    assert agreed_to_foi_display_value == actual_foi_value
    assert foi_reason == actual_foi_reason_value


@pytest.fixture
def licence_details(data_standard_case):
    return {
        "id": data_standard_case["case"]["licences"][0]["id"],
        "status": "issued",
        "case_status": "finalised",
        "reference_code": "12345AB",
    }


def test_actions_column_and_change_link_displays_on_licence_details(data_standard_case, mock_gov_user, licence_details):
    mock_gov_user["user"]["role"]["id"] = LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID
    data_standard_case["case"]["licences"] = [licence_details]
    case = data_standard_case["case"]
    request = HttpRequest()

    request.lite_user = mock_gov_user["user"]
    context = {
        "case": case,
        "queue": {"id": "00000000-0000-0000-0000-000000000001"},
        "request": request,
        "show_actions_column": True,
    }

    html = render_to_string("case/tabs/licences.html", context)
    soup = BeautifulSoup(html, "html.parser")

    show_actions_column = bool(soup.find(id="actions_column_header"))
    show_licence_status_change_link = bool(soup.find(id="actions_column_header"))

    assert show_actions_column and show_licence_status_change_link
