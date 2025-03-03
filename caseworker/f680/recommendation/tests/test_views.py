import pytest

from bs4 import BeautifulSoup
from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from caseworker.advice.constants import AdviceSteps
from caseworker.f680.recommendation.forms.forms import (
    FootnotesApprovalAdviceForm,
    PicklistLicenceConditionsForm,
    RecommendAnApprovalForm,
    SelectRecommendationTypeForm,
    SimpleLicenceConditionsForm,
)
from core import client


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    mock_approval_reason,
    mock_denial_reasons,
    mock_footnote_details,
):
    return


@pytest.fixture
def url_approve(data_queue, f680_case_id):
    return reverse("cases:f680:approve_all", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})


@pytest.fixture
def view_recommendation_url(data_queue, f680_case_id):
    return reverse("cases:f680:view_my_recommendation", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})


@pytest.fixture
def post_to_step(post_to_step_factory, url_approve):
    return post_to_step_factory(url_approve)


@pytest.fixture
def mock_current_gov_user(requests_mock, f680_case_id):
    return requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{f680_case_id}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )


@pytest.fixture
def recommendation(current_user, admin_team):
    return [
        {
            "created_at": "2021-10-16T23:48:39.486679+01:00",
            "denial_reasons": [],
            "id": "429c5596-fe8b-4540-988b-c37805cd08de",  # /PS-IGNORE
            "level": "user",
            "note": "additional notes",
            "text": "No concerns",
            "type": {"key": "approve", "value": "Approve"},
            "user": current_user,
            "team": admin_team,
        }
    ]


class TestF680RecommendationView:

    def test_GET_recommendation_success(
        self,
        authorized_client,
        queue_f680_cases_to_review,
        current_user,
        mock_f680_case,
        f680_case_id,
        f680_reference_code,
        data_submitted_f680_case,
    ):
        url = reverse(
            "cases:f680:recommendation", kwargs={"queue_pk": queue_f680_cases_to_review["id"], "pk": f680_case_id}
        )
        data_submitted_f680_case["case"]["assigned_users"] = {queue_f680_cases_to_review["name"]: [{"id": current_user["id"]}]}
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
            == f'/queues/{queue_f680_cases_to_review["id"]}/cases/{f680_case_id}/f680/recommendation/select-recommendation-type/'
        )

    @pytest.mark.parametrize(
        "recommendation_type",
        [
            {"key": "approve", "value": "Approve"},
            {"key": "proviso", "value": "Proviso"},
        ],
    )
    def test_GET_recommendation_page_existing_recommendation(
        self,
        authorized_client,
        queue_f680_cases_to_review,
        current_user,
        mock_f680_case,
        f680_case_id,
        data_submitted_f680_case,
        recommendation,
        recommendation_type,
    ):
        url = reverse(
            "cases:f680:recommendation", kwargs={"queue_pk": queue_f680_cases_to_review["id"], "pk": f680_case_id}
        )
        data_submitted_f680_case["case"]["assigned_users"] = {queue_f680_cases_to_review["name"]: [{"id": current_user["id"]}]}
        recommendation[0]["type"] = recommendation_type
        data_submitted_f680_case["case"]["advice"] = recommendation
        response = authorized_client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "f680/case/recommendation/recommendation.html")
        assertTemplateUsed(response, "f680/case/recommendation/other-recommendations.html")

        soup = BeautifulSoup(response.content, "html.parser")
        all_teams_recommendation = soup.find_all("summary", {"class": "govuk-details__summary"})
        assert len(all_teams_recommendation) == 1
        actual_string = all_teams_recommendation[0].text.replace("\n", "").strip()
        assert actual_string == f"{current_user['team']['name']}"


class TestF680SelectRecommendationTypeView:

    def test_GET_select_recommendation_type(
        self, authorized_client, data_queue, mock_f680_case, f680_case_id, f680_reference_code, data_submitted_f680_case
    ):
        url = reverse(
            "cases:f680:select_recommendation_type", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id}
        )
        response = authorized_client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "f680/case/recommendation/select_recommendation_type.html")
        assert dict(response.context["case"]) == data_submitted_f680_case["case"]

        form = response.context["form"]
        assert isinstance(form, SelectRecommendationTypeForm)
        assert form.fields["recommendation"].choices == [("approve_all", "Approve all")]

    @pytest.mark.parametrize("recommendation, redirect", [("approve_all", "approve-all")])
    def test_submit_select_recommendation_type(
        self,
        authorized_client,
        data_queue,
        mock_f680_case,
        f680_case_id,
        f680_reference_code,
        data_submitted_f680_case,
        recommendation,
        redirect,
    ):
        url = reverse(
            "cases:f680:select_recommendation_type", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id}
        )
        response = authorized_client.post(url, data={"recommendation": recommendation})
        assert response.status_code == 302
        assert (
            response.url
            == f'/queues/00000000-0000-0000-0000-000000000001/cases/{data_submitted_f680_case["case"]["id"]}/f680/recommendation/{redirect}/'
        )


