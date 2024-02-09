import pytest


from caseworker.cases.forms.queries import CloseQueryForm


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"reason_for_closing_query": ["Enter a reason why you are closing the query"]}),
        (
            {"reason_for_closing_query": ""},
            False,
            {"reason_for_closing_query": ["Enter a reason why you are closing the query"]},
        ),
        ({"reason_for_closing_query": "closing response"}, True, {}),
    ),
)
def test_ecju_queries_close_query_form(data, is_valid, errors):
    form = CloseQueryForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors
