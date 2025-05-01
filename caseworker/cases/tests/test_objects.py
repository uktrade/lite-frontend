from caseworker.cases.objects import Case


def test_case_object_properties(data_standard_case):
    case = Case(data_standard_case["case"])
    assert case.organisation["primary_site"]["name"] == "Systems Ltd"
    assert case.status == "submitted"
    assert case.type == "application"
    assert case.sub_type == "standard"
    assert case.reference == "siel"
    assert case.amendment_of_url == ""
    assert case.superseded_by_url == ""
