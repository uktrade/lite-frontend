from cases.services import get_user_case_queues
from lite_content.lite_internal_frontend.cases import DoneWithCaseOnQueueForm
from lite_forms.components import Form, Option, Checkboxes, DetailComponent, TextArea
from lite_forms.helpers import conditional


def done_with_case_form(request, case_pk, has_review_date):
    queues, _ = get_user_case_queues(request, case_pk)

    return Form(
        title=DoneWithCaseOnQueueForm.TITLE,
        questions=[
            Checkboxes(
                name="queues[]",
                options=[Option(queue["id"], queue["name"]) for queue in queues],
                title=DoneWithCaseOnQueueForm.CHECKBOX_TITLE,
                description=DoneWithCaseOnQueueForm.CHECKBOX_DESCRIPTION,
            ),
            DetailComponent(
                title=DoneWithCaseOnQueueForm.NOTE, components=[TextArea(name="note", classes=["govuk-!-margin-0"]),],
            ),
        ],
        default_button_name=DoneWithCaseOnQueueForm.SUBMIT,
        container="case",
        javascript_imports=conditional(has_review_date, {"/javascripts/assign_queue.js"}, None),
    )
