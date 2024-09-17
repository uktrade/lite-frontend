from django.core.cache import cache

from exporter.core.services import get_control_list_entries


def test_get_control_list_entries_cache_empty_success(mock_exporter_control_list_entries_get, mock_request):
    assert cache.get("exporter_control_list_entries_cache") is None

    control_list_entries = get_control_list_entries(mock_request)
    assert control_list_entries == [{"rating": "ML1a", "text": "some text"}, {"rating": "ML22b", "text": "some text"}]

    # assert that the API is called to get the list of CLEs
    assert mock_exporter_control_list_entries_get.called_once

    # assert that the CLEs are in the cache
    assert cache.get("exporter_control_list_entries_cache") == control_list_entries


def test_get_control_list_entries_cached_data_success(mock_exporter_control_list_entries_get, mock_request):
    # arrange test following empty cache test above
    assert cache.get("exporter_control_list_entries_cache") is None
    control_list_entries = get_control_list_entries(mock_request)
    assert control_list_entries == [{"rating": "ML1a", "text": "some text"}, {"rating": "ML22b", "text": "some text"}]
    assert mock_exporter_control_list_entries_get.called_once

    # get CLEs again
    control_list_entries = get_control_list_entries(mock_request)

    # assert that call_count == 1 because the cached data was used
    assert mock_exporter_control_list_entries_get.call_count == 1

    # assert that the CLEs are still in the cache
    assert cache.get("exporter_control_list_entries_cache") == control_list_entries
