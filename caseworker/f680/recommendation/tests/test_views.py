import pytest

from bs4 import BeautifulSoup
from pytest_django.asserts import assertTemplateUsed
from unittest import mock

from django.urls import reverse

from caseworker.f680.recommendation.constants import (
    RecommendationSteps,
    RecommendationType,
    RecommendationSecurityGrading,
)
from caseworker.f680.recommendation.forms.forms import (
    BasicRecommendationForm,
    BasicRecommendationRefusalReasonsForm,
    ClearRecommendationForm,
    EntityConditionsForm,
    EntityRefusalReasonsForm,
)
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
    mock_proviso,
    mock_get_case_recommendations,
    settings,
):
    settings.FEATURE_FLAG_ALLOW_F680 = True
    return


@pytest.fixture
def make_recommendation_url(data_queue, f680_case_id):
    return reverse("cases:f680:make_recommendation", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})


@pytest.fixture
def view_recommendation_url(data_queue, f680_case_id):
    return reverse("cases:f680:view_my_recommendation", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})


@pytest.fixture
def clear_recommendation_url(data_queue, f680_case_id):
    return reverse("cases:f680:clear_recommendation", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})


@pytest.fixture
def post_to_step(post_to_step_factory, make_recommendation_url):
    return post_to_step_factory(make_recommendation_url)


@pytest.fixture
def mock_current_gov_user(requests_mock, current_user, f680_case_id):
    return requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{f680_case_id}"),
        json={"user": {"id": current_user["id"]}},
    )


@pytest.fixture
def mock_clear_recommendations(requests_mock, data_submitted_f680_case):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/recommendation/"
    return requests_mock.delete(url, status_code=204)


@pytest.fixture
def hydrated_recommendations(data_submitted_f680_case, recommendations):
    for item in recommendations:
        release_id = item["security_release_request"]
        item["security_release_request"] = next(
            item
            for item in data_submitted_f680_case["case"]["data"]["security_release_requests"]
            if item["id"] == release_id
        )

    return recommendations


