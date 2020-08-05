from http import HTTPStatus

from lite_content.lite_internal_frontend import strings


def validate_query_type_question(_, __, json):
    if json.get("ecju_query_type"):
        return json, HTTPStatus.OK

    return (
        {"errors": {"ecju_query_type": [strings.cases.EcjuQueries.AddQuery.SELECT_A_TYPE]}},
        HTTPStatus.BAD_REQUEST,
    )
