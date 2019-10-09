from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture(scope='function')
def add_clc_query(driver, request, context, exporter_url, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.seed_clc.add_clc_good(lite_client.seed_good, lite_client.seed_ecju)
    context.clc_good_id = lite_client.context['clc_good_id']
