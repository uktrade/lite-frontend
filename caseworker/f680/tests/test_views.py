import pytest

from itertools import chain
from requests.exceptions import HTTPError

from bs4 import BeautifulSoup
from django.urls import reverse

from http import HTTPStatus

from core import client
from caseworker.f680 import rules as recommendation_rules


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    mock_approval_reason,
    mock_denial_reasons,
    mock_proviso,
    mock_footnote_details,
    settings,
):
    settings.FEATURE_FLAG_ALLOW_F680 = True
    return


@pytest.fixture
def mock_f680_case_with_submitted_by(f680_case_id, requests_mock, data_submitted_f680_case):
    data_submitted_f680_case["case"]["data"]["submitted_by"] = {"first_name": "foo", "last_name": "bar"}
    url = client._build_absolute_uri(f"/cases/{f680_case_id}/")
    return requests_mock.get(url=url, json=data_submitted_f680_case)


@pytest.fixture
def mock_f680_case_activity_filters(f680_case_id, requests_mock, standard_case_activity_filters):
    url = client._build_absolute_uri(f"/cases/{f680_case_id}/activity/filters/")
    return requests_mock.get(url=url, json=standard_case_activity_filters)


@pytest.fixture
def mock_f680_case_activity(f680_case_id, requests_mock, standard_case_activity):
    url = client._build_absolute_uri(f"/cases/{f680_case_id}/activity/")
    return requests_mock.get(url=url, json=standard_case_activity)


@pytest.fixture
def mock_put_assigned_queues(f680_case_id, requests_mock, data_queue):
    queue_pk = data_queue["id"]
    return requests_mock.put(
        client._build_absolute_uri(f"/cases/{f680_case_id}/assigned-queues/"), json={"queues": [queue_pk]}
    )


@pytest.fixture
def mock_case_sub_statuses(requests_mock, data_submitted_f680_case):
    url = f"/applications/{data_submitted_f680_case['case']['id']}/sub-statuses/"
    return requests_mock.get(url, json=[])


@pytest.fixture
def f680_feature_flag_disabled(settings):
    settings.FEATURE_FLAG_ALLOW_F680 = False


