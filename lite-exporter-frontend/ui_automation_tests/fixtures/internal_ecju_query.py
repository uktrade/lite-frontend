from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture(scope="module")
def internal_ecju_query(driver, context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.add_ecju_query(context.case_id)


@fixture(scope="module")
def internal_ecju_query_end_user_advisory(driver, context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.seed_ecju.add_ecju_query(context.end_user_advisory_id)
