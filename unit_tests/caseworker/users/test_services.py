from caseworker.users.services import convert_users_to_choices, convert_users_to_options
from lite_forms.components import Option


def test_convert_users_to_choices(mock_gov_users):
    result = convert_users_to_choices(mock_gov_users)
    expected = [
        ("1f288b81-2c26-439f-ac32-2a43c8b1a5cb", "joe_1 Williams (MOD-ECJU)"),  # /PS-IGNORE
        ("53a88f67-feda-4975-b0f9-e7689999abd7", "joe_2 smith (MOD-ECJU)"),  # /PS-IGNORE
        ("d832b2fb-e128-4367-9cfe-6f6d37d270f7", "test_3@joebloggs.co.uk"),  # /PS-IGNORE
    ]
    assert result == expected


def test_convert_users_to_options(mock_gov_users):
    result = convert_users_to_options(mock_gov_users)
    expected = [
        Option(
            key="1f288b81-2c26-439f-ac32-2a43c8b1a5cb",  # /PS-IGNORE
            value="joe_1 Williams (MOD-ECJU)",  # /PS-IGNORE
            description="nobody_1@nodomain.com",  # /PS-IGNORE
        ),
        Option(
            key="53a88f67-feda-4975-b0f9-e7689999abd7",  # /PS-IGNORE
            value="joe_2 smith (MOD-ECJU)",  # /PS-IGNORE
            description="nobody@nodomain.com",  # /PS-IGNORE
        ),
        Option(
            key="d832b2fb-e128-4367-9cfe-6f6d37d270f7", value="test_3@joebloggs.co.uk", description=None
        ),  # /PS-IGNORE
    ]
    for i, value in enumerate(expected):
        assert result[i].description == expected[i].description
