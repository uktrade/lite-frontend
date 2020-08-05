from applications.components import back_to_task_list
from core.services import get_f680_clearance_types
from lite_content.lite_exporter_frontend.goods import F680Details

from lite_forms.components import Form, Checkboxes, Option


def f680_details_form(request, application_id):
    return Form(
        title=F680Details.TITLE,
        description=F680Details.DESCRIPTION,
        questions=[
            Checkboxes(
                name="types[]",
                options=[Option(key, value) for key, value in get_f680_clearance_types(request).items()],
            ),
        ],
        default_button_name=F680Details.BUTTON,
        back_link=back_to_task_list(application_id),
    )
