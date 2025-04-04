from caseworker.cases import services


def get_ecju_queries(request, case_id):
    ecju_queries = services.get_ecju_queries(request, case_id)[0]
    open_ecju_queries = list()
    closed_ecju_queries = list()

    for query in ecju_queries.get("ecju_queries"):
        if query.get("is_query_closed"):
            closed_ecju_queries.append(query)
        else:
            open_ecju_queries.append(query)
    return open_ecju_queries, closed_ecju_queries


def has_open_queries(request, case_id):
    num_open_queries = services.get_ecju_queries_open_count(request, case_id)
    return num_open_queries["count"] > 0


def get_open_ecju_query(request, case_id, query_id):
    open_ecju_queries, _ = get_ecju_queries(request, case_id)
    return _get_query_from_open_queries(open_ecju_queries, query_id)


def _get_query_from_open_queries(open_ecju_queries, query_id):
    for query in open_ecju_queries:
        if query["id"] == str(query_id):
            return query
    return None


def put_ecju_query(request, case_id, query_id, reason_for_closing_query):
    data = {
        "response": reason_for_closing_query,
        "responded_by_user": request.lite_user["id"],
    }
    return services.put_ecju_query(request=request, pk=case_id, query_pk=query_id, json=data)
