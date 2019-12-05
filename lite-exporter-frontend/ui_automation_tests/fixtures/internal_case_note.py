from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture(scope="module")
def internal_case_note(context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.seed_case.add_case_note(context, context.case_id)


@fixture(scope="module")
def internal_case_note_end_user_advisory(context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.seed_case.add_case_note(context, context.end_user_advisory_id)
