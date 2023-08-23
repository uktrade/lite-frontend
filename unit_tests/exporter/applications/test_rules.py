import pytest
import rules

from datetime import datetime, timedelta

from django.utils import timezone

from exporter.core.objects import Application


@pytest.mark.parametrize(
    "flag_value, licence, days_until_deadline, expected",
    (
        (False, None, None, False),
        (True, {"reference_code": "GBSIEL/2023/0000001/P"}, None, False),
        (True, None, -1, False),  # deadline is 1 day before today
        (True, None, 0, True),  # today is the deadline
        (True, None, 5, True),  # deadline is 5 days from today
    ),
)
def test_can_user_appeal_case_based_on_feature_flag(
    settings, rf, data_standard_case, flag_value, licence, days_until_deadline, expected
):
    settings.FEATURE_FLAG_APPEALS = flag_value
    data_standard_case["licence"] = licence
    data_standard_case["appeal_deadline"] = ""

    if days_until_deadline is not None:
        appeal_deadline = timezone.localtime() + timedelta(days_until_deadline)
        data_standard_case["appeal_deadline"] = appeal_deadline.isoformat()

    application = Application(data_standard_case)

    request = rf.get("/")
    assert rules.test_rule("can_user_appeal_case", request, application) is expected
