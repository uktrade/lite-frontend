from lite_content.lite_exporter_frontend import strings
from django.urls import reverse_lazy

from lite_forms.components import HiddenField, Form, BackLink, TextArea, HTMLBlock, RadioButtons, Option
from lite_forms.generators import confirm_form, success_page


def respond_to_query_form(application_id, ecju_query):
    return Form(
        title="Respond to query",
        questions=[
            HTMLBlock(
                '<div class="app-ecju-query__text" style="display: block; max-width: 100%;">'
                + ecju_query["question"]
                + "</div><br><br>"
            ),
            TextArea(
                name="response",
                title="Your response",
                description="You won't be able to edit this once you've submitted it.",
                extras={"max_length": 2200,},
            ),
            HiddenField(name="form_name", value="respond_to_query"),
        ],
        back_link=BackLink(
            strings.BACK_TO_APPLICATION,
            reverse_lazy("applications:application", kwargs={"pk": application_id, "type": "ecju-queries"}),
        ),
        default_button_name="Submit response",
    )


def ecju_query_respond_confirmation_form(edit_response_url):
    return confirm_form(
        title="Are you sure you want to send this response?",
        confirmation_name="confirm_response",
        hidden_field="ecju_query_response_confirmation",
        yes_label="Yes, send the response",
        no_label="No, change my response",
        back_link_text="Back to edit response",
        back_url=edit_response_url,
        submit_button_text=strings.CONTINUE,
    )


def edit_type_form(application_id):
    return Form(
        title=strings.Applications.Edit.TITLE,
        description=strings.Applications.Edit.DESCRIPTION,
        questions=[
            RadioButtons(
                name="edit-type",
                options=[
                    Option(
                        key="minor",
                        value=strings.Applications.Edit.Minor.TITLE,
                        description=strings.Applications.Edit.Minor.DESCRIPTION,
                    ),
                    Option(
                        key="major",
                        value=strings.Applications.Edit.Major.TITLE,
                        description=strings.Applications.Edit.Major.DESCRIPTION,
                    ),
                ],
            )
        ],
        back_link=BackLink(
            strings.BACK_TO_APPLICATION,
            reverse_lazy("applications:application", kwargs={"pk": application_id, "type": "ecju-queries"}),
        ),
        default_button_name=strings.CONTINUE,
    )


def application_success_page(request, application_id):
    return success_page(
        request=request,
        title="Application sent successfully",
        secondary_title="Your reference code: " + application_id,
        description="",
        what_happens_next=["You'll receive an email from DIT when your check is finished."],
        links={
            "View your list of applications": reverse_lazy("applications:applications"),
            "Apply for another export licence": reverse_lazy("apply_for_a_licence:start"),
            "Return to Exporter Hub": reverse_lazy("core:hub"),
        },
    )
