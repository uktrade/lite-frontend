import pytest

from caseworker.tau.utils import get_cle_suggestions_json


@pytest.mark.parametrize(
    "good_on_applications,json",
    (
        (
            [
                {
                    "id": "good-id-1",
                    "good": {
                        "name": "Good 1",
                        "control_list_entries": [
                            {"rating": "R1"},
                            {"rating": "R1a"},
                        ],
                    },
                    "precedents": [],
                },
                {
                    "id": "good-id-2",
                    "good": {
                        "name": "Good 2",
                        "control_list_entries": [
                            {"rating": "R2"},
                            {"rating": "R2a"},
                        ],
                    },
                    "precedents": [],
                },
            ],
            [
                {
                    "id": "good-id-1",
                    "name": "Good 1",
                    "controlListEntries": {
                        "exporter": ["R1", "R1a"],
                        "precedents": [],
                    },
                },
                {
                    "id": "good-id-2",
                    "name": "Good 2",
                    "controlListEntries": {
                        "exporter": ["R2", "R2a"],
                        "precedents": [],
                    },
                },
            ],
        ),
        (
            [
                {
                    "id": "good-id-1",
                    "good": {
                        "name": "Good 1",
                        "control_list_entries": [
                            {"rating": "R1"},
                            {"rating": "R1a"},
                        ],
                    },
                    "precedents": [
                        {
                            "control_list_entries": ["S1", "S1a"],
                        },
                        {
                            "control_list_entries": ["T1", "T1a"],
                        },
                    ],
                },
                {
                    "id": "good-id-2",
                    "good": {
                        "name": "Good 2",
                        "control_list_entries": [
                            {"rating": "R2"},
                            {"rating": "R2a"},
                        ],
                    },
                    "precedents": [],
                },
            ],
            [
                {
                    "id": "good-id-1",
                    "name": "Good 1",
                    "controlListEntries": {
                        "exporter": [],
                        "precedents": [
                            ["S1", "S1a"],
                            ["T1", "T1a"],
                        ],
                    },
                },
                {
                    "id": "good-id-2",
                    "name": "Good 2",
                    "controlListEntries": {
                        "exporter": ["R2", "R2a"],
                        "precedents": [],
                    },
                },
            ],
        ),
    ),
)
def test_get_cle_suggestions_json(good_on_applications, json):
    assert get_cle_suggestions_json(good_on_applications) == json
