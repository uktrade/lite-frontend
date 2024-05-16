from django.urls import reverse_lazy
from caseworker.core.context_processors import lite_menu
from caseworker.core.constants import Role

import pytest


@pytest.mark.parametrize(
    "valid_user_role",
    Role.tau_roles.value,
)
@pytest.mark.parametrize(
    "invalid_user_role",
    [
        ("TAU User"),
        ("HMRC Manager"),
        ("HMRC User"),
    ],
)
def test_lite_menu_denial_records_link_for_valid_and_invalid_roles(
    valid_user_role, invalid_user_role, authorized_client, mocker
):
    mocker.patch("caseworker.core.context_processors.get_user_permissions")
    mocker.patch(
        "caseworker.core.context_processors.get_user_role_name", side_effect=[valid_user_role, invalid_user_role]
    )
    mocker.patch("caseworker.core.context_processors.get_queue")

    request = mocker.MagicMock()
    request.session = {"lite_api_user_id": "user_id", "default_queue": "00000000-0000-0000-0000-000000000001"}

    result_for_side_effect_1 = lite_menu(request)

    for item in result_for_side_effect_1["LITE_MENU"]:
        if item["title"] == "Denial records":
            assert item["url"] == reverse_lazy("external_data:denials-upload")

    result_for_side_effect_2 = lite_menu(request)

    assert "Denial records" not in [x["title"] for x in result_for_side_effect_2["LITE_MENU"]]
