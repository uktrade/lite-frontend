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
