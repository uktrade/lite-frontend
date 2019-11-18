from django.urls import reverse_lazy
from lite_forms.components import BackLink, Label
from core.builtins.custom_tags import get_string


def back_to_task_list(application_id):
    return BackLink(
        get_string("common.back_to_task_list"), reverse_lazy("applications:task_list", kwargs={"pk": application_id})
    )


def footer_label(application_id):
    return Label(
        'Or <a class="govuk-link" href="'
        + reverse_lazy("applications:task_list", kwargs={"pk": str(application_id)})
        + '">Or return to the task list</a>'
    )
