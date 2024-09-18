from django.core.cache import cache

from caseworker.core.services import get_control_list_entries, group_denial_reasons
from lite_forms.components import Option


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


def test_get_control_list_entries_grouped_cache_empty_success(mock_control_list_entries_grouped_get, mock_request):
    assert cache.get("caseworker_control_list_entries_grouped_cache") is None

    control_list_entries_grouped = get_control_list_entries(mock_request)
    assert control_list_entries_grouped == [
        {
            "id": "3fc955d3-1b0e-406f-96ee-b2a3c237f9bd",
            "rating": "ML1",
            "text": "Smooth-bore weapons with a calibre of less than 20mm, other firearms and automatic weapons with a calibre of 12.7mm or less, and accessories and specially designed components",
            "parent_id": None,
            "category": "UK Military List",
            "controlled": True,
            "selectable_for_assessment": True,
            "children": [
                {
                    "id": "0b9116c2-3aa0-49fb-a590-944b4738b208",
                    "rating": "ML1a",
                    "text": "Rifles and combination guns, handguns, machine, sub-machine and volley guns",
                    "parent_id": "3fc955d3-1b0e-406f-96ee-b2a3c237f9bd",
                    "category": "UK Military List",
                    "controlled": True,
                    "selectable_for_assessment": True,
                }
            ],
        }
    ]

    # assert that the API is called to get the grouped list of CLEs
    assert mock_control_list_entries_grouped_get.called_once

    # assert that the grouped CLEs are in the cache
    assert cache.get("caseworker_control_list_entries_grouped_cache") == control_list_entries_grouped


def test_get_control_list_entries_grouped_cached_data_success(mock_control_list_entries_grouped_get, mock_request):
    # arrange test following empty cache test above
    assert cache.get("caseworker_control_list_entries_grouped_cache") is None
    control_list_entries_grouped = get_control_list_entries(mock_request)
    assert control_list_entries_grouped == [
        {
            "id": "3fc955d3-1b0e-406f-96ee-b2a3c237f9bd",
            "rating": "ML1",
            "text": "Smooth-bore weapons with a calibre of less than 20mm, other firearms and automatic weapons with a calibre of 12.7mm or less, and accessories and specially designed components",
            "parent_id": None,
            "category": "UK Military List",
            "controlled": True,
            "selectable_for_assessment": True,
            "children": [
                {
                    "id": "0b9116c2-3aa0-49fb-a590-944b4738b208",
                    "rating": "ML1a",
                    "text": "Rifles and combination guns, handguns, machine, sub-machine and volley guns",
                    "parent_id": "3fc955d3-1b0e-406f-96ee-b2a3c237f9bd",
                    "category": "UK Military List",
                    "controlled": True,
                    "selectable_for_assessment": True,
                }
            ],
        }
    ]
    assert mock_control_list_entries_grouped_get.called_once

    # get grouped CLEs again
    control_list_entries_grouped = get_control_list_entries(mock_request)

    # assert that call_count == 1 because the cached data was used
    assert mock_control_list_entries_grouped_get.call_count == 1

    # assert that the CLEs are still in the cache
    assert cache.get("caseworker_control_list_entries_grouped_cache") == control_list_entries_grouped


def test_get_control_list_entries_convert_to_options_cache_empty_success(mock_control_list_entries_get, mock_request):
    assert cache.get("caseworker_control_list_entries_cache") is None

    converted_control_list_entries = get_control_list_entries(mock_request, convert_to_options=True)

    for option in converted_control_list_entries:
        assert type(option) == Option
    converted_control_list_entries_dicts = [
        {"key": option.key, "value": option.value, "description": option.description}
        for option in converted_control_list_entries
    ]
    assert converted_control_list_entries_dicts == [
        {"description": "some text", "key": "ML1a", "value": "ML1a"},
        {"description": "some text", "key": "ML22b", "value": "ML22b"},
    ]

    # assert that the API is called to get the grouped list of CLEs
    assert mock_control_list_entries_get.called_once

    # assert that the CLEs are in the cache
    assert cache.get("caseworker_control_list_entries_cache") == [
        {"rating": "ML1a", "text": "some text"},
        {"rating": "ML22b", "text": "some text"},
    ]