class TestCaseDetailView:

    def test_GET_success(
        self, authorized_client, data_queue, mock_f680_case, f680_case_id, f680_reference_code, data_submitted_f680_case
    ):
        url = reverse("cases:f680:details", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        response = authorized_client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert dict(response.context["case"]) == data_submitted_f680_case["case"]
        soup = BeautifulSoup(response.content, "html.parser")
        assert f680_reference_code in soup.find("h1").text
        assert "General application details" in soup.find("h2").text
        table_elems = soup.find_all("table", {"class": "application-section-general_application_details"})
        assert len(table_elems) == 1
        table_text = table_elems[0].text
        assert (
            "Do you have exceptional circumstances that mean you need F680 approval in less than 30 days?" in table_text
        )
        assert "some name" in table_text

    @pytest.mark.parametrize(
        "case_status, expected",
        (
            chain(
                ((status, False) for status in recommendation_rules.INFORMATIONAL_STATUSES),
                ((status, True) for status in recommendation_rules.RECOMMENDATION_STATUSES),
                ((status, True) for status in recommendation_rules.OUTCOME_STATUSES),
            )
        ),
    )
    def test_GET_case_recommendation_tab_status(
        self,
        authorized_client,
        data_queue,
        mock_f680_case,
        mock_case_sub_statuses,
        mock_get_case_no_recommendations,
        f680_case_id,
        data_submitted_f680_case,
        queue_f680_cases_to_review,
        current_user,
        case_status,
        expected,
    ):
        data_submitted_f680_case["case"]["data"]["status"]["key"] = case_status
        data_submitted_f680_case["case"]["assigned_users"] = {queue_f680_cases_to_review["name"]: [current_user]}
        url = reverse("cases:f680:details", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        response = authorized_client.get(url)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, "html.parser")
        recommendations_tab = soup.find(id="recommendations")
        assert bool(recommendations_tab) is expected

    def test_GET_success_transformed_submitted_by(
        self,
        authorized_client,
        data_queue,
        mock_f680_case_with_submitted_by,
        f680_case_id,
        f680_reference_code,
        data_submitted_f680_case,
    ):
        url = reverse("cases:f680:details", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        response = authorized_client.get(url)
        assert response.status_code == HTTPStatus.OK

    def test_GET_not_logged_in(
        self, client, data_queue, mock_f680_case, f680_case_id, f680_reference_code, data_submitted_f680_case
    ):
        url = reverse("cases:f680:details", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        expected_redirect_location = reverse("auth:login")
        response = client.get(url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(expected_redirect_location)

    def test_GET_no_case_404(self, authorized_client, data_queue, missing_case_id, mock_missing_case):
        url = reverse("cases:f680:details", kwargs={"queue_pk": data_queue["id"], "pk": missing_case_id})
        with pytest.raises(HTTPError, match="404"):
            authorized_client.get(url)


class TestCaseSummaryView:

    def test_GET_success(
        self, authorized_client, data_queue, mock_f680_case, f680_case_id, f680_reference_code, data_submitted_f680_case
    ):
        url = reverse("cases:f680:summary", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        response = authorized_client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert dict(response.context["case"]) == data_submitted_f680_case["case"]
        soup = BeautifulSoup(response.content, "html.parser")
        assert f680_reference_code in soup.find("h1").text

        assert "Product" in soup.find("h2").text
        product_table_elems = soup.find_all("table", {"class": "f680-product-table"})
        assert len(product_table_elems) == 1
        product_table_text = product_table_elems[0].text
        assert "product description" in product_table_text

        security_release_table_elems = soup.find_all("table", {"class": "f680-security-release-table"})
        assert len(security_release_table_elems) == 1
        security_release_table_text = security_release_table_elems[0].text
        assert "australia name" in security_release_table_text
        assert "france name" in security_release_table_text
        assert "uae name" in security_release_table_text

    def test_GET_not_logged_in(
        self, client, data_queue, mock_f680_case, f680_case_id, f680_reference_code, data_submitted_f680_case
    ):
        url = reverse("cases:f680:summary", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        expected_redirect_location = reverse("auth:login")
        response = client.get(url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(expected_redirect_location)

    def test_GET_no_case_404(self, authorized_client, data_queue, missing_case_id, mock_missing_case):
        url = reverse("cases:f680:summary", kwargs={"queue_pk": data_queue["id"], "pk": missing_case_id})
        with pytest.raises(HTTPError, match="404"):
            authorized_client.get(url)


class TestMoveCaseForwardView:

    def test_POST_not_assigned_permisison_denied(self, authorized_client, data_queue, mock_f680_case, f680_case_id):
        url = reverse("cases:f680:move_case_forward", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        response = authorized_client.post(url)
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_POST_no_f680_feature_flag_permission_denied(
        self, authorized_client, data_queue, mock_f680_case, f680_case_id, f680_feature_flag_disabled
    ):
        url = reverse("cases:f680:move_case_forward", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        response = authorized_client.post(url)
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_POST_success(
        self, authorized_client, data_queue, mock_f680_case_with_assigned_user, f680_case_id, mock_put_assigned_queues
    ):
        url = reverse("cases:f680:move_case_forward", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        response = authorized_client.post(url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("queues:cases", kwargs={"queue_pk": data_queue["id"]})


@pytest.fixture
def mock_post_case_notes(requests_mock, f680_case_id):
    return requests_mock.post(
        f"/cases/{f680_case_id}/case-notes/",
        json={},
        status_code=HTTPStatus.CREATED,
    )


class TestNotesAndTimelineView:

    @pytest.fixture(autouse=True)
    def _setup(self, setup, data_queue, f680_case_id, mock_gov_users, requests_mock):
        self.f680_case_id = f680_case_id
        self.queue = data_queue
        self.url = reverse(
            "cases:f680:notes_and_timeline", kwargs={"queue_pk": self.queue["id"], "pk": self.f680_case_id}
        )
        self.gov_user_id = "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"
        requests_mock.get(
            client._build_absolute_uri(f"/gov-users/"),
            json={
                "results": mock_gov_users,
            },
        )

    def test_GET_not_logged_in(
        self,
        client,
        mock_f680_case,
        mock_f680_case_activity,
        mock_f680_case_activity_filters,
    ):
        expected_redirect_location = reverse("auth:login")
        response = client.get(self.url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(expected_redirect_location)

    def test_GET_success(
        self,
        authorized_client,
        mock_f680_case,
        mock_f680_case_activity,
        mock_f680_case_activity_filters,
    ):

        response = authorized_client.get(self.url)
        assert response.status_code == HTTPStatus.OK

    def test_POST_success(
        self,
        authorized_client,
        mock_f680_case,
        mock_f680_case_activity,
        mock_f680_case_activity_filters,
        mock_post_case_notes,
    ):
        response = authorized_client.post(
            self.url,
            data={
                "text": "Note text",
                "mentions": [self.gov_user_id],
            },
        )
        assert response.status_code == HTTPStatus.FOUND
        assert (
            response.url == f"/queues/00000000-0000-0000-0000-000000000001/cases/{self.f680_case_id}/f680/activities/"
        )
        assert mock_post_case_notes.called
        assert mock_post_case_notes.last_request.json() == {
            "is_urgent": False,
            "mentions": [{"user": self.gov_user_id}],
            "text": "Note text",
        }
