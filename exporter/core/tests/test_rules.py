import pytest
import rules


@pytest.mark.parametrize(
    "user_organisation, allowed_organisations_feature, f680_enabled_feature_flag, expected",
    (
        ("12345", ["12345", "98765", "56757"], False, True),
        ("99999", ["12345", "98765", "56757"], False, False),
        ("", ["12345", "98765", "56757"], False, False),
        ("99999", [], False, False),
        (None, [], False, False),
        ("99999", [], True, True),
        ("99999", ["12345", "98765", "56757"], True, True),
    ),
)
def test_can_exporter_use_f680s(
    rf, client, user_organisation, allowed_organisations_feature, f680_enabled_feature_flag, expected, settings
):
    settings.FEATURE_FLAG_F680_ALLOWED_ORGANISATIONS = allowed_organisations_feature
    settings.FEATURE_FLAG_ALLOW_F680 = f680_enabled_feature_flag

    request = rf.get("/")
    request.session = client.session
    session = request.session
    session["organisation"] = user_organisation
    session.save()

    assert rules.test_rule("can_exporter_use_f680s", request) is expected
