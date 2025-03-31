from django import template
from django.urls import reverse
from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag
def show_application_link(application, template="show_application_link.html"):
    application_type = application["case_type"]["sub_type"]["key"]
    is_draft_or_editable = application["status"]["key"] in ["draft", "applicant_editing"]

    link_mapping = {
        ("f680_clearance", True): "f680:summary",
        ("f680_clearance", False): "f680:submitted_summary",
        ("standard", True): "applications:task_list",
        ("standard", False): "applications:application",
    }

    link_url = link_mapping.get((application_type, is_draft_or_editable), None)

    return render_to_string(
        template,
        {
            "link_target": reverse(link_url, kwargs={"pk": application["id"]}) if link_url else "#",
            "application_display_text": application["name"],
        },
    )
