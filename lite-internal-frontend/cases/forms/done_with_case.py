from cases.services import get_user_case_queues
from lite_content.lite_internal_frontend.cases import DoneWithCaseOnQueueForm
from lite_forms.components import Form, Option, Checkboxes


def done_with_case_form(request, case_pk):
    queues, _ = get_user_case_queues(request, case_pk)

    return Form(
        title=DoneWithCaseOnQueueForm.TITLE,
        questions=[
            Checkboxes(
                name="queues[]",
                options=[Option(queue["id"], queue["name"]) for queue in queues["queues"]],
                title=DoneWithCaseOnQueueForm.CHECKBOX_TITLE,
                description=DoneWithCaseOnQueueForm.CHECKBOX_DESCRIPTION,
                optional=False,
            )
        ],
        default_button_name=DoneWithCaseOnQueueForm.SUBMIT,
    )
