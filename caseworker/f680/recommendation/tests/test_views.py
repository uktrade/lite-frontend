import pytest

from bs4 import BeautifulSoup
from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from caseworker.f680.recommendation.constants import RecommendationType
from caseworker.f680.recommendation.forms.forms import BaseRecommendationForm, EntityConditionsRecommendationForm
from core import client
from core.constants import CaseStatusEnum


@pytest.fixture(autouse=True)
def setup(
    data_queue,
    f680_case_id,
    mock_queue,
    mock_case,
    mock_approval_reason,
    mock_denial_reasons,
    mock_footnote_details,
):
    return


@pytest.fixture
def make_recommendation_url(data_queue, f680_case_id):
    return reverse("cases:f680:make_recommendation", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})


@pytest.fixture
def view_recommendation_url(data_queue, f680_case_id):
    return reverse("cases:f680:view_my_recommendation", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})


@pytest.fixture
def post_to_step(post_to_step_factory, make_recommendation_url):
    return post_to_step_factory(make_recommendation_url)


@pytest.fixture
def mock_current_gov_user(requests_mock, f680_case_id):
    return requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{f680_case_id}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )


@pytest.fixture
def recommendations(current_user, admin_team, data_submitted_f680_case):
    security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
    return [
        {
            "created_at": "2021-10-16T23:48:39.486679+01:00",
            "id": "429c5596-fe8b-4540-988b-c37805cd08de",  # /PS-IGNORE
            "type": {"key": "approve", "value": "Approve"},
            "conditions": "No concerns",
            "refusal_reasons": "",
            "security_grading": {"key": "official", "value": "Official"},
            "security_grading_other": "",
            "security_release_request": security_release_requests[0]["id"],
            "user": current_user,
            "team": admin_team,
        }
    ]


@pytest.fixture
def mock_get_case_recommendations(requests_mock, data_submitted_f680_case, recommendations):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/recommendation/"
    return requests_mock.get(url, json=recommendations, status_code=200)


@pytest.fixture
def mock_get_case_no_recommendations(requests_mock, data_submitted_f680_case, recommendations):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/recommendation/"
    return requests_mock.get(url, json=[], status_code=200)


class TestF680RecommendationView:

    def test_GET_recommendation_success(
        self,
        authorized_client,
        queue_f680_cases_to_review,
        current_user,
        mock_f680_case,
        mock_get_case_no_recommendations,
        f680_case_id,
        f680_reference_code,
        data_submitted_f680_case,
    ):
        url = reverse(
            "cases:f680:recommendation", kwargs={"queue_pk": queue_f680_cases_to_review["id"], "pk": f680_case_id}
        )
        data_submitted_f680_case["case"]["assigned_users"] = {
            queue_f680_cases_to_review["name"]: [{"id": current_user["id"]}]
        }
        data_submitted_f680_case["case"]["data"]["status"]["key"] = CaseStatusEnum.OGD_ADVICE
        response = authorized_client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "f680/case/recommendation/recommendation.html")

        assert dict(response.context["case"]) == data_submitted_f680_case["case"]
        soup = BeautifulSoup(response.content, "html.parser")
        assert f680_reference_code in soup.find("h1").text
        make_recommendation_button = soup.find(id="make-recommendation-button")
        assert make_recommendation_button
        assert (
            make_recommendation_button["href"]
            == f'/queues/{queue_f680_cases_to_review["id"]}/cases/{f680_case_id}/f680/recommendation/make-recommendation/'
        )

    def test_GET_recommendation_page_existing_recommendation(
        self,
        authorized_client,
        queue_f680_cases_to_review,
        current_user,
        mock_f680_case,
        mock_get_case_recommendations,
        f680_case_id,
        data_submitted_f680_case,
    ):
        url = reverse(
            "cases:f680:recommendation", kwargs={"queue_pk": queue_f680_cases_to_review["id"], "pk": f680_case_id}
        )
        data_submitted_f680_case["case"]["assigned_users"] = {
            queue_f680_cases_to_review["name"]: [{"id": current_user["id"]}]
        }
        response = authorized_client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "f680/case/recommendation/recommendation.html")
        assertTemplateUsed(response, "f680/case/recommendation/other-recommendations.html")


class TestF680MakeRecommendationView:

    def test_make_recommendation_post(
        self,
        authorized_client,
        data_submitted_f680_case,
        make_recommendation_url,
        mock_f680_case,
        mock_approval_reason,
        mock_proviso,
        mock_post_recommendation,
        post_to_step,
        view_recommendation_url,
    ):
        security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
        response = post_to_step(
            security_release_requests[0]["id"],
            {
                "recommendation": RecommendationType.APPROVE,
                "security_grading": "official",
                "conditions": ["no_release", "no_specifications"],
            },
        )
        assert response.status_code == 200
        form = response.context["form"]
        assert isinstance(form, EntityConditionsRecommendationForm)

        response = post_to_step(
            security_release_requests[1]["id"],
            {
                "recommendation": RecommendationType.APPROVE,
                "security_grading": "official",
                "conditions": ["no_specifications"],
            },
        )
        assert response.status_code == 200
        form = response.context["form"]
        assert isinstance(form, EntityConditionsRecommendationForm)

        response = post_to_step(
            security_release_requests[2]["id"],
            {
                "recommendation": RecommendationType.REFUSE,
                "security_grading": "official",
                "conditions": [],
            },
        )
        assert response.status_code == 302
        assert response.url == view_recommendation_url

    def test_make_recommendation_post_no_team_provisos(
        self,
        authorized_client,
        data_submitted_f680_case,
        make_recommendation_url,
        mock_f680_case,
        mock_approval_reason,
        mock_no_provisos,
        mock_post_recommendation,
        post_to_step,
        view_recommendation_url,
    ):
        security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
        response = post_to_step(
            security_release_requests[0]["id"],
            {
                "recommendation": RecommendationType.APPROVE,
                "security_grading": "official",
                "conditions": ["no_release", "no_specifications"],
            },
        )
        assert response.status_code == 200
        form = response.context["form"]
        assert isinstance(form, BaseRecommendationForm)

        response = post_to_step(
            security_release_requests[1]["id"],
            {
                "recommendation": RecommendationType.APPROVE,
                "security_grading": "official",
                "conditions": ["no_specifications"],
            },
        )
        assert response.status_code == 200
        form = response.context["form"]
        assert isinstance(form, BaseRecommendationForm)

        response = post_to_step(
            security_release_requests[2]["id"],
            {
                "recommendation": RecommendationType.REFUSE,
                "security_grading": "official",
                "conditions": [],
            },
        )
        assert response.status_code == 302
        assert response.url == view_recommendation_url


class TestF680MyRecommendationView:
    def test_view_my_recommendation(
        self,
        authorized_client,
        data_submitted_f680_case,
        mock_f680_case,
        recommendations,
        mock_current_gov_user,
        mock_get_case_recommendations,
        view_recommendation_url,
    ):
        response = authorized_client.get(view_recommendation_url)
        assert response.status_code == 200
        assertTemplateUsed(response, "f680/case/recommendation/view_my_recommendation.html")

        soup = BeautifulSoup(response.content, "html.parser")
        assert soup.find("h1", {"class": "govuk-heading-xl"}).text == "View recommendation"
        assert soup.find("h2", {"class": "govuk-heading-m"}).text.strip() == "australia name [Official]"
        assert soup.find("div", {"class": "clearance-conditions"}).text == "No concerns"
