import pytest

from exporter.apply_for_a_licence.forms import triage_questions
from exporter.core.constants import CaseTypes
from unit_tests.helpers import reload_urlconf


@pytest.mark.parametrize(
    "siel_only_allowed, f680_allowed, expect_enabled, expect_disabled",
    (
        (True, True, ["export_licence", "f680"], ["transhipment", "trade_control_licence"]),
        (True, False, ["export_licence"], ["f680", "transhipment", "trade_control_licence"]),
        (False, True, ["export_licence", "f680", "transhipment", "trade_control_licence"], []),
        (False, False, ["export_licence", "transhipment", "trade_control_licence"], ["f680"]),
    ),
)
def test_opening_question_feature_flags(settings, siel_only_allowed, f680_allowed, expect_enabled, expect_disabled):
    # given the flag is set or unset
    settings.FEATURE_FLAG_ONLY_ALLOW_SIEL = siel_only_allowed
    settings.FEATURE_FLAG_ALLOW_F680 = f680_allowed
    reload_urlconf(["exporter.apply_for_a_licence.urls", settings.ROOT_URLCONF])

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
    settings.FEATURE_FLAG_ONLY_ALLOW_SIEL = value
    reload_urlconf(["exporter.apply_for_a_licence.urls", settings.ROOT_URLCONF])

    # when the form is created
    form = triage_questions.export_type_form()

    # then the disabled options reflect the feature flag
    assert [item.key for item in form.questions[0].options if item.disabled] == expect_disabled
    assert [item.key for item in form.questions[0].options if not item.disabled] == expect_enabled
