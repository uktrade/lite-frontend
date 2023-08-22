import pytest
import rules


@pytest.mark.parametrize(
    "flag_value, expected",
    (
        (True, True),
        (False, False),
    ),
)
def test_can_user_appeal_case_based_on_feature_flag(settings, flag_value, expected, rf):
    settings.FEATURE_FLAG_APPEALS = flag_value
    request = rf.get("/")
    assert rules.test_rule("can_user_appeal_case", request) is expected
