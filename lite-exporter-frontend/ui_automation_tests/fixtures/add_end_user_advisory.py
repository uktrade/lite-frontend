from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture(scope="module")
def add_end_user_advisory(driver, request, context, exporter_url, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.seed_party.add_eua_query()
    context.end_user_advisory_id = lite_client.context["end_user_advisory_id"]
