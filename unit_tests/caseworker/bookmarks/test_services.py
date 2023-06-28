import uuid

import pytest

from caseworker.bookmarks.services import enrich_filter_for_saving, BookmarkEnricher
from unit_tests.caseworker.conftest import GOV_USER_ID


def new_bookmarks(filter):
    return [{"name": "Name", "description": "", "filter_json": filter, "id": uuid.uuid4()}]


@pytest.fixture()
def all_regimes(data_regime_entries):
    return [{"id": regime["pk"], "name": regime["name"]} for regime in data_regime_entries]


@pytest.mark.parametrize(
    "bookmark_filter, expected_description",
    [
        ({}, ""),
        ({"country": "AZ"}, "Country: AZ"),
        ({"case_reference": "GBSIEL/2023"}, "Case reference: GBSIEL/2023"),
        ({"case_officer": GOV_USER_ID}, "Case officer: John Smith"),
        ({"assigned_user": GOV_USER_ID}, "Assigned user: John Smith"),
        ({"case_type": "gift"}, "Case type: MOD Gifting Clearance"),
        ({"status": "ogd_advice"}, "Status: OGD Advice"),
        ({"team_advice_type": "no_licence_required"}, "Team advice type: No Licence Required"),
        ({"final_advice_type": "not_applicable"}, "Final advice type: Not Applicable"),
        (
            {
                "final_advice_type": "not_applicable",
                "case_officer": GOV_USER_ID,
                "assigned_user": GOV_USER_ID,
                "case_type": "gift",
                "status": "ogd_advice",
                "team_advice_type": "no_licence_required",
                "country": "AZ",
            },
            "Final advice type: Not Applicable, Case officer: John Smith, Assigned user: John Smith, Case type: MOD "
            "Gifting Clearance, Status: OGD Advice, Team advice type: No Licence Required, Country: AZ",
        ),
    ],
)
def test_description_from_filter(filter_data, bookmark_filter, expected_description, flags):
    bookmarks = new_bookmarks(bookmark_filter)
    enricher = BookmarkEnricher(filter_data, flags, None, "/queues/")
    enriched = enricher.enrich_for_display(bookmarks)

    # description = description_from_filter(bookmark_filter, filter_data, flags)
    assert len(enriched) == 1
    assert enriched[0]["description"] == expected_description


@pytest.mark.parametrize(
    "bookmark_filter, expected_description, expected_url_params",
    [
        (
            {"submitted_from": "07-06-2022"},
            "Submitted from: 07-06-2022",
            "submitted_from_0=07&submitted_from_1=06&submitted_from_2=2022",
        ),
        (
            {"submitted_to": "23-11-1990"},
            "Submitted to: 23-11-1990",
            "submitted_to_0=23&submitted_to_1=11&submitted_to_2=1990",
        ),
        (
            {"finalised_from": "31-12-2007"},
            "Finalised from: 31-12-2007",
            "finalised_from_0=31&finalised_from_1=12&finalised_from_2=2007",
        ),
        (
            {"finalised_to": "01-03-2011"},
            "Finalised to: 01-03-2011",
            "finalised_to_0=01&finalised_to_1=03&finalised_to_2=2011",
        ),
        (
            {"country": "DE", "_id_country": "Germany"},
            "Country: Germany",
            "country=DE",
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
                    "d73d0273-ef94-4951-9c51-c291eba949a0",
                    "c760976f-fd14-4356-9f23-f6eaf084475d",
                ],  #  /PS-IGNORE
            },
            "Regime entry: mtcr-1, wassenaar-1",
            "regime_entry=d73d0273-ef94-4951-9c51-c291eba949a0&regime_entry=c760976f-fd14-4356-9f23-f6eaf084475d",  #  /PS-IGNORE
        ),
        (
            {"control_list_entry": ["ML11a", "MEND2"]},
            "Control list entry: MEND2, ML11a",
            "control_list_entry=ML11a&control_list_entry=MEND2",
        ),
        (
            {"flags": ["798d5e92-c31a-48cc-9e6b-d3fc6dfd65f2", "e50f5cd3-331c-4914-b618-ee6eb67a081c"]},
            "Flags: AG Review Required, BAE",
            "flags=798d5e92-c31a-48cc-9e6b-d3fc6dfd65f2&flags=e50f5cd3-331c-4914-b618-ee6eb67a081c",
        ),
        (
            {"is_trigger_list": True},
            "Is trigger list: True",
            "is_trigger_list=True",
        ),
        (
            {"min_sla_days_remaining": 15},
            "Min sla days remaining: 15",
            "min_sla_days_remaining=15",
        ),
    ],
)
def test_enrich_bookmark_for_display(
    filter_data, bookmark_filter, expected_description, expected_url_params, flags, all_regimes
):
    bookmarks = new_bookmarks(bookmark_filter)

    enricher = BookmarkEnricher(filter_data, flags, all_regimes, "/queues/")
    enriched = enricher.enrich_for_display(bookmarks)

    assert len(enriched) == 1
    assert enriched[0]["description"] == expected_description
    assert enriched[0]["url"] == f"/queues/?{expected_url_params}"


def test_enrich_bookmark_for_display_custom_base_url(filter_data, flags):
    bookmarks = new_bookmarks({"is_trigger_list": True})

    enricher = BookmarkEnricher(filter_data, flags, all_regimes, "/queues/abcd")
    enriched = enricher.enrich_for_display(bookmarks)

    assert len(enriched) == 1
    assert enriched[0]["description"] == "Is trigger list: True"
    assert enriched[0]["url"] == f"/queues/abcd?is_trigger_list=True"


class ObjectToForceException:
    def __str__(self):
        raise Exception("This object breaks when str() called")


def test_enrich_bookmark_for_display_filters_out_errors(filter_data, flags):
    bookmark_filter = {"dodgy_filter_entry": ObjectToForceException()}
    bookmarks = new_bookmarks(bookmark_filter)

    enricher = BookmarkEnricher(filter_data, flags, None, "/queues/")
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
    ],
)
def test_enrich_filter_for_saving(name, filter_data, raw_filters, expected_filter_data):
    actual_filter = enrich_filter_for_saving(filter_data, raw_filters)

    assert sorted(actual_filter.items()) == sorted(expected_filter_data.items())
