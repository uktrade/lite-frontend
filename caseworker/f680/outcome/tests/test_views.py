import pytest

from freezegun import freeze_time
from http import HTTPStatus

from dateutil.relativedelta import relativedelta
from django.urls import reverse
from django.utils import timezone

from core import client
from core.exceptions import ServiceError

from caseworker.f680.outcome.constants import OutcomeSteps, OutcomeType, SecurityReleaseOutcomeDuration
from caseworker.f680.outcome import forms


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
def decide_outcome_url(data_queue, f680_case_id):
    return reverse("cases:f680:outcome:decide_outcome", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})


@pytest.fixture
def clear_outcome_url(data_queue, f680_case_id, data_outcome_id):
    return reverse(
        "cases:f680:outcome:clear_outcome",
        kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id, "outcome_id": data_outcome_id},
    )


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


@pytest.fixture
def mock_DELETE_outcome(requests_mock, data_submitted_f680_case, data_outcome_id):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/outcome/{data_outcome_id}/"
    return requests_mock.delete(url, status_code=HTTPStatus.NO_CONTENT)


@pytest.fixture
def mock_DELETE_outcome_outcome_missing(requests_mock, data_submitted_f680_case, data_outcome_id):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/outcome/{data_outcome_id}/"
    return requests_mock.delete(url, status_code=HTTPStatus.NOT_FOUND)


