from applications.forms.edit import told_by_an_official_form
from apply_for_a_licence.forms import reference_name_form
from conf.constants import STANDARD
from lite_content.lite_exporter_frontend import strings
from django.urls import reverse_lazy

from lite_content.lite_exporter_frontend.applications import ApplicationSuccessPage
from lite_forms.components import HiddenField, Form, BackLink, TextArea, HTMLBlock, RadioButtons, Option, FormGroup
from lite_forms.generators import confirm_form, success_page
from lite_forms.helpers import conditional


def respond_to_query_form(application_id, ecju_query):
    return Form(
        title="Respond to query",
        questions=[
            HTMLBlock(
                '<div class="app-ecju-query__text" style="display: block; max-width: 100%;">'
                + ecju_query["question"]
                + "</div><br><br>"
            ),
            TextArea(name="response", title="Your response", description="", extras={"max_length": 2200,},),
            HiddenField(name="form_name", value="respond_to_query"),
        ],
        back_link=BackLink(
            strings.BACK_TO_APPLICATION,
            reverse_lazy("applications:application", kwargs={"pk": application_id, "type": "ecju-queries"}),
        ),
        default_button_name="Submit",
    )


def ecju_query_respond_confirmation_form(edit_response_url):
    return confirm_form(
        title="Confirm you want to send this response",
        confirmation_name="confirm_response",
        hidden_field="ecju_query_response_confirmation",
        yes_label="Confirm and send the response",
        no_label="Cancel",
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
            strings.BACK_TO_APPLICATION, reverse_lazy("applications:application", kwargs={"pk": application_id}),
        ),
        default_button_name=strings.CONTINUE,
    )


def application_success_page(request, application_reference_code):
    return success_page(
        request=request,
        title=ApplicationSuccessPage.TITLE,
        secondary_title=ApplicationSuccessPage.SECONDARY_TITLE + application_reference_code,
        description=ApplicationSuccessPage.DESCRIPTION,
        what_happens_next=ApplicationSuccessPage.WHAT_HAPPENS_NEXT,
        links={
            ApplicationSuccessPage.VIEW_APPLICATIONS: reverse_lazy("applications:applications"),
            ApplicationSuccessPage.APPLY_AGAIN: reverse_lazy("apply_for_a_licence:start"),
            ApplicationSuccessPage.RETURN_TO_DASHBOARD: reverse_lazy("core:home"),
        },
    )


def application_copy_form(application_type=None):
    return FormGroup(
        forms=[reference_name_form(), conditional((application_type == STANDARD), told_by_an_official_form()),]
    )
