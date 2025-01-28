import pytest

from exporter.apply_for_a_licence.forms import triage_questions
from exporter.core.constants import CaseTypes


@pytest.mark.parametrize(
    "siel_allowed, f680_allowed, expect_enabled, expect_disabled",
    (
        (True, True, ["export_licence", "f680", "transhipment", "trade_control_licence"], []),
        (True, False, ["export_licence", "transhipment", "trade_control_licence"], ["f680"]),
        (False, True, ["export_licence", "f680"], ["transhipment", "trade_control_licence"]),
        (False, False, ["export_licence"], ["f680", "transhipment", "trade_control_licence"]),
    ),
)
def test_opening_question_feature_flags(settings, siel_allowed, f680_allowed, expect_enabled, expect_disabled):
    # given the flag is set or unset
    settings.FEATURE_FLAG_ALLOW_SIEL = siel_allowed
    settings.FEATURE_FLAG_ALLOW_F680 = f680_allowed

    # when the form is created
    form = triage_questions.opening_question()

    # then the disabled options reflect the feature flag
    assert [item.key for item in form.questions[0].options if not item.disabled] == expect_enabled
    assert [item.key for item in form.questions[0].options if item.disabled] == expect_disabled


@pytest.mark.parametrize(
    "value, expect_enabled, expect_disabled",
    (
        (True, [CaseTypes.SIEL], [CaseTypes.OGEL, CaseTypes.OIEL]),
        (False, [CaseTypes.SIEL, CaseTypes.OGEL, CaseTypes.OIEL], []),
    ),
)
def test_export_type_form_feature_flag(settings, value, expect_enabled, expect_disabled):
    # given the flag is set or unset
    settings.FEATURE_FLAG_ALLOW_SIEL = value

    # when the form is created
    form = triage_questions.export_type_form()

    # then the disabled options reflect the feature flag
    assert [item.key for item in form.questions[0].options if item.disabled] == expect_disabled
    assert [item.key for item in form.questions[0].options if not item.disabled] == expect_enabled
