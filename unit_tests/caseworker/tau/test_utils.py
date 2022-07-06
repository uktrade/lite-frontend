from caseworker.tau.utils import get_cle_suggestions_json


def test_get_cle_suggestions_json():
    good_on_application_list = [
        {
            "id": "good-id-1",
            "good": {
                "name": "Good 1",
                "control_list_entries": ["R1", "R1a"],
            },
        },
        {
            "id": "good-id-2",
            "good": {
                "name": "Good 2",
                "control_list_entries": ["R2", "R2a"],
            },
        },
    ]

    assert get_cle_suggestions_json(good_on_application_list) == [
        {
            "id": "good-id-1",
            "name": "Good 1",
            "controlListEntries": {
                "exporter": ["R1", "R1a"],
            },
        },
        {
            "id": "good-id-2",
            "name": "Good 2",
            "controlListEntries": {
                "exporter": ["R2", "R2a"],
            },
        },
    ]
