import pytest

from caseworker.core.services import get_control_list_entries, group_denial_reasons


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
