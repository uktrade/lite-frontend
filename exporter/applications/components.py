from django.urls import reverse

from lite_content.lite_exporter_frontend import strings
from lite_forms.components import BackLink, Label


def back_to_task_list(application_id):
    if not application_id:
        return BackLink()

    return BackLink(strings.Common.BACK_TO_TASK_LIST, reverse("applications:task_list", kwargs={"pk": application_id}))


def footer_label(application_id):
    url = reverse("applications:task_list", kwargs={"pk": str(application_id)})
    return Label(f'Or <a class="govuk-link" href="{url}">return to application overview</a>')
