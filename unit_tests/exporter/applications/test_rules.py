import pytest
import rules

from datetime import timedelta

from django.utils import timezone

from exporter.applications import rules as appeal_rules
from exporter.core.objects import Application


def test_can_user_appeal_case_rule_predicates(settings, rf, data_standard_case):
    settings.FEATURE_FLAG_APPEALS = True
    data_standard_case["case"]["data"]["appeal_deadline"] = ""

    request = rf.get("/")
    assert not appeal_rules.is_application_finalised(request, None)
    assert not appeal_rules.is_application_refused(request, None)
    assert not appeal_rules.appeal_within_deadline(request, None)

    application = Application(data_standard_case["case"]["data"])
    assert not appeal_rules.appeal_within_deadline(request, application)


@pytest.mark.parametrize(
    "flag_value, status, licence, days_until_deadline, expected",
    (
        (False, "submitted", None, None, False),
        (True, "under_final_review", {"reference_code": "GBSIEL/2023/0000001/P"}, None, False),
        (True, "finalised", {"reference_code": "GBSIEL/2023/0000001/P"}, None, False),
        (True, "finalised", None, -1, False),  # we are past deadline by 1 day
        (True, "finalised", None, 0, True),  # today is the deadline
        (True, "finalised", None, 5, True),  # deadline is 5 days from today
    ),
)
def test_can_user_appeal_case_based_on_feature_flag(
    settings, rf, data_standard_case, flag_value, status, licence, days_until_deadline, expected
):
    settings.FEATURE_FLAG_APPEALS = flag_value
    data_standard_case["case"]["data"]["status"] = {"key": status, "value": status.title()}
    data_standard_case["case"]["data"]["licence"] = licence
    data_standard_case["case"]["data"]["appeal_deadline"] = ""

    if days_until_deadline is not None:
        appeal_deadline = timezone.localtime() + timedelta(days_until_deadline)
        data_standard_case["case"]["data"]["appeal_deadline"] = appeal_deadline.isoformat()

    application = Application(data_standard_case["case"]["data"])

    request = rf.get("/")
    assert rules.test_rule("can_user_appeal_case", request, application) is expected
