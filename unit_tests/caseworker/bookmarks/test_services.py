import json
import uuid

import pytest

from caseworker.bookmarks.services import description_from_filter, enhance_bookmark
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
    ],
)
def test_enhance_bookmark(filter_data, bookmark_filter, expected_description, expected_url_params):
    bookmark = {"name": "Name", "description": "", "filter_json": json.dumps(bookmark_filter), "id": uuid.uuid4()}

    enhance_bookmark(bookmark, filter_data)

    assert bookmark["description"] == expected_description
    assert bookmark["url"] == f"/queues/?{expected_url_params}"
