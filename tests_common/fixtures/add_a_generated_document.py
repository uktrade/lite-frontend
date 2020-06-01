from pytest import fixture


@fixture(scope="function")
def add_a_generated_document(api_test_client, add_a_document_template, context):
    api_test_client.cases.add_generated_document(context.case_id, context.document_template_id)
