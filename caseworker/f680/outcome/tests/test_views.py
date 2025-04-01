import pytest
from http import HTTPStatus

from django.urls import reverse

from caseworker.f680.outcome.constants import OutcomeSteps
from caseworker.f680.outcome import forms
from core import client


@pytest.fixture(autouse=True)
def setup(
    data_queue,
    f680_case_id,
    mock_queue,
    mock_case,
    mock_approval_reason,
    mock_denial_reasons,
    mock_footnote_details,
    settings,
    mock_get_case_recommendations,
):
    settings.FEATURE_FLAG_ALLOW_F680 = True
    return


@pytest.fixture
def decide_outcome_url(data_queue, f680_case_id):
    return reverse("cases:f680:outcome:decide_outcome", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})


@pytest.fixture
def post_to_step(post_to_step_factory, decide_outcome_url):
    return post_to_step_factory(decide_outcome_url)


@pytest.fixture
def mock_current_gov_user(requests_mock, current_user, f680_case_id):
    return requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{f680_case_id}"),
        json={"user": {"id": current_user["id"]}},
    )


@pytest.fixture
def mock_outcomes_no_outcomes(requests_mock, data_submitted_f680_case):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/outcome/"
    return requests_mock.get(url, json=[], status_code=HTTPStatus.OK)


@pytest.fixture
def mock_POST_outcome(requests_mock, data_submitted_f680_case):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/outcome/"
    return requests_mock.post(url, json={}, status_code=HTTPStatus.CREATED)


