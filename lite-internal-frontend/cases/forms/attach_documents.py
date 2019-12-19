from lite_content.lite_internal_frontend import strings
from lite_forms.components import Form, TextArea, FileUpload, BackLink


def attach_documents_form(case_url):
    return Form(
        strings.Cases.Manage.Documents.AttachDocuments.TITLE,
        strings.Cases.Manage.Documents.AttachDocuments.DESCRIPTION,
        [
            FileUpload("documents"),
            TextArea(
                title=strings.Cases.Manage.Documents.AttachDocuments.DESCRIPTION_FIELD_TITLE,
                optional=True,
                name="description",
                extras={"max_length": 280,},
            ),
        ],
        back_link=BackLink(strings.Cases.Manage.Documents.AttachDocuments.BACK_TO_CASE_DOCUMENTS, case_url),
    )
