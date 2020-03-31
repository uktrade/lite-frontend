from cases.helpers import case_view_breadcrumbs
from lite_content.lite_internal_frontend import cases
from lite_forms.components import Form, Option, Select


def change_status_form(queue, case, statuses):
    return Form(
        title=cases.ChangeStatusPage.TITLE,
        description=cases.ChangeStatusPage.DESCRIPTION,
        questions=[
            Select(
                name="status",
                options=[Option(status["key"], status["value"]) for status in statuses],
                include_default_select=False,
            )
        ],
        back_link=case_view_breadcrumbs(queue, case, cases.ChangeStatusPage.TITLE),
    )
