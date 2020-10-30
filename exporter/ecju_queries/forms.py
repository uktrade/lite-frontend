from lite_forms.components import (
    Form,
    HTMLBlock,
    TextArea,
    HiddenField,
    BackLink,
    RadioButtons,
    Select,
    Option,
    Label,
    Button,
    FileUpload,
)
from lite_forms.generators import confirm_form
from lite_content.lite_exporter_frontend import ecju_queries
from exporter.ecju_queries.services import get_ecju_query_document_missing_reasons


def respond_to_query_form(back_link, ecju_query):
    return Form(
        title=ecju_queries.Forms.RespondForm.TITLE,
        questions=[
            HTMLBlock(
                '<div class="app-ecju-query__text" style="display: block; max-width: 100%;">'
                + ecju_query["question"]
                + "</div><br><br>"
            ),
            TextArea(
                name="response",
                title=ecju_queries.Forms.RespondForm.RESPONSE,
                description="",
                extras={
                    "max_length": 2200,
                },
            ),
            HiddenField(name="form_name", value="respond_to_query"),
        ],
        back_link=BackLink(
            ecju_queries.Forms.RespondForm.BACK_LINK,
            back_link,
        ),
    )


def ecju_query_respond_confirmation_form(edit_response_url):
    return confirm_form(
        title=ecju_queries.Forms.ConfirmResponseForm.TITLE,
        confirmation_name="confirm_response",
        hidden_field="ecju_query_response_confirmation",
        yes_label=ecju_queries.Forms.ConfirmResponseForm.YES_LABEL,
        no_label=ecju_queries.Forms.ConfirmResponseForm.NO_LABEL,
        back_link_text=ecju_queries.Forms.ConfirmResponseForm.BACK_LINK,
        back_url=edit_response_url,
        submit_button_text=ecju_queries.Forms.ConfirmResponseForm.SUBMIT_BTN,
    )


def document_grading_form(request, back_link):
    select_options = get_ecju_query_document_missing_reasons(request)[0]["reasons"]
    doc_sensitivity_form = ecju_queries.SupportingDocumentSensitivityForm

    return Form(
        title=doc_sensitivity_form.TITLE,
        description=doc_sensitivity_form.DESCRIPTION,
        questions=[
            RadioButtons(
                name="has_document_to_upload",
                options=[
                    Option(key="yes", value=doc_sensitivity_form.Options.YES),
                    Option(
                        key="no",
                        value=doc_sensitivity_form.Options.NO,
                        components=[
                            Label(text=doc_sensitivity_form.ECJU_HELPLINE),
                            Select(
                                name="missing_document_reason",
                                title=doc_sensitivity_form.LABEL,
                                options=select_options,
                            ),
                        ],
                    ),
                ],
            ),
        ],
        back_link=BackLink(doc_sensitivity_form.BACK_BUTTON, back_link),
        default_button_name=doc_sensitivity_form.SUBMIT_BUTTON,
    )


def upload_documents_form(back_link):
    return Form(
        title=ecju_queries.UploadDocumentForm.TITLE,
        description=ecju_queries.UploadDocumentForm.DESCRIPTION,
        questions=[
            FileUpload(),
            TextArea(
                title=ecju_queries.UploadDocumentForm.Description.TITLE,
                optional=True,
                name="description",
                extras={"max_length": 280},
            ),
        ],
        buttons=[Button(ecju_queries.UploadDocumentForm.BUTTON, "submit")],
        back_link=back_link,
    )
