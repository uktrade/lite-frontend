from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse


register = template.Library()


@register.simple_tag
def show_application_link(application, template="application_link.html"):
    is_f680_application = application["case_type"]["sub_type"]["key"] == "f680_clearance"
    is_draft_or_editiable = (
        application["status"]["key"] == "draft" or application["status"]["key"] == "applicant_editing"
    )
    application_display_text = application["name"]

    if is_f680_application and is_draft_or_editiable:
        link_target = reverse("f680:summary", kwargs={"pk": application["id"]})
    elif is_f680_application and not is_draft_or_editiable:
        link_target = "#"
    elif not is_f680_application and is_draft_or_editiable:
        link_target = reverse("applications:task_list", kwargs={"pk": application["id"]})
    else:
        link_target = reverse("applications:application", kwargs={"pk": application["id"]})

    return mark_safe( # /PS-IGNORE
        f'<a class="govuk-link govuk-link--no-visited-state app-icon-label" href="{link_target}">{application_display_text}</a>'
    )
