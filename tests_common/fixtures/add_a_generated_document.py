from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture(scope="module")
def add_a_generated_document(
    driver, seed_data_config, add_a_document_template, context,
):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.seed_case.add_generated_document(context.case_id, context.document_template_id)
