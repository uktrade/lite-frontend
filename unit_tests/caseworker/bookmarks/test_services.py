import json
import uuid
from collections import OrderedDict

import pytest

from caseworker.bookmarks.services import description_from_filter, enrich_bookmark_for_display, enrich_filter_for_saving
from unit_tests.caseworker.conftest import GOV_USER_ID


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
def test_description_from_filter(filter_data, bookmark_filter, expected_description):
    description = description_from_filter(bookmark_filter, filter_data)
    assert description == expected_description


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
                "regime_entry": "2594daef-8156-4e78-b4c4-e25f6cdbd203",
                "_id_regime_entry": "Wassenaar Arrangement Sensitive",
            },
            "Regime entry: Wassenaar Arrangement Sensitive",
            "regime_entry=2594daef-8156-4e78-b4c4-e25f6cdbd203",
        ),
    ],
)
def test_enrich_bookmark_for_display(filter_data, bookmark_filter, expected_description, expected_url_params):
    bookmark = {"name": "Name", "description": "", "filter_json": bookmark_filter, "id": uuid.uuid4()}

    enrich_bookmark_for_display(bookmark, filter_data)

    assert bookmark["description"] == expected_description
    assert bookmark["url"] == f"/queues/?{expected_url_params}"


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
