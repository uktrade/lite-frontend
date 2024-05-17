from caseworker.core.context_processors import lite_menu
from caseworker.core.constants import Role

import pytest

# Add valid roles to list of tuples to define the role and whether the user can access the denial records

roles_and_status = []
for role in Role.tau_roles.value:
    role = (role, True)
    roles_and_status.append(role)

# Add invalid roles

invalid_roles = [
    ("TAU User", False),
    ("HMRC User", False),
    ("HMRC Manager", False),
]

roles_and_status.extend(invalid_roles)


@pytest.mark.parametrize("role, status", roles_and_status)
def test_lite_menu_user_can_access_denial_records(mocker, role, status, authorized_client):
    mocker.patch("caseworker.core.context_processors.get_user_permissions")
    mocker.patch("caseworker.core.context_processors.get_user_role_name", return_value=role)
    mocker.patch("caseworker.core.context_processors.get_queue")

    request = mocker.MagicMock()
    request.session = {"lite_api_user_id": "user_id", "default_queue": "00000000-0000-0000-0000-000000000001"}

    result = lite_menu(request)
    menu_titles = [item["title"] for item in result["LITE_MENU"]]
    menu_urls = [item["url"] for item in result["LITE_MENU"]]

    assert ("Denial records" in menu_titles) == status
    assert ("/denials/upload/" in menu_urls) == status
