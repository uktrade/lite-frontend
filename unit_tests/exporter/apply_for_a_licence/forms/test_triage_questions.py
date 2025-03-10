import pytest

from exporter.apply_for_a_licence.forms.triage_questions import LicenceTypeForm


@pytest.mark.parametrize(
    "f680_allowed, expect_enabled, expect_disabled",
    (
        (True, ["export_licence", "f680"], ["transhipment", "trade_control_licence"]),
        (False, ["export_licence"], ["f680", "transhipment", "trade_control_licence"]),
    ),
)
def test_licence_type_form_feature_flags_disabled_values(
    render_form,
    rf,
    client,
    beautiful_soup,
    settings,
    f680_allowed,
    expect_enabled,
    expect_disabled,
):
    request = rf.get("/")
    request.session = client.session
    session = request.session
    session["organisation"] = "12345"
    session.save()

    settings.FEATURE_FLAG_ALLOW_F680 = f680_allowed

    # when the form is created
    form = LicenceTypeForm(request=request)

    form_html = render_form(form, request)
    soup = beautiful_soup(form_html)

    enabled_options = soup.select("input[name=licence_type]:not([disabled])")
    assert [option["value"] for option in enabled_options] == expect_enabled

    disabled_options = soup.select("input[name=licence_type][disabled]")
    assert [option["value"] for option in disabled_options] == expect_disabled


@pytest.mark.parametrize(
    "f680_allowed, expect_enabled, expect_disabled",
    (
        (True, ["export_licence", "f680"], ["transhipment", "trade_control_licence"]),
        (False, ["export_licence"], ["f680", "transhipment", "trade_control_licence"]),
    ),
)
def test_licence_type_form_feature_flags_errors(
    rf,
    client,
    settings,
    f680_allowed,
    expect_enabled,
    expect_disabled,
):
    request = rf.get("/")
    request.session = client.session
    session = request.session
    session["organisation"] = "12345"
    session.save()

    settings.FEATURE_FLAG_ALLOW_F680 = f680_allowed

    # when the form is created
    for value_to_submit in expect_enabled:
        form = LicenceTypeForm({"licence_type": value_to_submit}, request=request)
        assert form.is_valid()

    for value_to_submit in expect_disabled:
        form = LicenceTypeForm({"licence_type": value_to_submit}, request=request)
        assert not form.is_valid()
        assert form.errors["licence_type"] == [
            f"Select a valid choice. {value_to_submit} is not one of the available choices."
        ]


@pytest.mark.parametrize(
    "f680_allowed, f680_orgs_allowed, user_org, expect_enabled",
    (
        (True, [], "1234", ["export_licence", "f680"]),
        (False, [], "1234", ["export_licence"]),
        (False, ["1234"], "1234", ["export_licence", "f680"]),
        (False, ["1234"], "12345", ["export_licence"]),
    ),
)
def test_licence_type_f680_feature_flags_disabled_values(
    rf,
    client,
    settings,
    render_form,
    beautiful_soup,
    f680_allowed,
    f680_orgs_allowed,
    user_org,
    expect_enabled,
):
    request = rf.get("/")
    request.session = client.session
    session = request.session
    session["organisation"] = user_org
    session.save()

    # given the flag is set
    settings.FEATURE_FLAG_ALLOW_F680 = f680_allowed
    settings.FEATURE_FLAG_F680_ALLOWED_ORGANISATIONS = f680_orgs_allowed

    # when the form is created
    form = LicenceTypeForm(request=request)

    form_html = render_form(form, request)
    soup = beautiful_soup(form_html)

    enabled_options = soup.select("input[name=licence_type]:not([disabled])")
    assert [option["value"] for option in enabled_options] == expect_enabled


@pytest.mark.parametrize(
    "f680_allowed, f680_orgs_allowed, user_org, expect_enabled",
    (
        (True, [], "1234", True),
        (False, [], "1234", False),
        (False, ["1234"], "1234", True),
        (False, ["1234"], "12345", False),
    ),
)
def test_licence_type_f680_feature_flags_disabled_values(
    rf,
    client,
    settings,
    f680_allowed,
    f680_orgs_allowed,
    user_org,
    expect_enabled,
):
    request = rf.get("/")
    request.session = client.session
    session = request.session
    session["organisation"] = user_org
    session.save()

    # given the flag is set
    settings.FEATURE_FLAG_ALLOW_F680 = f680_allowed
    settings.FEATURE_FLAG_F680_ALLOWED_ORGANISATIONS = f680_orgs_allowed

    # when the form is created
    form = LicenceTypeForm({"licence_type": "f680"}, request=request)
    assert form.is_valid() is expect_enabled
    if not expect_enabled:
        assert form.errors["licence_type"] == ["Select a valid choice. f680 is not one of the available choices."]
