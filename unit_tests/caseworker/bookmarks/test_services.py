import pytest
import requests
import uuid

from decimal import Decimal

from caseworker.bookmarks.services import enrich_filter_for_saving, BookmarkEnricher
from unit_tests.caseworker.conftest import GOV_USER_ID


def new_bookmarks(filter):
    return [{"name": "Name", "description": "", "filter_json": filter, "id": uuid.uuid4()}]


@pytest.fixture()
def all_cles(data_control_list_entries):
    return data_control_list_entries["control_list_entries"]


@pytest.fixture()
def all_regimes(data_regime_entries):
    return [{"id": regime["pk"], "name": regime["name"]} for regime in data_regime_entries]


@pytest.fixture()
def request_with_session(rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()

    return request


@pytest.mark.parametrize(
    "bookmark_filter, expected_description",
    [
        ({}, ""),
        ({"case_reference": "GBSIEL/2023"}, "Case reference: GBSIEL/2023"),
        ({"case_officer": GOV_USER_ID}, "Licensing Unit case officer: John Smith"),
        ({"assigned_user": GOV_USER_ID}, "Case adviser: John Smith"),
        ({"status": "ogd_advice"}, "Case status: OGD Advice"),
        ({"control_list_entry": ["ML1", "ML1a"]}, "Control list entry: ML1, ML1a"),
        ({"submitted_from": "12-12-2010"}, "Submitted after: 12-12-2010"),
        ({"is_trigger_list": True}, "Trigger list: True"),
        ({"countries": ["DE"]}, "Country: Germany"),
        (
            {
                "regime_entry": [
                    "d73d0273-ef94-4951-9c51-c291eba949a0",  #  /PS-IGNORE
                    "c760976f-fd14-4356-9f23-f6eaf084475d",  #  /PS-IGNORE
                ],
            },
            "Regime entry: mtcr-1, wassenaar-1",
        ),
        (
            {
                "case_officer": GOV_USER_ID,
                "assigned_user": GOV_USER_ID,
                "status": "ogd_advice",
                "control_list_entry": ["ML1", "ML1a"],
                "submitted_from": "12-12-2010",
                "is_trigger_list": True,
                "countries": ["DE"],
            },
            "Case adviser: John Smith, Case status: OGD Advice, Control list entry: ML1, ML1a, Country: Germany, Licensing Unit case officer: John Smith, Submitted after: 12-12-2010, Trigger list: True",
        ),
        ({"invalid_field_name": "invalid field value"}, ""),
        (
            {
                "case_reference": "GBSIEL/2023",
                "invalid_field_name": "invalid field value",
            },
            "Case reference: GBSIEL/2023",
        ),
        (
            {
                "case_officer": "not-a-real-id",
            },
            "",
        ),
        (
            {
                "case_reference": "GBSIEL/2023",
                "case_officer": "not-a-real-id",
            },
            "Case reference: GBSIEL/2023",
        ),
    ],
)
def test_description_from_filter(
    request_with_session,
    filter_data,
    bookmark_filter,
    expected_description,
    flags,
    all_cles,
    all_regimes,
    mock_countries,
    mock_queues_list,
    data_queue,
):
    bookmarks = new_bookmarks(bookmark_filter)
    enricher = BookmarkEnricher(request_with_session, filter_data, flags, all_cles, all_regimes, data_queue, "/queues/")
    enriched = enricher.enrich_for_display(bookmarks)

    # description = description_from_filter(bookmark_filter, filter_data, flags)
    assert len(enriched) == 1
    assert enriched[0]["description"] == expected_description


@pytest.mark.parametrize(
    "bookmark_filter, expected_description, expected_url_params",
    [
        (
            {"submitted_from": "07-06-2022"},
            "Submitted after: 07-06-2022",
            "submitted_from_0=07&submitted_from_1=06&submitted_from_2=2022",
        ),
        (
            {"submitted_to": "23-11-1990"},
            "Submitted before: 23-11-1990",
            "submitted_to_0=23&submitted_to_1=11&submitted_to_2=1990",
        ),
        (
            {"finalised_from": "31-12-2007"},
            "Finalised after: 31-12-2007",
            "finalised_from_0=31&finalised_from_1=12&finalised_from_2=2007",
        ),
        (
            {"finalised_to": "01-03-2011"},
            "Finalised before: 01-03-2011",
            "finalised_to_0=01&finalised_to_1=03&finalised_to_2=2011",
        ),
        (
            {"countries": ["DE"]},
            "Country: Germany",
            "countries=DE",
        ),
        (
            {
                "regime_entry": ["d73d0273-ef94-4951-9c51-c291eba949a0"],  #  /PS-IGNORE
            },
            "Regime entry: wassenaar-1",
            "regime_entry=d73d0273-ef94-4951-9c51-c291eba949a0",  #  /PS-IGNORE
        ),
        (
            {
                "regime_entry": [
                    "d73d0273-ef94-4951-9c51-c291eba949a0",  #  /PS-IGNORE
                    "c760976f-fd14-4356-9f23-f6eaf084475d",  #  /PS-IGNORE
                ],
            },
            "Regime entry: mtcr-1, wassenaar-1",
            "regime_entry=d73d0273-ef94-4951-9c51-c291eba949a0&regime_entry=c760976f-fd14-4356-9f23-f6eaf084475d",  #  /PS-IGNORE
        ),
        (
            {"control_list_entry": ["ML1", "ML1a"]},
            "Control list entry: ML1, ML1a",
            "control_list_entry=ML1&control_list_entry=ML1a",
        ),
        (
            {"flags": ["798d5e92-c31a-48cc-9e6b-d3fc6dfd65f2", "e50f5cd3-331c-4914-b618-ee6eb67a081c"]},
            "Flags: AG Review Required, BAE",
            "flags=798d5e92-c31a-48cc-9e6b-d3fc6dfd65f2&flags=e50f5cd3-331c-4914-b618-ee6eb67a081c",
        ),
        (
            {"is_trigger_list": True},
            "Trigger list: True",
            "is_trigger_list=True",
        ),
        (
            {"max_total_value": "200.0"},
            "Max total value (£): 200.0",
            "max_total_value=200.0",
        ),
    ],
)
def test_enrich_bookmark_for_display(
    request_with_session,
    filter_data,
    bookmark_filter,
    expected_description,
    expected_url_params,
    flags,
    all_cles,
    all_regimes,
    mock_countries,
    mock_queues_list,
    data_queue,
):
    bookmarks = new_bookmarks(bookmark_filter)

    enricher = BookmarkEnricher(request_with_session, filter_data, flags, all_cles, all_regimes, data_queue, "/queues/")
    enriched = enricher.enrich_for_display(bookmarks)

    assert len(enriched) == 1
    assert enriched[0]["description"] == expected_description
    assert enriched[0]["url"] == f"/queues/?{expected_url_params}"


def test_enrich_bookmark_for_display_custom_base_url(
    request_with_session,
    filter_data,
    flags,
    all_cles,
    all_regimes,
    mock_countries,
    mock_queues_list,
    data_queue,
):
    bookmarks = new_bookmarks({"is_trigger_list": True})

    enricher = BookmarkEnricher(
        request_with_session, filter_data, flags, all_cles, all_regimes, data_queue, "/queues/abcd"
    )
    enriched = enricher.enrich_for_display(bookmarks)

    assert len(enriched) == 1
    assert enriched[0]["description"] == "Trigger list: True"
    assert enriched[0]["url"] == f"/queues/abcd?is_trigger_list=True"


class ObjectToForceException:
    def __str__(self):
        raise Exception("This object breaks when str() called")


def test_enrich_bookmark_for_display_filters_out_errors(
    request_with_session,
    filter_data,
    all_cles,
    all_regimes,
    flags,
):
    bookmark_filter = {"dodgy_filter_entry": ObjectToForceException()}
    bookmarks = new_bookmarks(bookmark_filter)

    enricher = BookmarkEnricher(request_with_session, filter_data, flags, all_cles, all_regimes, None, "/queues/")
    enriched = enricher.enrich_for_display(bookmarks)

    assert len(enriched) == 0


@pytest.mark.parametrize(
    "name, filter_data, raw_filters, expected_filter_data",
    [
        (
            "Test unwanted entries are removed",
            {"case_reference": "ABC/123", "save": True, "saved_filter_description": "Filter_1"},
            {
                "case_reference": "ABC/123",
                "_id_country": "Germany",
                "regime": "",
                "_id_regime": "",
                "save": True,
                "saved_filter_description": "Filter_1",
            },
            {"case_reference": "ABC/123"},
        ),
        (
            "Test _id_ entry is copied over if the corresponding entry is present",
            {"country": "DE"},
            {"country": "DE", "_id_country": "Germany", "regime": "", "_id_regime": ""},
            {"country": "DE", "_id_country": "Germany"},
        ),
        (
            "Test _id_ entry is copied over for mulitple entries",
            {"country": "DE", "regime": "2594daef-8156-4e78-b4c4-e25f6cdbd203"},
            {
                "country": "DE",
                "_id_country": "Germany",
                "regime": "2594daef-8156-4e78-b4c4-e25f6cdbd203",
                "_id_regime": "Wassenaar Arrangement Sensitive",
            },
            {
                "country": "DE",
                "_id_country": "Germany",
                "regime": "2594daef-8156-4e78-b4c4-e25f6cdbd203",
                "_id_regime": "Wassenaar Arrangement Sensitive",
            },
        ),
        (
            "Test decimal value converted properly",
            {"max_total_value": Decimal(200)},
            {
                "max_total_value": Decimal(200),
            },
            {"max_total_value": "200"},
        ),
    ],
)
def test_enrich_filter_for_saving(name, filter_data, raw_filters, expected_filter_data):
    actual_filter = enrich_filter_for_saving(filter_data, raw_filters)

    assert sorted(actual_filter.items()) == sorted(expected_filter_data.items())