class TestDecideOutcomeView:

    def test_GET_select_outcome(
        self,
        authorized_client,
        requests_mock,
        f680_case_id,
        data_submitted_f680_case,
        mock_f680_case,
        mock_outcomes_no_outcomes,
        decide_outcome_url,
    ):
        security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
        expected_security_release_request_choices = [
            [
                request["id"],
                f"{request['recipient']['name']} - {request['recipient']['country']['name']} - {request['security_grading']['value']}",
            ]
            for request in security_release_requests
        ]
        request_ids = [request["id"] for request in security_release_requests]
        response = authorized_client.get(decide_outcome_url)
        assert response.status_code == HTTPStatus.OK
        form = response.context["form"]
        assert isinstance(form, forms.SelectOutcomeForm)
        assert (
            response.context["form"].fields["security_release_requests"].choices
            == expected_security_release_request_choices
        )

    def test_GET_select_outcome_existing_outcome(
        self,
        authorized_client,
        requests_mock,
        f680_case_id,
        data_submitted_f680_case,
        mock_f680_case,
        mock_outcomes_single_outcome,
        decide_outcome_url,
        data_outcomes,
    ):
        security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
        existing_outcome_id = data_outcomes[0]["security_release_requests"][0]
        expected_security_release_request_choices = [
            [
                request["id"],
                f"{request['recipient']['name']} - {request['recipient']['country']['name']} - {request['security_grading']['value']}",
            ]
            for request in security_release_requests
            if request["id"] != existing_outcome_id
        ]
        request_ids = [request["id"] for request in security_release_requests]
        response = authorized_client.get(decide_outcome_url)
        assert response.status_code == HTTPStatus.OK
        form = response.context["form"]
        assert isinstance(form, forms.SelectOutcomeForm)
        assert (
            response.context["form"].fields["security_release_requests"].choices
            == expected_security_release_request_choices
        )

    @pytest.mark.parametrize(
        "outcome, expected_form_class",
        (
            ["approve", forms.ApproveOutcomeForm],
            ["refuse", forms.RefuseOutcomeForm],
        ),
    )
    def test_POST_select_outcome(
        self,
        authorized_client,
        requests_mock,
        f680_case_id,
        data_submitted_f680_case,
        mock_f680_case,
        mock_outcomes_no_outcomes,
        post_to_step,
        outcome,
        expected_form_class,
    ):
        security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
        request_ids = [request["id"] for request in security_release_requests]
        response = post_to_step(
            OutcomeSteps.SELECT_OUTCOME,
            {
                "outcome": outcome,
                "security_release_requests": request_ids,
            },
        )
        assert response.status_code == HTTPStatus.OK
        form = response.context["form"]
        assert isinstance(form, expected_form_class)

    def test_POST_select_outcome_bad_request(
        self,
        authorized_client,
        requests_mock,
        f680_case_id,
        data_submitted_f680_case,
        mock_f680_case,
        mock_outcomes_no_outcomes,
        post_to_step,
    ):
        security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
        request_ids = [request["id"] for request in security_release_requests]
        response = post_to_step(
            OutcomeSteps.SELECT_OUTCOME,
            {},
        )
        assert response.status_code == HTTPStatus.OK
        form = response.context["form"]
        assert isinstance(form, forms.SelectOutcomeForm)
        assert form.errors == {
            "outcome": ["Select if you approve or refuse"],
            "security_release_requests": ["This field is required."],
        }

    def test_POST_approve(
        self,
        authorized_client,
        requests_mock,
        f680_case_id,
        data_submitted_f680_case,
        data_queue,
        mock_f680_case,
        mock_outcomes_no_outcomes,
        post_to_step,
        mock_POST_outcome,
    ):
        security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
        request_ids = [request["id"] for request in security_release_requests]
        response = post_to_step(
            OutcomeSteps.SELECT_OUTCOME,
            {
                "outcome": "approve",
                "security_release_requests": request_ids,
            },
        )
        assert response.status_code == HTTPStatus.OK

        response = post_to_step(
            OutcomeSteps.APPROVE,
            {
                "conditions": "my conditions",
                "approval_types": ["training"],
                "security_grading": "secret",
            },
        )
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse(
            "cases:f680:recommendation",
            kwargs={"queue_pk": data_queue["id"], "pk": data_submitted_f680_case["case"]["id"]},
        )
        assert mock_POST_outcome.call_count == 1
        request = mock_POST_outcome.request_history.pop()
        assert request.json() == {
            "outcome": "approve",
            "conditions": "my conditions",
            "approval_types": ["training"],
            "security_grading": "secret",
            "security_release_requests": request_ids,
        }

    def test_POST_approve_bad_request(
        self,
        authorized_client,
        requests_mock,
        f680_case_id,
        data_submitted_f680_case,
        data_queue,
        mock_f680_case,
        mock_outcomes_no_outcomes,
        post_to_step,
        mock_POST_outcome,
    ):
        security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
        request_ids = [request["id"] for request in security_release_requests]
        response = post_to_step(
            OutcomeSteps.SELECT_OUTCOME,
            {
                "outcome": "approve",
                "security_release_requests": request_ids,
            },
        )
        assert response.status_code == HTTPStatus.OK

        response = post_to_step(
            OutcomeSteps.APPROVE,
            {},
        )
        assert response.status_code == HTTPStatus.OK
        form = response.context["form"]
        assert form.errors == {
            "security_grading": ["Select the security grading"],
            "approval_types": ["This field is required."],
        }

    def test_POST_partial_approve(
        self,
        authorized_client,
        requests_mock,
        f680_case_id,
        data_submitted_f680_case,
        data_queue,
        mock_f680_case,
        mock_outcomes_no_outcomes,
        post_to_step,
        mock_POST_outcome,
    ):
        security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
        # Only approve for one ID
        request_ids = [security_release_requests[0]["id"]]
        response = post_to_step(
            OutcomeSteps.SELECT_OUTCOME,
            {
                "outcome": "approve",
                "security_release_requests": request_ids,
            },
        )
        assert response.status_code == HTTPStatus.OK

        response = post_to_step(
            OutcomeSteps.APPROVE,
            {
                "conditions": "my conditions",
                "approval_types": ["training"],
                "security_grading": "secret",
            },
        )
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse(
            "cases:f680:outcome:decide_outcome",
            kwargs={"queue_pk": data_queue["id"], "pk": data_submitted_f680_case["case"]["id"]},
        )

        assert mock_POST_outcome.call_count == 1
        request = mock_POST_outcome.request_history.pop()
        assert request.json() == {
            "outcome": "approve",
            "conditions": "my conditions",
            "approval_types": ["training"],
            "security_grading": "secret",
            "security_release_requests": request_ids,
        }

    def test_POST_refuse(
        self,
        authorized_client,
        requests_mock,
        f680_case_id,
        data_submitted_f680_case,
        mock_f680_case,
        mock_outcomes_no_outcomes,
        post_to_step,
        mock_POST_outcome,
    ):
        security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
        request_ids = [request["id"] for request in security_release_requests]
        response = post_to_step(
            OutcomeSteps.SELECT_OUTCOME,
            {
                "outcome": "refuse",
                "security_release_requests": request_ids,
            },
        )
        assert response.status_code == HTTPStatus.OK

        response = post_to_step(
            OutcomeSteps.REFUSE,
            {
                "refusal_reasons": "my reasons",
            },
        )
        assert response.status_code == HTTPStatus.FOUND
        assert mock_POST_outcome.call_count == 1
        request = mock_POST_outcome.request_history.pop()
        assert request.json() == {
            "outcome": "refuse",
            "refusal_reasons": "my reasons",
            "security_release_requests": request_ids,
        }

    def test_POST_refuse_bad_request(
        self,
        authorized_client,
        requests_mock,
        f680_case_id,
        data_submitted_f680_case,
        mock_f680_case,
        mock_outcomes_no_outcomes,
        post_to_step,
        mock_POST_outcome,
    ):
        security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
        request_ids = [request["id"] for request in security_release_requests]
        response = post_to_step(
            OutcomeSteps.SELECT_OUTCOME,
            {
                "outcome": "refuse",
                "security_release_requests": request_ids,
            },
        )
        assert response.status_code == HTTPStatus.OK

        response = post_to_step(
            OutcomeSteps.REFUSE,
            {},
        )
        assert response.status_code == HTTPStatus.OK
        form = response.context["form"]
        assert form.errors == {
            "refusal_reasons": ["This field is required."],
        }
