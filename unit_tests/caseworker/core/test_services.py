from caseworker.core.services import group_denial_reasons


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
