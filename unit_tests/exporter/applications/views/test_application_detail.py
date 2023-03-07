import pytest

from bs4 import BeautifulSoup
from django.urls import reverse


@pytest.mark.parametrize(
    "is_read_only",
    [True, False],
)
def test_edit_button(authorized_client, data_standard_case, mock_application_get, mock_status_properties, is_read_only):
    pk = data_standard_case["case"]["id"]
    mock_status_properties["is_read_only"] = is_read_only

    application_url = reverse("applications:application", kwargs={"pk": pk})
    response = authorized_client.get(application_url)
    soup = BeautifulSoup(response.content, "html.parser")
    if is_read_only:
        assert not soup.find(id="button-edit-application")
    else:
        assert soup.find(id="button-edit-application")
