import copy

from unittest.mock import MagicMock
from bs4 import BeautifulSoup
from django.template.loader import render_to_string

from caseworker.advice.forms import BEISTriggerListAssessmentForm
from caseworker.cases.objects import Case

QUEUE_ID = "00000000-0000-0000-0000-000000000001"


def basic_context(data):
    case = copy.deepcopy(data)
    goods = {good["id"]: good for good in case["case"]["data"]["goods"]}

    button_mock = MagicMock()
    button_mock.make_recommendation = True
    return {
        "queue": {"id": QUEUE_ID},
        "queue_pk": QUEUE_ID,
        "case": Case(case["case"]),
        "form": BEISTriggerListAssessmentForm(MagicMock(), QUEUE_ID, goods, QUEUE_ID, False, {}),
        "can_advise": True,
        "buttons": button_mock,
    }


def test_view_advice_does_not_show_assessed_product_table_if_no_assessments_made(
    data_standard_case_with_potential_trigger_list_product_no_assessments,
):
    context = basic_context(data_standard_case_with_potential_trigger_list_product_no_assessments)

    context["assessed_trigger_list_goods"] = []

    html = render_to_string("advice/view-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert soup.find(id="assessed-products") is None


def test_view_advice_does_show_assessed_product_table_if_all_assessments_made(
    data_standard_case_with_potential_trigger_list_product,
):
    context = basic_context(data_standard_case_with_potential_trigger_list_product)

    goods = data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"]
    context["assessed_trigger_list_goods"] = [good for good in goods if "nsg_list_type" in good]

    html = render_to_string("advice/view-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="assessed-products")
    assert table is not None
    rows = table.tbody.find_all("tr")
    assert len(rows) == len(context["assessed_trigger_list_goods"])
