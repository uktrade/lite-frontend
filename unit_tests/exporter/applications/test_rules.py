import pytest
import rules

from datetime import timedelta

from django.utils import timezone

from exporter.applications import rules as appeal_rules
from exporter.core.objects import Application


def test_can_user_appeal_case_rule_predicates(settings, rf, data_standard_case):
    data_standard_case["case"]["data"]["appeal_deadline"] = ""

    request = rf.get("/")
    assert not appeal_rules.is_application_finalised(request, None)
    assert not appeal_rules.is_application_refused(request, None)
    assert not appeal_rules.appeal_within_deadline(request, None)
    assert not appeal_rules.is_application_appealed(request, None)

    application = Application(data_standard_case["case"]["data"])
    assert not appeal_rules.appeal_within_deadline(request, application)


@pytest.mark.parametrize(
    "status, licence, days_until_deadline, appeal_details, expected",
    (
        ("under_final_review", {"reference_code": "GBSIEL/2023/0000001/P"}, None, None, False),
        ("finalised", {"reference_code": "GBSIEL/2023/0000001/P"}, None, None, False),
        ("finalised", None, -1, None, False),  # we are past deadline by 1 day
        ("finalised", None, 0, None, True),  # today is the deadline
        ("finalised", None, 5, None, True),  # deadline is 5 days from today
        ("finalised", None, 5, {"grounds_for_appeal": "test appeal"}, False),
    ),
)
def test_can_user_appeal_case_based_on_feature_flag(
    rf, data_standard_case, status, licence, days_until_deadline, appeal_details, expected
):
    data_standard_case["case"]["data"]["status"] = {"key": status, "value": status.title()}
    data_standard_case["case"]["data"]["licence"] = licence
    data_standard_case["case"]["data"]["appeal_deadline"] = ""
    data_standard_case["case"]["data"]["appeal"] = appeal_details

    if days_until_deadline is not None:
        appeal_deadline = timezone.localtime() + timedelta(days_until_deadline)
        data_standard_case["case"]["data"]["appeal_deadline"] = appeal_deadline.isoformat()

    application = Application(data_standard_case["case"]["data"])

    request = rf.get("/")
    assert rules.test_rule("can_user_appeal_case", request, application) is expected


@pytest.mark.parametrize(
    "appeal, expected",
    (
        (None, False),
        ({"grounds_for_appeal": "test appeal"}, True),
    ),
)
def test_view_appeal_details(settings, rf, data_standard_case, appeal, expected):
    data_standard_case["case"]["data"]["status"] = {"key": "finalised", "value": "Finalised"}
    data_standard_case["case"]["data"]["licence"] = None
    data_standard_case["case"]["data"]["appeal_deadline"] = timezone.localtime().isoformat()
    data_standard_case["case"]["data"]["appeal"] = appeal

    application = Application(data_standard_case["case"]["data"])

    request = rf.get("/")
    assert rules.test_rule("can_view_appeal_details", request, application) is expected
