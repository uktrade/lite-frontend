from pytest import fixture

from ..tools.utils import get_lite_client


@fixture(scope="module")
def add_a_generated_document(driver, api_client_config, add_a_document_template, context):
    lite_client = get_lite_client(context, api_client_config)
    lite_client.cases.add_generated_document(context.case_id, context.document_template_id)
