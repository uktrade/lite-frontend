from django.urls import reverse_lazy
from caseworker.core.context_processors import lite_menu

import pytest


@pytest.mark.parametrize(
    "valid_user_role",
    [
        ("TAU Manager"),
        ("TAU Officer"),
        ("TAU Senior Manager"),
        ("Super User"),
    ],
)
def test_lite_menu_denial_records_link_for_valid_roles(valid_user_role, authorized_client, mocker):
    mocker.patch("caseworker.core.context_processors.get_user_permissions")
    mocker.patch("caseworker.core.context_processors.get_user_role_name", return_value=valid_user_role)
    mocker.patch("caseworker.core.context_processors.get_queue")

    request = mocker.MagicMock()
    request.session = {"lite_api_user_id": "user_id", "default_queue": "00000000-0000-0000-0000-000000000001"}

    result = lite_menu(request)

    assert result["LITE_MENU"][-1]["title"] == "Denial records"
    assert result["LITE_MENU"][-1]["url"] == reverse_lazy("external_data:denials-upload")
    assert result["LITE_MENU"][-1]["icon"] == "menu/cases"


@pytest.mark.parametrize(
    "invalid_user_role",
    [
        ("TAU User"),
        ("HMRC Manager"),
        ("HMRC User"),
    ],
)
def test_lite_menu_denial_records_link_for_invalid_roles(invalid_user_role, authorized_client, mocker):
    mocker.patch("caseworker.core.context_processors.get_user_permissions")
    mocker.patch("caseworker.core.context_processors.get_user_role_name", return_value=invalid_user_role)
    mocker.patch("caseworker.core.context_processors.get_queue")

    request = mocker.MagicMock()
    request.session = {"lite_api_user_id": "user_id", "default_queue": "00000000-0000-0000-0000-000000000001"}

    result = lite_menu(request)

    assert "Denial records" not in [x["title"] for x in result["LITE_MENU"]]
    assert reverse_lazy("external_data:denials-upload") not in [x["url"] for x in result["LITE_MENU"]]
