import pytest

from django.urls import reverse


@pytest.fixture()
def apply_for_a_licence_url():
    return reverse("apply_for_a_licence:start")


def test_POST_apply_for_a_licence_redirects(
    authorized_client,
    apply_for_a_licence_url,
):
    response = authorized_client.post(apply_for_a_licence_url, data={"licence_type": "export_licence"})
    assert response.status_code == 302
    assert response.url == reverse("apply_for_a_licence:export_licence_questions")
