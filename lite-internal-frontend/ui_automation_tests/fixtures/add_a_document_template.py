from pytest import fixture


@fixture(scope="function")
def add_a_document_template(context, api_test_client):
    document_template = api_test_client.document_templates.add_template(api_test_client.picklists)
    context.document_template_id = document_template["id"]
    context.document_template_name = document_template["name"]
    context.document_template_layout = document_template["layout"]["name"]
    context.document_template_case_types = document_template["case_types"]
    context.document_template_paragraph_text = [document_template["paragraph"]["text"]]


def get_paragraph_text(api_test_client, paragraph_id):
    return api_test_client.document_templates.get_paragraph(paragraph_id)["text"]


@fixture(scope="function")
def get_template_id(api_test_client):
    return api_test_client.document_templates.get_layouts()[0]["id"]


@fixture(scope="function")
def get_licence_template_id(api_test_client):
    return api_test_client.document_templates.get_layouts()[1]["id"]
