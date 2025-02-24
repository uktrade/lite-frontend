from django import template
from django.urls import reverse, NoReverseMatch
from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag
def show_application_link(application, template="show_application_link.html"):
    application_type = application["case_type"]["sub_type"]["key"]
    is_draft_or_editable = application["status"]["key"] in ["draft", "applicant_editing"]

    destination = "task_list" if is_draft_or_editable else "application"

    breakpoint()
    try:
        url = reverse(f"{application_type}:{destination}", kwargs={"pk": application["id"]})
    except NoReverseMatch:
        raise Exception(f"You need to create a view with the url {application_type}:{destination}")

    return render_to_string(
        template,
        {
            "link_target": url,
            "application_display_text": application["name"],
        },
    )
