from django.template.defaultfilters import default
from lite_forms.components import Summary


def good_summary(good):
    if not good:
        return

    return Summary(
        values={
            "Description": good["description"],
            "Control list entry": default(good["control_code"], "N/A"),
            "Part number": default(good["part_number"], "N/A"),
        },
        classes=["govuk-summary-list--no-border"],
    )
