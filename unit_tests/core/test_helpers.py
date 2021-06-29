import pytest
from core.helpers import convert_parameters_to_query_params, format_date


def test_convert_parameters_to_query_params():
    params = {"request": "request", "org_type": ["individual", "commercial"], "page": 1, "empty": None}

    assert convert_parameters_to_query_params(params) == "?org_type=individual&org_type=commercial&page=1"


@pytest.mark.parametrize(
    "data,formatted",
    [
        ({"fieldnameday": "01", "fieldnamemonth": "01", "fieldnameyear": "2020",}, "2020-01-01"),
        ({"fieldnameday": "1", "fieldnamemonth": "1", "fieldnameyear": "2020",}, "2020-01-01"),
        ({"fieldnameday": None, "fieldnamemonth": "01", "fieldnameyear": "2020",}, None),
        ({"fieldnameday": "01", "fieldnamemonth": None, "fieldnameyear": "2020",}, None),
        ({"fieldnameday": "01", "fieldnamemonth": "01", "fieldnameyear": None,}, None),
        ({"fieldnameday": None, "fieldnamemonth": None, "fieldnameyear": None,}, None),
    ],
)
def test_format_date(data, formatted):
    assert format_date(data, "fieldname") == formatted