@pytest.fixture
def mock_DELETE_outcome_server_error(requests_mock, data_submitted_f680_case, data_outcome_id):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/outcome/{data_outcome_id}/"
    return requests_mock.delete(url, json={"error": "error"}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@pytest.fixture
def mock_get_case_recommendations_multiple(
    requests_mock, data_submitted_f680_case, current_user, MOD_team1, MOD_team2, fcdo_team, recommendations
):
    security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
    recommendations.extend(
        [
            {
                "created_at": "2021-10-16T23:48:39.486679+01:00",
                "id": "529c5596-fe8b-4540-988b-c37805cd08de",  # /PS-IGNORE
                "type": {"key": "approve", "value": "Approve"},
                "conditions": "No concerns",
                "refusal_reasons": "",
                "security_grading": {"key": "official", "value": "Official"},
                "security_grading_other": "",
                "security_release_request": security_release_requests[0]["id"],
                "user": current_user,
                "team": MOD_team1,
            },
            {
                "created_at": "2021-10-16T23:48:39.486679+01:00",
                "id": "529c5596-fe8b-4540-988b-c37805cd08de",  # /PS-IGNORE
                "type": {"key": "approve", "value": "Approve"},
                "conditions": "some concerns",
                "refusal_reasons": "",
                "security_grading": {"key": "official", "value": "Official"},
                "security_grading_other": "",
                "security_release_request": security_release_requests[0]["id"],
                "user": current_user,
                "team": MOD_team2,
            },
            {
                "created_at": "2021-10-16T23:48:39.486679+01:00",
                "id": "529c5596-fe8b-4540-988b-c37805cd08de",  # /PS-IGNORE
                "type": {"key": "refuse", "value": "Refuse"},
                "conditions": "",
                "refusal_reasons": "some reasons",
                "security_release_request": security_release_requests[0]["id"],
                "security_grading": None,
                "security_grading_other": "",
                "user": current_user,
                "team": fcdo_team,
            },
        ]
    )
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/recommendation/"
    return requests_mock.get(url, json=recommendations, status_code=200)


@pytest.fixture
def mock_get_case_refuse_recommendations_multiple(
    requests_mock, data_submitted_f680_case, current_user, MOD_team1, MOD_team2, fcdo_team, recommendations
):
    security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
    recommendations.extend(
        [
            {
                "created_at": "2021-10-16T23:48:39.486679+01:00",
                "id": "529c5596-fe8b-4540-988b-c37805cd08de",  # /PS-IGNORE
                "type": {"key": "refuse", "value": "Refuse"},
                "conditions": "",
                "refusal_reasons": "Criteria 1: one\n\n--------\nCriteria 5a: five",
                "security_grading": None,
                "security_grading_other": "",
                "security_release_request": security_release_requests[0]["id"],
                "user": current_user,
                "team": MOD_team1,
            },
            {
                "created_at": "2021-10-16T23:48:39.486679+01:00",
                "id": "529c5596-fe8b-4540-988b-c37805cd08de",  # /PS-IGNORE
                "type": {"key": "refuse", "value": "Refuse"},
                "conditions": "",
                "refusal_reasons": "Criteria 1: one\n\n--------\nCriteria 5a: five",
                "security_grading": None,
                "security_grading_other": "",
                "security_release_request": security_release_requests[0]["id"],
                "user": current_user,
                "team": MOD_team2,
            },
            {
                "created_at": "2021-10-16T23:48:39.486679+01:00",
                "id": "529c5596-fe8b-4540-988b-c37805cd08de",  # /PS-IGNORE
                "type": {"key": "refuse", "value": "Refuse"},
                "conditions": "",
                "refusal_reasons": "Criteria 1: one\n\n--------\nCriteria 5a: five\n\n--------\nmore reasons",
                "security_release_request": security_release_requests[0]["id"],
                "security_grading": None,
                "security_grading_other": "",
                "user": current_user,
                "team": fcdo_team,
            },
        ]
    )
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/recommendation/"
    return requests_mock.get(url, json=recommendations, status_code=200)


class TestDecideOutcomeView:

    def test_GET_select_outcome(
        self,
        authorized_client,
        f680_case_id,
        data_submitted_f680_case,
        mock_f680_case,
        mock_outcomes_no_outcomes,
        decide_outcome_url,
        recommendations,
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
        assert response.context["selected_security_release_requests"] == []
        expected_all_security_release_requests = {
            "approval_types": ["demonstration_overseas", "training"],
            "id": request_ids[0],
            "intended_use": "australia intended use",
            "product_id": data_submitted_f680_case["case"]["data"]["product"]["id"],
            "recipient": {
                "address": "australia address",
                "country": {
                    "id": "AU",
                    "is_eu": False,
                    "name": "Australia",
                    "report_name": "",
                    "type": "gov.uk Country",
                },
                "id": data_submitted_f680_case["case"]["data"]["security_release_requests"][0]["recipient"]["id"],
                "name": "australia name",
                "role": {"key": "consultant", "value": "Consultant"},
                "role_other": None,
                "type": {"key": "third-party", "value": "Third party"},
            },
            "recommendations": [
                {
                    "conditions": "No concerns",
                    "created_at": "2021-10-16T23:48:39.486679+01:00",
                    "id": recommendations[0]["id"],
                    "refusal_reasons": "",
                    "security_release_request_id": request_ids[0],
                    "team": {
                        "alias": None,
                        "id": "00000000-0000-0000-0000-000000000001",
                        "is_ogd": False,
                        "name": "Admin",
                        "part_of_ecju": None,
                    },
                    "type": {"key": "approve", "value": "Approve"},
                    "user": {
                        "email": "test.user@example.com",  # /PS-IGNORE
                        "first_name": "Test",
                        "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",  # /PS-IGNORE
                        "last_name": "User",
                        "role_name": "Super User",
                        "status": "Active",
                        "team": {
                            "alias": None,
                            "id": "00000000-0000-0000-0000-000000000001",
                            "is_ogd": False,
                            "name": "Admin",
                            "part_of_ecju": None,
                        },
                    },
                }
            ],
            "security_grading": {"key": "secret", "value": "Secret"},
            "security_grading_other": "",
        }

        assert response.context["all_security_release_requests"][0] == expected_all_security_release_requests

    def test_GET_select_outcome_existing_outcome(
        self,
        authorized_client,
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
        f680_case_id,
        data_submitted_f680_case,
        mock_f680_case,
        mock_outcomes_no_outcomes,
        post_to_step,
        outcome,
        expected_form_class,
        recommendations,
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
        expected_selected_security_release_requests = {
            "approval_types": ["demonstration_overseas", "training"],
            "id": request_ids[0],
            "intended_use": "australia intended use",
            "product_id": data_submitted_f680_case["case"]["data"]["product"]["id"],
            "recipient": {
                "address": "australia address",
                "country": {
                    "id": "AU",
                    "is_eu": False,
                    "name": "Australia",
                    "report_name": "",
                    "type": "gov.uk Country",
                },
                "id": data_submitted_f680_case["case"]["data"]["security_release_requests"][0]["recipient"]["id"],
                "name": "australia name",
                "role": {"key": "consultant", "value": "Consultant"},
                "role_other": None,
                "type": {"key": "third-party", "value": "Third party"},
            },
            "recommendations": [
                {
                    "conditions": "No concerns",
                    "created_at": "2021-10-16T23:48:39.486679+01:00",
                    "id": recommendations[0]["id"],
                    "refusal_reasons": "",
                    "security_release_request_id": request_ids[0],
                    "team": {
                        "alias": None,
                        "id": "00000000-0000-0000-0000-000000000001",
                        "is_ogd": False,
                        "name": "Admin",
                        "part_of_ecju": None,
                    },
                    "type": {"key": "approve", "value": "Approve"},
                    "user": {
                        "email": "test.user@example.com",  # /PS-IGNORE
                        "first_name": "Test",
                        "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",  # /PS-IGNORE
                        "last_name": "User",
                        "role_name": "Super User",
                        "status": "Active",
                        "team": {
                            "alias": None,
                            "id": "00000000-0000-0000-0000-000000000001",
                            "is_ogd": False,
                            "name": "Admin",
                            "part_of_ecju": None,
                        },
                    },
                }
            ],
            "security_grading": {"key": "secret", "value": "Secret"},
            "security_grading_other": "",
        }

        assert response.context["selected_security_release_requests"][0] == expected_selected_security_release_requests

    def test_POST_select_approve_outcome_conditions_aggregated(
        self,
        authorized_client,
        f680_case_id,
        data_submitted_f680_case,
        mock_f680_case,
        mock_outcomes_no_outcomes,
        post_to_step,
        mock_get_case_recommendations_multiple,
    ):
        security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
        request_ids = [request["id"] for request in security_release_requests]
        response = post_to_step(
            OutcomeSteps.SELECT_OUTCOME,
            {
                "outcome": OutcomeType.APPROVE,
                "security_release_requests": request_ids,
            },
        )
        assert response.status_code == HTTPStatus.OK
        form = response.context["form"]
        assert isinstance(form, forms.ApproveOutcomeForm)
        # Expect a de-duplicated set of conditions
        assert form.initial == {"conditions": "No concerns\r\n\r\nsome concerns"}

    def test_POST_select_refuse_outcome_reasons_aggregated(
        self,
        authorized_client,
        f680_case_id,
        data_submitted_f680_case,
        mock_f680_case,
        mock_outcomes_no_outcomes,
        post_to_step,
        mock_get_case_refuse_recommendations_multiple,
    ):
        security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
        request_ids = [request["id"] for request in security_release_requests]
        response = post_to_step(
            OutcomeSteps.SELECT_OUTCOME,
            {
                "outcome": OutcomeType.REFUSE,
                "security_release_requests": request_ids,
            },
        )
        assert response.status_code == HTTPStatus.OK
        form = response.context["form"]
        assert isinstance(form, forms.RefuseOutcomeForm)
        # Expect a de-duplicated set of refusal reasons
        assert form.initial == {
            "refusal_reasons": "Criteria 1: one\n\n--------\nCriteria 5a: five\r\n\r\nCriteria 1: one\n\n--------\nCriteria 5a: five\n\n--------\nmore reasons"
        }

    def test_POST_select_outcome_bad_request(
        self,
        authorized_client,
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

    @freeze_time("2025-04-15")
    def test_POST_approve(
        self,
        authorized_client,
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
        validity_start_date = timezone.now().date().isoformat()
        validity_end_date = (
            timezone.now().date()
            + relativedelta(
                months=+SecurityReleaseOutcomeDuration.MONTHS_48,
            )
        ).isoformat()
        response = post_to_step(
            OutcomeSteps.SELECT_OUTCOME,
            {
                "outcome": OutcomeType.APPROVE,
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
                "validity_start_date_0": validity_start_date.split("-")[2],
                "validity_start_date_1": validity_start_date.split("-")[1],
                "validity_start_date_2": validity_start_date.split("-")[0],
                "validity_period": SecurityReleaseOutcomeDuration.MONTHS_48,
            },
            follow=True,
        )
        assert response.status_code == HTTPStatus.OK
        assert response.redirect_chain[-1][0] == reverse(
            "cases:f680:recommendation",
            kwargs={"queue_pk": data_queue["id"], "pk": data_submitted_f680_case["case"]["id"]},
        )
        messages = [str(msg) for msg in response.context["messages"]]
        assert messages == ["Outcomes for 3 security releases saved successfully"]

        assert mock_POST_outcome.call_count == 1
        request = mock_POST_outcome.request_history.pop()
        assert request.json() == {
            "outcome": OutcomeType.APPROVE,
            "conditions": "my conditions",
            "approval_types": ["training"],
            "security_grading": "secret",
            "security_release_requests": request_ids,
            "validity_start_date": validity_start_date,
            "validity_end_date": validity_end_date,
        }

    def test_POST_approve_bad_request(
        self,
        authorized_client,
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
                "outcome": OutcomeType.APPROVE,
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
            "security_grading": ["Select the security release"],
            "approval_types": ["Select approval types"],
            "validity_start_date": ["Enter the validity start date"],
            "validity_period": ["Select validity period"],
        }

    @freeze_time("2025-04-15")
    def test_POST_partial_approve(
        self,
        authorized_client,
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
        validity_start_date = timezone.now().date().isoformat()
        validity_end_date = (
            timezone.now().date()
            + relativedelta(
                months=+SecurityReleaseOutcomeDuration.MONTHS_24,
            )
        ).isoformat()
        response = post_to_step(
            OutcomeSteps.SELECT_OUTCOME,
            {
                "outcome": OutcomeType.APPROVE,
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
                "validity_start_date_0": validity_start_date.split("-")[2],
                "validity_start_date_1": validity_start_date.split("-")[1],
                "validity_start_date_2": validity_start_date.split("-")[0],
                "validity_period": SecurityReleaseOutcomeDuration.MONTHS_24,
            },
            follow=True,
        )
        assert response.status_code == HTTPStatus.OK
        assert response.redirect_chain[-1][0] == reverse(
            "cases:f680:outcome:decide_outcome",
            kwargs={"queue_pk": data_queue["id"], "pk": data_submitted_f680_case["case"]["id"]},
        )
        messages = [str(msg) for msg in response.context["messages"]]
        assert messages == ["Outcome saved successfully"]

        assert mock_POST_outcome.call_count == 1
        request = mock_POST_outcome.request_history.pop()
        assert request.json() == {
            "outcome": OutcomeType.APPROVE,
            "conditions": "my conditions",
            "approval_types": ["training"],
            "security_grading": "secret",
            "security_release_requests": request_ids,
            "validity_start_date": validity_start_date,
            "validity_end_date": validity_end_date,
        }

    def test_POST_refuse(
        self,
        authorized_client,
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
                "outcome": OutcomeType.REFUSE,
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
            "outcome": OutcomeType.REFUSE,
            "refusal_reasons": "my reasons",
            "security_release_requests": request_ids,
        }

    def test_POST_refuse_bad_request(
        self,
        authorized_client,
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
                "outcome": OutcomeType.REFUSE,
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
            "refusal_reasons": ["Enter refusal reasons"],
        }


class TestClearOutcome:

    def test_POST_outcome_missing(
        self,
        authorized_client,
        data_queue,
        data_submitted_f680_case,
        mock_f680_case,
        mock_outcomes_single_outcome,
        clear_outcome_url,
        data_outcome_id,
        mock_DELETE_outcome_outcome_missing,
    ):
        with pytest.raises(ServiceError):
            response = authorized_client.post(clear_outcome_url)
        assert mock_DELETE_outcome_outcome_missing.call_count == 1

    def test_POST_api_error(
        self,
        authorized_client,
        data_queue,
        data_submitted_f680_case,
        mock_f680_case,
        mock_outcomes_single_outcome,
        clear_outcome_url,
        data_outcome_id,
        mock_DELETE_outcome_server_error,
    ):
        with pytest.raises(ServiceError):
            response = authorized_client.post(clear_outcome_url)
        assert mock_DELETE_outcome_server_error.call_count == 1

    def test_POST_success(
        self,
        authorized_client,
        data_queue,
        data_submitted_f680_case,
        mock_f680_case,
        mock_outcomes_single_outcome,
        clear_outcome_url,
        data_outcome_id,
        mock_DELETE_outcome,
    ):
        response = authorized_client.post(clear_outcome_url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse(
            "cases:f680:recommendation",
            kwargs={"queue_pk": data_queue["id"], "pk": data_submitted_f680_case["case"]["id"]},
        )
        assert mock_DELETE_outcome.call_count == 1
