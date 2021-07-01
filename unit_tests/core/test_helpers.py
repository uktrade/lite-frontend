from core.helpers import convert_parameters_to_query_params


def test_convert_parameters_to_query_params():
    params = {"request": "request", "org_type": ["individual", "commercial"], "page": 1, "empty": None}

    assert convert_parameters_to_query_params(params) == "?org_type=individual&org_type=commercial&page=1"