class TestF680RecommendationView:

    def test_GET_recommendation_success(
        self,
        authorized_client,
        queue_f680_cases_to_review,
        current_user,
        mock_f680_case,
        mock_get_case_no_recommendations,
        mock_outcomes_no_outcomes,
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

    def test_GET_recommendation_success_with_outcome(
        self,
        authorized_client,
        queue_f680_cases_to_review,
        current_user,
        mock_f680_case,
        mock_get_case_no_recommendations,
        mock_outcomes_single_outcome,
        f680_case_id,
        f680_reference_code,
        data_submitted_f680_case,
        data_outcomes,
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
        assert len(response.context["outcomes"]) == 1
        assert response.context["outcomes"][0]["id"] == data_outcomes[0]["id"]

    def test_GET_recommendation_page_existing_recommendation(
        self,
        authorized_client,
        queue_f680_cases_to_review,
        current_user,
        mock_f680_case,
        mock_outcomes_no_outcomes,
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
        soup = BeautifulSoup(response.content, "html.parser")
        clear_recommendation_button = soup.find(id="clear-recommendation-button")
        assert clear_recommendation_button


class TestF680MakeRecommendationView:

    @mock.patch("caseworker.f680.recommendation.services.get_case_recommendations")
    def test_make_recommendation_post_all_entities(
        self,
        mock_case_recommendations,
        authorized_client,
        requests_mock,
        f680_case_id,
        data_submitted_f680_case,
        mock_f680_case,
        mock_proviso,
        mock_denial_reasons,
        mock_post_recommendation,
        post_to_step,
        view_recommendation_url,
        hydrated_recommendations,
    ):
        mock_case_recommendations.side_effect = [[], [], hydrated_recommendations]
        release_requests_ids = [
            item["id"] for item in data_submitted_f680_case["case"]["data"]["security_release_requests"]
        ]
        response = post_to_step(
            RecommendationSteps.ENTITIES_AND_DECISION,
            {
                "release_requests": release_requests_ids,
                "recommendation": RecommendationType.APPROVE,
            },
        )
        assert response.status_code == 200
        form = response.context["form"]
        assert isinstance(form, EntityConditionsForm)

        response = post_to_step(
            RecommendationSteps.RELEASE_REQUEST_PROVISOS,
            {
                "security_grading": "official",
                "conditions": ["no_release", "no_specifications"],
                "no_specifications": "no specifications",
                "no_release": "no release",
            },
        )
        assert response.status_code == 302
        assert response.url == view_recommendation_url

        request = requests_mock.last_request
        assert request.method == "POST"
        assert request.path == f"/caseworker/f680/{f680_case_id}/recommendation/"
        assert request.json() == [
            {
                "type": RecommendationType.APPROVE,
                "security_grading": RecommendationSecurityGrading.OFFICIAL,
                "security_grading_other": "",
                "conditions": "no release\n\n--------\nno specifications",
                "refusal_reasons": "",
                "security_release_request": release_request_id,
            }
            for release_request_id in release_requests_ids
        ]

    @mock.patch("caseworker.f680.recommendation.services.get_case_recommendations")
    def test_make_recommendation_post_few_entities(
        self,
        mock_pending_requests,
        authorized_client,
        requests_mock,
        f680_case_id,
        data_submitted_f680_case,
        data_queue,
        mock_f680_case,
        mock_proviso,
        mock_denial_reasons,
        mock_post_recommendation,
        post_to_step,
        hydrated_recommendations,
    ):
        mock_pending_requests.side_effect = [[], [], hydrated_recommendations[:2]]
        release_requests_ids = [
            item["id"] for item in data_submitted_f680_case["case"]["data"]["security_release_requests"]
        ]
        response = post_to_step(
            RecommendationSteps.ENTITIES_AND_DECISION,
            {
                "release_requests": release_requests_ids[:2],
                "recommendation": RecommendationType.REFUSE,
            },
        )
        assert response.status_code == 200
        form = response.context["form"]
        assert isinstance(form, EntityRefusalReasonsForm)

        response = post_to_step(
            RecommendationSteps.RELEASE_REQUEST_REFUSAL_REASONS,
            {
                "refusal_reasons": ["1", "2"],
                "1": "one",
                "2": "two",
            },
        )
        assert response.status_code == 302
        assert response.url == reverse(
            "cases:f680:recommendation", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id}
        )

        request = requests_mock.last_request
        assert request.method == "POST"
        assert request.path == f"/caseworker/f680/{f680_case_id}/recommendation/"
        assert request.json() == [
            {
                "type": RecommendationType.REFUSE,
                "security_grading": "",
                "security_grading_other": "",
                "conditions": "",
                "refusal_reasons": "one\n\n--------\ntwo",
                "security_release_request": release_request_id,
            }
            for release_request_id in release_requests_ids[:2]
        ]

    @mock.patch("caseworker.f680.recommendation.services.get_case_recommendations")
    def test_make_recommendation_post_no_team_provisos(
        self,
        mock_case_recommendations,
        authorized_client,
        requests_mock,
        f680_case_id,
        data_submitted_f680_case,
        mock_f680_case,
        mock_no_provisos,
        mock_post_recommendation,
        post_to_step,
        view_recommendation_url,
        hydrated_recommendations,
    ):
        mock_case_recommendations.side_effect = [[], [], hydrated_recommendations]
        release_requests_ids = [
            item["id"] for item in data_submitted_f680_case["case"]["data"]["security_release_requests"]
        ]
        response = post_to_step(
            RecommendationSteps.ENTITIES_AND_DECISION,
            {
                "release_requests": release_requests_ids,
                "recommendation": RecommendationType.APPROVE,
            },
        )
        assert response.status_code == 200
        form = response.context["form"]
        assert isinstance(form, BasicRecommendationForm)

        response = post_to_step(
            RecommendationSteps.RELEASE_REQUEST_NO_PROVISOS,
            {
                "security_grading": RecommendationSecurityGrading.OFFICIAL,
                "conditions": "no release",
            },
        )
        assert response.status_code == 302
        assert response.url == view_recommendation_url

        request = requests_mock.request_history.pop()
        assert request.method == "POST"
        assert request.path == f"/caseworker/f680/{f680_case_id}/recommendation/"
        assert request.json() == [
            {
                "type": RecommendationType.APPROVE,
                "security_grading": RecommendationSecurityGrading.OFFICIAL,
                "security_grading_other": "",
                "conditions": "no release",
                "refusal_reasons": "",
                "security_release_request": release_request_id,
            }
            for release_request_id in release_requests_ids
        ]

    @mock.patch("caseworker.f680.recommendation.services.get_case_recommendations")
    def test_make_recommendation_post_no_denial_reasons(
        self,
        mock_case_recommendations,
        authorized_client,
        requests_mock,
        f680_case_id,
        data_submitted_f680_case,
        mock_f680_case,
        mock_no_denial_reasons,
        mock_post_recommendation,
        post_to_step,
        view_recommendation_url,
        hydrated_recommendations,
    ):
        mock_case_recommendations.side_effect = [[], [], hydrated_recommendations]
        release_requests_ids = [
            item["id"] for item in data_submitted_f680_case["case"]["data"]["security_release_requests"]
        ]
        response = post_to_step(
            RecommendationSteps.ENTITIES_AND_DECISION,
            {"release_requests": release_requests_ids, "recommendation": RecommendationType.REFUSE},
        )
        assert response.status_code == 200
        form = response.context["form"]
        assert isinstance(form, BasicRecommendationRefusalReasonsForm)

        response = post_to_step(
            RecommendationSteps.RELEASE_REQUEST_NO_REFUSAL_REASONS,
            {
                "refusal_reasons": "doesn't meet the criteria",
            },
        )
        assert response.status_code == 302
        assert response.url == view_recommendation_url

        request = requests_mock.request_history.pop()
        assert request.method == "POST"
        assert request.path == f"/caseworker/f680/{f680_case_id}/recommendation/"
        assert request.json() == [
            {
                "type": RecommendationType.REFUSE,
                "security_grading": "",
                "security_grading_other": "",
                "conditions": "",
                "refusal_reasons": "doesn't meet the criteria",
                "security_release_request": release_request_id,
            }
            for release_request_id in release_requests_ids
        ]


class TestF680MyRecommendationView:
    def test_view_my_recommendation(
        self,
        authorized_client,
        data_submitted_f680_case,
        queue_f680_cases_to_review,
        current_user,
        mock_f680_case,
        mock_current_gov_user,
        mock_get_case_recommendations,
        view_recommendation_url,
    ):
        data_submitted_f680_case["case"]["assigned_users"] = {
            queue_f680_cases_to_review["name"]: [{"id": current_user["id"]}]
        }
        response = authorized_client.get(view_recommendation_url)
        assert response.status_code == 200
        assertTemplateUsed(response, "f680/case/recommendation/view_my_recommendation.html")

        soup = BeautifulSoup(response.content, "html.parser")
        assert soup.find("h1", {"class": "govuk-heading-xl"}).text == "View recommendation"
        assert soup.find("h2", {"class": "govuk-heading-m"}).text.strip() == "australia name"
        assert soup.find("div", {"class": "clearance-conditions"}).text == "No concerns"
        clear_recommendation_button = soup.find(id="clear-recommendation-button")
        assert clear_recommendation_button

    def test_clear_my_recommendation_get(
        self,
        authorized_client,
        data_submitted_f680_case,
        mock_f680_case,
        mock_current_gov_user,
        mock_get_case_recommendations,
        clear_recommendation_url,
        view_recommendation_url,
    ):
        response = authorized_client.get(clear_recommendation_url)
        assert response.status_code == 200
        assertTemplateUsed(response, "f680/case/recommendation/clear_recommendation.html")

        assert isinstance(response.context["form"], ClearRecommendationForm)

        soup = BeautifulSoup(response.content, "html.parser")
        assert (
            soup.find("h1", {"class": "govuk-heading-xl"}).text
            == "Are you sure you want to delete your recommendation on this case?"
        )
        confirm_button = soup.find(id="submit-id-submit")
        assert confirm_button

        cancel_link = soup.find("a", {"class": "govuk-button"})
        assert cancel_link
        assert cancel_link["href"] == view_recommendation_url

    def test_clear_my_recommendation_post(
        self,
        authorized_client,
        requests_mock,
        f680_case_id,
        mock_f680_case,
        mock_current_gov_user,
        mock_get_case_recommendations,
        mock_clear_recommendations,
        clear_recommendation_url,
        data_queue,
        data_submitted_f680_case,
    ):
        response = authorized_client.post(clear_recommendation_url)
        assert response.status_code == 302
        assert response.url == reverse(
            "cases:f680:recommendation",
            kwargs={"queue_pk": data_queue["id"], "pk": data_submitted_f680_case["case"]["id"]},
        )
        request = requests_mock.request_history.pop()
        assert request.method == "DELETE"
        assert request.path == f"/caseworker/f680/{f680_case_id}/recommendation/"
        assert request.json() == {}
