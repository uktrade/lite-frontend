from django import template
from django.urls import reverse
from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag
def show_application_link(application, template="show_application_link.html"):
    is_f680_application = application["case_type"]["sub_type"]["key"] == "f680_clearance"
    is_draft_or_editiable = (
        application["status"]["key"] == "draft" or application["status"]["key"] == "applicant_editing"
    )

    link_mapping = {
        (True, True): "f680:summary",
        (False, True): "applications:task_list",
        (False, False): "applications:application",
    }

    link_url = link_mapping.get((is_f680_application, is_draft_or_editiable), None)

    return render_to_string(
        template,
        {
            "link_target": reverse(link_url, kwargs={"pk": application["id"]}) if link_url else "#",
            "application_display_text": application["name"],
        },
    )
