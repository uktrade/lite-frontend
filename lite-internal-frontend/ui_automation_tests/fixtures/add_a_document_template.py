from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture(scope="module")
def add_a_document_template(context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config)
    document_template = lite_client.seed_document_template.add_template(lite_client.seed_picklist)
    context.document_template_id = document_template["id"]
    context.document_template_name = document_template["name"]
    context.document_template_layout = document_template["layout"]["name"]
    context.document_template_case_types = [document_template["case_types"][0]]
    context.document_template_paragraph_text = [document_template["paragraph"]["text"]]


def get_paragraph_text(context, seed_data_config, paragraph_id):
    lite_client = get_lite_client(context, seed_data_config)
    return lite_client.seed_document_template.get_paragraph(paragraph_id)["text"]


@fixture(scope="session")
def get_template_id(context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config)
    return lite_client.seed_document_template.get_layouts()[0]["id"]


@fixture(scope="session")
def get_licence_template_id(context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config)
    return lite_client.seed_document_template.get_layouts()[1]["id"]
