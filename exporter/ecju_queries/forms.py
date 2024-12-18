from lite_forms.components import (
    Form,
    HTMLBlock,
    TextArea,
    HiddenField,
    BackLink,
    Button,
    FileUpload,
)
from lite_forms.generators import confirm_form
from lite_content.lite_exporter_frontend import ecju_queries


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
                extras={"max_length": 2200},
            ),
            HiddenField(name="form_name", value="respond_to_query"),
        ],
        back_link=BackLink(ecju_queries.Forms.RespondForm.BACK_LINK, back_link),
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


def upload_documents_form(back_link):
    return Form(
        title=ecju_queries.UploadDocumentForm.TITLE,
        description="Do not attach a document that's above OFFICIAL-SENSITIVE.<br><br>The file must be smaller than 50MB.",
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
