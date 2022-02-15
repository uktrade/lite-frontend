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


def test_highlight_results_nested():
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


def test_highlight_results_nested_missing_fields():
    result = {
        "id": "b0c2a113-bb8f-4948-86bd-a5402502434e",
        "reference_code": "GBSIEL/2020/0000105/P",
        "organisation": "Foo bar Ltd",
        "status": "under_final_review",
        "goods": [
            {
                "quantity": 10.0,
                "value": 47000.0,
                "unit": "GRM",
                "item_type": None,
                "incorporated": False,
                "description": "3-(fluoro-methyl-phosphoryl)oxy-2,2-dimethyl-butane",
                "part_number": "",
                "organisation": "Foo bar Ltd",
                "status": "verified",
                "comment": "ARS should be changed to Foo",
                "grading_comment": None,
                "report_summary": "Foo",
                "is_military_use": None,
                "is_pv_graded": "no",
                "is_good_controlled": "yes",
                "item_category": None,
                "control_list_entries": [
                    {
                        "rating": "ML22a",
                        "text": "<b>software</b>",
                        "category": "UK Military List",
                        "parent": {"rating": "ML22", "text": "Military 'technology'"},
                    },
                ],
            },
            {
                "quantity": 0.01,
                "value": 500.0,
                "unit": "LTR",
                "item_type": None,
                "incorporated": False,
                "description": "Atropine sulfate for intravenous injection",
                "part_number": "",
                "organisation": "Foo Ltd",
                "status": "verified",
                "comment": "",
                "grading_comment": None,
                "report_summary": "",
                "is_military_use": None,
                "is_pv_graded": "no",
                "is_good_controlled": "no",
                "item_category": None,
                "control_list_entries": [],
            },
        ],
        "name": "20200429_E2E-00101a",
        "queues": [],
        "highlight": {
            "goods.control_list_entries.text": [
                "<b>software</b>",
            ],
            "wildcard": [
                "<b>software</b>",
            ],
        },
        "score": 17.466608,
    }
    helpers.highlight_results([result])
    assert result["goods"][0]["control_list_entries"][0]["text"] == "<b>software</b>"


def test_highlight_results_nested_dicts():
    result = {
        "id": "300636b1-6cbd-4848-ad09-21a778f8a81e",
        "queues": [],
        "name": "20200224/TL-programme/001",
        "reference_code": "GBSICL/2020/0000002/P",
        "organisation": "Example Ltd",
        "status": "initial_checks",
        "submitted_by": {},
        "case_officer": {"username": None, "email": "foo@example.com"},
        "goods": [
            {
                "quantity": 15.0,
                "value": 20000.0,
                "unit": "NAR",
                "item_type": None,
                "incorporated": True,
                "description": "software",
                "part_number": "DA00001-01A",
                "organisation": "Example Ltd",
                "status": "verified",
                "comment": "",
                "grading_comment": "",
                "report_summary": "General military vehicle components",
                "is_military_use": None,
                "is_pv_graded": "yes",
                "is_good_controlled": "yes",
                "item_category": None,
                "control_list_entries": [],
            }
        ],
        "highlight": {
            "case_officer.email.raw": ["<b>foo@example.com</b>"],
            "goods.description": [
                "<b>software</b>",
            ],
        },
        "score": 108.375305,
    }
    helpers.highlight_results([result])
    assert result["goods"][0]["description"] == "<b>software</b>"

    assert result["case_officer"]["email"] == "<b>foo@example.com</b>"
