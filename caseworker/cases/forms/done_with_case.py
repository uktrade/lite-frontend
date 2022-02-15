from caseworker.cases.services import get_user_case_queues
from lite_content.lite_internal_frontend.cases import DoneWithCaseOnQueueForm
from lite_forms.components import Form, Option, Checkboxes, DetailComponent, TextArea, HiddenField
from lite_forms.helpers import conditional
from caseworker.queues.services import get_queue


def done_with_case_form(request, queue_pk, case_pk, has_review_date):
    queue = None
    queues, _ = get_user_case_queues(request, case_pk)

    if not queues:
        queue = get_queue(request, queue_pk)

    return Form(
        title=DoneWithCaseOnQueueForm.TITLE
        if not queue
        else DoneWithCaseOnQueueForm.TITLE_SINGULAR.format(queue["name"]),
        questions=[
            conditional(
                queues,
                Checkboxes(
                    name="queues[]",
                    options=[Option(queue["id"], queue["name"]) for queue in queues],
                    title=DoneWithCaseOnQueueForm.CHECKBOX_TITLE,
                    description=DoneWithCaseOnQueueForm.CHECKBOX_DESCRIPTION,
                ),
                HiddenField(name="queues[]", value=queue_pk),
            ),
            DetailComponent(
                title=DoneWithCaseOnQueueForm.NOTE,
                components=[
                    TextArea(name="note", classes=["govuk-!-margin-0"]),
                ],
            ),
        ],
        default_button_name=DoneWithCaseOnQueueForm.SUBMIT,
        container="case",
        javascript_imports=conditional(has_review_date, {"/javascripts/assign_queue.js"}, None),
    )
