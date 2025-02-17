import pytest
import rules


@pytest.mark.parametrize(
    "user_organisation, organisation_list, expected",
    (
        ("12345", ["12345", "98765", "56757"], True),
        ("99999", ["12345", "98765", "56757"], False),
        ("", ["12345", "98765", "56757"], False),
        ("99999", [], False),
        (None, [], False),
    ),
)
def test_exporter_in_organisation_list(rf, client, user_organisation, organisation_list, expected):
    request = rf.get("/")
    request.session = client.session
    session = request.session
    session["organisation"] = user_organisation
    session.save()

    assert rules.test_rule("exporter_in_organisation_list", request, organisation_list) is expected
