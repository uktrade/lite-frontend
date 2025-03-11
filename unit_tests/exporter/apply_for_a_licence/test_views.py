import pytest

from django.urls import (
    reverse,
    reverse_lazy,
)


@pytest.fixture()
def licence_type_url():
    return reverse("apply_for_a_licence:start")


@pytest.mark.parametrize(
    "licence_type, update_settings, expected_url",
    (
        ("export_licence", {}, reverse_lazy("apply_for_a_licence:export_licence_questions")),
        ("f680", {"FEATURE_FLAG_ALLOW_F680": True}, reverse_lazy("apply_for_a_licence:f680_questions")),
        (
            "f680",
            {"FEATURE_FLAG_F680_ALLOWED_ORGANISATIONS": "f65fbf49-c14b-482b-833f-fe39bb26a51d"},  # /PS-IGNORE
            reverse_lazy("apply_for_a_licence:f680_questions"),
        ),
    ),
)
def test_licence_type_redirects(
    authorized_client,
    licence_type_url,
    licence_type,
    settings,
    update_settings,
    expected_url,
):
    for key, value in update_settings.items():
        setattr(settings, key, value)

    response = authorized_client.post(
        licence_type_url,
        data={"licence_type": licence_type},
    )

    assert response.status_code == 302
    assert response.url == expected_url