class TestF680GiveApprovalRecommendationView:

    def test_give_approval_advice_get(self, authorized_client, beautiful_soup, mock_f680_case, url_approve):
        response = authorized_client.get(url_approve)
        assert response.status_code == 200
        assertTemplateUsed(response, "f680/case/recommendation/form_wizard.html")

        soup = beautiful_soup(response.content)
        header = soup.find("h1", {"class": "govuk-heading-xl"})
        assert header.text == "Recommend an approval"

        form = response.context["form"]
        assert isinstance(form, RecommendAnApprovalForm)
        assert list(form.fields.keys()) == ["approval_reasons", "approval_radios", "add_licence_conditions"]

    def test_approval_advice_post_valid(
        self,
        authorized_client,
        data_submitted_f680_case,
        url_approve,
        mock_f680_case,
        mock_approval_reason,
        mock_proviso,
        mock_footnote_details,
        mock_post_recommendation,
        post_to_step,
        beautiful_soup,
    ):
        response = post_to_step(
            AdviceSteps.RECOMMEND_APPROVAL,
            {"approval_reasons": "No concerns"},
        )
        assert response.status_code == 302

    def test_approval_advice_post_valid_add_conditional(
        self,
        authorized_client,
        data_queue,
        f680_case_id,
        data_submitted_f680_case,
        url_approve,
        mock_f680_case,
        mock_approval_reason,
        mock_proviso,
        mock_footnote_details,
        mock_post_recommendation,
        post_to_step,
        beautiful_soup,
    ):
        response = post_to_step(
            AdviceSteps.RECOMMEND_APPROVAL,
            {"approval_reasons": "reason", "add_licence_conditions": True},
        )
        assert response.status_code == 200

        soup = beautiful_soup(response.content)
        # redirected to next form
        form = response.context["form"]
        assert isinstance(form, PicklistLicenceConditionsForm)

        header = soup.find("h1")
        assert header.text == "Add licence conditions (optional)"

        add_LC_response = post_to_step(AdviceSteps.LICENCE_CONDITIONS, {"proviso": "proviso"})
        assert add_LC_response.status_code == 200
        soup = beautiful_soup(add_LC_response.content)
        # redirected to next form
        form = add_LC_response.context["form"]
        assert isinstance(form, FootnotesApprovalAdviceForm)
        header = soup.find("h1")
        assert header.text == "Add instructions to the exporter, or a reporting footnote (optional)"

        add_instructions_response = post_to_step(
            AdviceSteps.LICENCE_FOOTNOTES,
            {"instructions_to_exporter": "instructions", "footnote_details": "footnotes"},
        )
        assert add_instructions_response.status_code == 302
        assert (
            add_instructions_response.url
            == f'/queues/{data_queue["id"]}/cases/{f680_case_id}/f680/recommendation/view-my-recommendation/'
        )

    def test_approval_advice_post_valid_add_conditional_optional(
        self,
        authorized_client,
        data_queue,
        f680_case_id,
        data_submitted_f680_case,
        url_approve,
        mock_f680_case,
        mock_approval_reason,
        mock_footnote_details,
        mock_post_recommendation,
        mock_proviso_no_results,
        post_to_step,
        beautiful_soup,
    ):
        response = post_to_step(
            AdviceSteps.RECOMMEND_APPROVAL,
            {"approval_reasons": "reason", "add_licence_conditions": True},
        )
        assert response.status_code == 200

        soup = beautiful_soup(response.content)
        # redirected to next form
        form = response.context["form"]
        assert isinstance(form, SimpleLicenceConditionsForm)

        header = soup.find("h1")
        assert header.text == "Add licence conditions (optional)"

        add_LC_response = post_to_step(AdviceSteps.LICENCE_CONDITIONS, {})
        assert add_LC_response.status_code == 200
        soup = beautiful_soup(add_LC_response.content)
        # redirected to next form
        form = add_LC_response.context["form"]
        assert isinstance(form, FootnotesApprovalAdviceForm)
        header = soup.find("h1")
        assert header.text == "Add instructions to the exporter, or a reporting footnote (optional)"

        add_instructions_response = post_to_step(
            AdviceSteps.LICENCE_FOOTNOTES,
            {"instructions_to_exporter": "instructions", "footnote_details": "footnotes"},
        )
        assert add_instructions_response.status_code == 302
        assert (
            add_instructions_response.url
            == f'/queues/{data_queue["id"]}/cases/{f680_case_id}/f680/recommendation/view-my-recommendation/'
        )


class TestF680MyRecommendationView:
    def test_view_approve_recommendation(
        self,
        authorized_client,
        data_submitted_f680_case,
        mock_f680_case,
        mock_current_gov_user,
        recommendation,
        view_recommendation_url,
    ):
        data_submitted_f680_case["case"]["advice"] = recommendation
        response = authorized_client.get(view_recommendation_url)
        assert response.status_code == 200
        assertTemplateUsed(response, "f680/case/recommendation/view_my_recommendation.html")

        soup = BeautifulSoup(response.content, "html.parser")
        assert soup.find("h1", {"class": "govuk-heading-xl"}).text == "View recommendation"
        assert soup.find("h2", {"class": "govuk-heading-m"}).text == "Reason for approving"
        assert soup.find("p", {"class": "govuk-body"}).text == "No concerns"
