import re
import pytest

from caseworker.core.services import get_control_list_entries, group_denial_reasons, get_permissible_statuses
from caseworker.cases.objects import Case
from caseworker.cases.constants import CaseType
from core.constants import CaseStatusEnum
from core import client
from caseworker.advice.constants import LICENSING_UNIT_TEAM


def test_group_denial_reasons():
    denial_reasons = [
        {
            "id": "1",
            "deprecated": True,
            "description": "denial reason 1",
            "display_value": "1",
        },
        {
            "id": "1a",
            "deprecated": False,
            "description": "denial reason 1a",
            "display_value": "1a",
        },
        {
            "id": "1b",
            "deprecated": False,
            "description": "denial reason 1b",
            "display_value": "1b",
        },
    ]

    result = group_denial_reasons(denial_reasons)

    expected_result = [("1", [("1a", "1a"), ("1b", "1b")])]

    assert list(result) == expected_result


@pytest.mark.parametrize(("include_non_selectable_for_assessment"), [False, True])
def test_get_control_list_entries_cache_empty_success(
    include_non_selectable_for_assessment, mock_control_list_entries, mock_request, data_control_list_entries
):
    control_list_entries = get_control_list_entries(mock_request)

    assert control_list_entries == data_control_list_entries

    assert mock_control_list_entries.called_once


@pytest.mark.parametrize(("include_non_selectable_for_assessment"), [False, True])
def test_get_control_list_entries_cache_read_success(
    include_non_selectable_for_assessment, mock_control_list_entries, mock_request, data_control_list_entries
):
    control_list_entries = get_control_list_entries(mock_request)

    assert control_list_entries == data_control_list_entries

    assert mock_control_list_entries.called_once

    # get CLEs again

    control_list_entries = get_control_list_entries(mock_request)

    assert control_list_entries == data_control_list_entries

    assert mock_control_list_entries.call_count == 1


def test_get_permissible_statuses(mock_request, mock_gov_user, data_standard_case):
    statuses = get_permissible_statuses(mock_request, Case(data_standard_case["case"]))
    assert len(statuses) == 24
    status_keys = [status_dict["key"] for status_dict in statuses]
    assert set(status_keys) == {
        CaseStatusEnum.APPEAL_FINAL_REVIEW,
        CaseStatusEnum.APPEAL_REVIEW,
        CaseStatusEnum.AWAITING_EXPORTER_RESPONSE,
        CaseStatusEnum.CHANGE_INITIAL_REVIEW,
        CaseStatusEnum.CHANGE_UNDER_FINAL_REVIEW,
        CaseStatusEnum.CHANGE_UNDER_REVIEW,
        CaseStatusEnum.DEREGISTERED,
        CaseStatusEnum.FINAL_REVIEW_COUNTERSIGN,
        CaseStatusEnum.FINAL_REVIEW_SECOND_COUNTERSIGN,
        CaseStatusEnum.INITIAL_CHECKS,
        CaseStatusEnum.OGD_ADVICE,
        CaseStatusEnum.OGD_CONSOLIDATION,
        CaseStatusEnum.OPEN,
        CaseStatusEnum.REOPENED_DUE_TO_ORG_CHANGES,
        CaseStatusEnum.REOPENED_FOR_CHANGES,
        CaseStatusEnum.RESUBMITTED,
        CaseStatusEnum.RETURN_TO_INSPECTOR,
        CaseStatusEnum.SUBMITTED,
        CaseStatusEnum.UNDER_APPEAL,
        CaseStatusEnum.UNDER_ECJU_REVIEW,
        CaseStatusEnum.UNDER_FINAL_REVIEW,
        CaseStatusEnum.UNDER_INTERNAL_REVIEW,
        CaseStatusEnum.UNDER_REVIEW,
        CaseStatusEnum.WITHDRAWN,
    }


def test_get_permissible_statuses_for_licencing_unit_team(
    mock_request, data_standard_case, requests_mock, gov_uk_user_id, mock_case_statuses
):
    data = {
        "user": {
            "role": {"statuses": mock_case_statuses["statuses"]},
            "team": {"id": LICENSING_UNIT_TEAM},
        }
    }
    url = client._build_absolute_uri("/gov-users/")
    requests_mock.get(url=f"{url}me/", json=data)
    requests_mock.get(url=re.compile(f"{url}{gov_uk_user_id}/"), json=data)

    statuses = get_permissible_statuses(mock_request, Case(data_standard_case["case"]))
    assert len(statuses) == 25
    status_keys = [status_dict["key"] for status_dict in statuses]
    assert set(status_keys) == {
        CaseStatusEnum.APPEAL_FINAL_REVIEW,
        CaseStatusEnum.APPEAL_REVIEW,
        CaseStatusEnum.AWAITING_EXPORTER_RESPONSE,
        CaseStatusEnum.CHANGE_INITIAL_REVIEW,
        CaseStatusEnum.CHANGE_UNDER_FINAL_REVIEW,
        CaseStatusEnum.CHANGE_UNDER_REVIEW,
        CaseStatusEnum.DEREGISTERED,
        CaseStatusEnum.FINAL_REVIEW_COUNTERSIGN,
        CaseStatusEnum.FINAL_REVIEW_SECOND_COUNTERSIGN,
        CaseStatusEnum.INITIAL_CHECKS,
        CaseStatusEnum.OGD_ADVICE,
        CaseStatusEnum.OGD_CONSOLIDATION,
        CaseStatusEnum.OPEN,
        CaseStatusEnum.REOPENED_DUE_TO_ORG_CHANGES,
        CaseStatusEnum.REOPENED_FOR_CHANGES,
        CaseStatusEnum.RESUBMITTED,
        CaseStatusEnum.RETURN_TO_INSPECTOR,
        CaseStatusEnum.SUBMITTED,
        CaseStatusEnum.UNDER_APPEAL,
        CaseStatusEnum.UNDER_ECJU_REVIEW,
        CaseStatusEnum.UNDER_FINAL_REVIEW,
        CaseStatusEnum.UNDER_INTERNAL_REVIEW,
        CaseStatusEnum.UNDER_REVIEW,
        CaseStatusEnum.WITHDRAWN,
        CaseStatusEnum.FINALISED,
    }


def test_get_permissible_statuses_for_not_supported_case_type(mock_request, mock_gov_user, data_standard_case):
    data_standard_case["case"]["case_type"]["type"]["key"] = CaseType.COMPLIANCE.value
    statuses = get_permissible_statuses(mock_request, Case(data_standard_case["case"]))
    assert statuses == []


def test_get_permissible_statuses_for_f680(mock_request, mock_gov_user, data_standard_case):
    data_standard_case["case"]["case_type"]["type"]["key"] = CaseType.SECURITY_CLEARANCE.value
    statuses = get_permissible_statuses(mock_request, Case(data_standard_case["case"]))
    assert len(statuses) == 5
    status_keys = [status_dict["key"] for status_dict in statuses]
    assert set(status_keys) == {
        CaseStatusEnum.SUBMITTED,
        CaseStatusEnum.OGD_ADVICE,
        CaseStatusEnum.UNDER_FINAL_REVIEW,
        CaseStatusEnum.WITHDRAWN,
        CaseStatusEnum.REOPENED_FOR_CHANGES,
    }
