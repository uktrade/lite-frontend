from caseworker.core.context_processors import lite_menu
from caseworker.core.constants import Role

import pytest


@pytest.mark.parametrize(
    "valid_role",
    Role.tau_roles.value,
)
@pytest.mark.parametrize(
    "invalid_role, status",
    [
        ("TAU User", False),
        ("HMRC Manager", False),
        ("HMRC User", False),
    ],
)
def test_lite_menu_user_can_access_denial_records(mocker, invalid_role, status, valid_role, authorized_client):
    mocker.patch("caseworker.core.context_processors.get_user_permissions")
    mocker.patch("caseworker.core.context_processors.get_user_role_name", side_effect=[valid_role, invalid_role])
    mocker.patch("caseworker.core.context_processors.get_queue")

    request = mocker.MagicMock()
    request.session = {"lite_api_user_id": "user_id", "default_queue": "00000000-0000-0000-0000-000000000001"}

    valid_status_result = lite_menu(request)
    valid_menu_options = [item["title"] for item in valid_status_result["LITE_MENU"]]
    assert "Denial records" in valid_menu_options

    invalid_status_result = lite_menu(request)
    invalid_menu_options = [item["title"] for item in invalid_status_result["LITE_MENU"]]
    assert ("Denial records" in invalid_menu_options) == status
