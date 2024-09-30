from exporter.core.services import get_control_list_entries


def test_get_control_list_entries_cache_empty_success(
    mock_exporter_control_list_entries, mock_request, data_control_list_entries
):
    control_list_entries = get_control_list_entries(mock_request)

    assert control_list_entries == data_control_list_entries

    assert mock_exporter_control_list_entries.called_once


def test_get_control_list_entries_cache_read_success(
    mock_exporter_control_list_entries, mock_request, data_control_list_entries
):
    control_list_entries = get_control_list_entries(mock_request)

    assert control_list_entries == data_control_list_entries

    assert mock_exporter_control_list_entries.called_once

    # get CLEs again

    control_list_entries = get_control_list_entries(mock_request)

    assert control_list_entries == data_control_list_entries

    assert mock_exporter_control_list_entries.call_count == 1
