from core.builtins.custom_tags import default_na
from core.helpers import convert_control_list_entries
from lite_forms.components import Summary


def good_summary(good):
    if not good:
        return

    return Summary(
        values={
            "Description": good["description"],
            "Control list entries": convert_control_list_entries(good["control_list_entries"]),
            "Part number": default_na(good["part_number"]),
        },
        classes=["govuk-summary-list--no-border"],
    )
