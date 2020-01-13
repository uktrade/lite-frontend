from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture(scope="function")
def add_a_draft(context, seed_data_config):
    context.draft_id = get_lite_client(context, seed_data_config).create_draft()
