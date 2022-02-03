from unittest.mock import patch

from bs4 import BeautifulSoup
from django.urls import reverse

from caseworker.advice.services import LICENSING_UNIT_TEAM


@patch("caseworker.advice.views.get_gov_user")
def test_no_advice_summary_for_lu(
    mock_get_gov_user, mock_queue, mock_case, mock_denial_reasons, authorized_client, data_queue, data_standard_case
):
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": "21313212-23123-3123-323wq2", "alias": LICENSING_UNIT_TEAM}}},
        None,
    )
    url = reverse(
        f"cases:consolidate_advice_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Other recommendations for this case" not in soup.find("h2")
