from lite_content.lite_internal_frontend.cases import GenerateDocumentsPage
from lite_forms.generators import error_page


def generate_document_error_page():
    return error_page(
        None,
        title=GenerateDocumentsPage.TITLE,
        description=GenerateDocumentsPage.ERROR,
        show_back_link=True,
    )
