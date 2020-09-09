from caseworker.search import helpers


def test_highlight_results_raw():
    result = {
        "id": "foo",
        "reference_code": "GBOIEL/2020/0000003/P",
        "organisation": "Foo Communications",
        "status": "under_final_review",
        "goods": [],
        "parties": [
            {
                "name": "Foo Example",
                "address": "31964 Fake street",
                "type": "ultimate_end_user",
                "country": "United Kingdom",
            }
        ],
        "name": "e-enable turn-key schemas",
        "queues": [],
        "highlight": {"organisation.raw": ["<b>Foo Communications</b>"]},
        "score": 0.0,
    }
    helpers.highlight_results([result])
    assert result["organisation"] == "<b>Foo Communications</b>"


def test_highlight_results_raw():
    result = {
        "id": "4e689a94-5fa0-47fd-b012-3f972c8d09a7",
        "reference_code": "EXHC/2020/0000022",
        "organisation": "Foo Communications",
        "status": "submitted",
        "goods": [
            {
                "quantity": None,
                "value": None,
                "unit": None,
                "item_type": "video",
                "incorporated": None,
                "description": "Lentils",
                "part_number": "1234",
                "organisation": "Foo Communications",
                "status": "submitted",
                "comment": None,
                "grading_comment": None,
                "report_summary": None,
                "is_military_use": None,
                "is_pv_graded": "no",
                "is_good_controlled": "yes",
                "item_category": None,
                "control_list_entries": [
                    {
                        "rating": "ML1a",
                        "text": "<b>Rifles</b> and combination guns, handguns, machine, sub-machine and volley guns",
                        "category": "UK Military List",
                        "parent": {
                            "rating": "ML1",
                            "text": "Smooth-bore weapons with a calibre of less than 20mm, other firearms and",
                        },
                    },
                    {
                        "rating": "ML2a",
                        "text": "<b>Rifles</b> and combination guns, handguns, machine, sub-machine and volley guns",
                        "category": "UK Military List",
                        "parent": {
                            "rating": "ML1",
                            "text": "Smooth-bore weapons with a calibre of less than 20mm, other firearms and",
                        },
                    },
                ],
            }
        ],
        "parties": [],
        "name": "deliver distributed schemas",
        "queues": [],
        "highlight": {
            "goods.control_list_entries.text": [
                "<b>Rifles</b> and combination guns, handguns, machine, sub-machine and volley guns"
            ],
            "wildcard": ["<b>Rifles</b> and combination guns, handguns, machine, sub-machine and volley guns"],
        },
        "score": 1.9518821,
    }
    helpers.highlight_results([result])
    assert result["goods"][0]["control_list_entries"][0]["text"] == (
        "<b>Rifles</b> and combination guns, handguns, machine, sub-machine and volley guns"
    )
    assert result["goods"][0]["control_list_entries"][1]["text"] == (
        "<b>Rifles</b> and combination guns, handguns, machine, sub-machine and volley guns"
    )
