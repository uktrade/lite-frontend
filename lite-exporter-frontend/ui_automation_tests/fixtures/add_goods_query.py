from pytest import fixture


@fixture(scope="function")
def add_goods_clc_query(context, api_test_client):
    api_test_client.goods_queries.add_clc_good(api_test_client.goods, api_test_client.ecju_queries)
    context.goods_query_good_id = api_test_client.context["goods_query_good_id"]