def test_get_control_list_entries_convert_to_options_cached_data_success(mock_control_list_entries_get, mock_request):
    # arrange test following empty cache test above
    assert cache.get("caseworker_control_list_entries_cache") is None
    converted_control_list_entries = get_control_list_entries(mock_request, convert_to_options=True)
    for option in converted_control_list_entries:
        assert type(option) == Option
    converted_control_list_entries_dicts = [
        {"key": option.key, "value": option.value, "description": option.description}
        for option in converted_control_list_entries
    ]
    assert converted_control_list_entries_dicts == [
        {"description": "some text", "key": "ML1a", "value": "ML1a"},
        {"description": "some text", "key": "ML22b", "value": "ML22b"},
    ]
    assert mock_control_list_entries_get.called_once

    # get CLE options again
    converted_control_list_entries = get_control_list_entries(mock_request, convert_to_options=True)

    # assert that call_count == 1 because the cached data was used
    assert mock_control_list_entries_get.call_count == 1

    # assert that the CLEs are still in the cache
    assert cache.get("caseworker_control_list_entries_cache") == [
        {"rating": "ML1a", "text": "some text"},
        {"rating": "ML22b", "text": "some text"},
    ]


def test_get_control_list_entries_including_parent_empty_cache_success(
    mock_control_list_entries_including_parent_get, mock_request
):
    assert cache.get("caseworker_control_list_entries_including_parent_cache") is None

    control_list_entries_including_parent = get_control_list_entries(mock_request, include_parent=True)

    assert control_list_entries_including_parent == [
        {
            "rating": "ML1",
            "text": "Smooth-bore weapons with a calibre of less than 20mm, other firearms and automatic weapons with a calibre of 12.7mm or less, and accessories and specially designed components",
            "parent": None,
        },
        {
            "rating": "ML1a",
            "text": "Rifles and combination guns, handguns, machine, sub-machine and volley guns",
            "parent": "3fc955d3-1b0e-406f-96ee-b2a3c237f9bd",
        },
    ]

    # assert that the API is called to get the list of CLEs including parent
    assert mock_control_list_entries_including_parent_get.called_once

    # assert that the CLEs including parent are in the cache
    assert cache.get("caseworker_control_list_entries_including_parent_cache") == control_list_entries_including_parent


def test_get_control_list_entries_including_parent_cached_data_success(
    mock_control_list_entries_including_parent_get, mock_request
):
    # arrange test following empty cache test above
    assert cache.get("caseworker_control_list_entries_including_parent_cache") is None
    control_list_entries_including_parent = get_control_list_entries(mock_request, include_parent=True)
    assert control_list_entries_including_parent == [
        {
            "rating": "ML1",
            "text": "Smooth-bore weapons with a calibre of less than 20mm, other firearms and automatic weapons with a calibre of 12.7mm or less, and accessories and specially designed components",
            "parent": None,
        },
        {
            "rating": "ML1a",
            "text": "Rifles and combination guns, handguns, machine, sub-machine and volley guns",
            "parent": "3fc955d3-1b0e-406f-96ee-b2a3c237f9bd",
        },
    ]
    assert mock_control_list_entries_including_parent_get.called_once

    # get CLEs including parent again
    control_list_entries_including_parent = get_control_list_entries(mock_request, include_parent=True)

    # assert that call_count == 1 because the cached data was used
    assert mock_control_list_entries_including_parent_get.call_count == 1

    # assert that the CLEs including parent are still in the cache
    assert cache.get("caseworker_control_list_entries_including_parent_cache") == control_list_entries_including_parent
