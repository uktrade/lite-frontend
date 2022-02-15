from django.urls import reverse_lazy

from lite_content.lite_internal_frontend.cases import UploadEnforcementXML
from lite_content.lite_internal_frontend.strings import cases
from lite_forms.components import Form, TextArea, FileUpload, BackLink


def attach_documents_form(case_url):
    return Form(
        cases.Manage.Documents.AttachDocuments.TITLE,
        cases.Manage.Documents.AttachDocuments.DESCRIPTION,
        [
            FileUpload(),
            TextArea(
                title=cases.Manage.Documents.AttachDocuments.DESCRIPTION_FIELD_TITLE,
                optional=True,
                name="description",
                extras={
                    "max_length": 280,
                },
            ),
        ],
        back_link=BackLink(cases.Manage.Documents.AttachDocuments.BACK_TO_CASE_DOCUMENTS, case_url),
        container="case",
    )


def upload_document_form(queue_pk):
    return Form(
        UploadEnforcementXML.TITLE,
        UploadEnforcementXML.DESCRIPTION,
        [
            FileUpload(name="file"),
        ],
        back_link=BackLink(UploadEnforcementXML.BACK_LINK, reverse_lazy("queues:cases", kwargs={"queue_pk": queue_pk})),
    )
