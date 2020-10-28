import pytest

from exporter.apply_for_a_licence.forms import triage_questions
from exporter.core.constants import CaseTypes


@pytest.mark.parametrize(
    "value,expect_enabled,expect_disabled",
    (
        (True, ["export_licence"], ["transhipment", "trade_control_licence", "mod"]),
        (False, ["export_licence", "transhipment", "trade_control_licence", "mod"], []),
    ),
)
def test_opening_question_feature_flag(settings, value, expect_enabled, expect_disabled):
    # given the flag is set or unset
    settings.FEATURE_FLAG_ONLY_ALLOW_SIEL = value

    # when the form is created
    form = triage_questions.opening_question()

    # then the disabled options reflect the feature flag
    assert [item.key for item in form.questions[0].options if item.disabled] == expect_disabled
    assert [item.key for item in form.questions[0].options if not item.disabled] == expect_enabled


@pytest.mark.parametrize(
    "value,expect_enabled,expect_disabled",
    (
        (True, [CaseTypes.SIEL], [CaseTypes.OGEL, CaseTypes.OIEL]),
        (False, [CaseTypes.SIEL, CaseTypes.OGEL, CaseTypes.OIEL], []),
    ),
)
def test_export_type_form_feature_flag(settings, value, expect_enabled, expect_disabled):
    # given the flag is set or unset
    settings.FEATURE_FLAG_ONLY_ALLOW_SIEL = value

    # when the form is created
    form = triage_questions.export_type_form()

    # then the disabled options reflect the feature flag
    assert [item.key for item in form.questions[0].options if item.disabled] == expect_disabled
    assert [item.key for item in form.questions[0].options if not item.disabled] == expect_enabled
