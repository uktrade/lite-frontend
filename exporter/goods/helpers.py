from django.urls import reverse_lazy

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


COMPONENT_SELECTION_TO_DETAIL_FIELD_MAP = {
    "yes_designed": "designed_details",
    "yes_modified": "modified_details",
    "yes_general": "general_details",
}


ITEM_CATEGORY_TO_DISPLAY_STRING_MAP = {"group3_software": "software", "group3_technology": "technology"}


def get_category_display_string(category):
    if category in ITEM_CATEGORY_TO_DISPLAY_STRING_MAP.keys():
        return ITEM_CATEGORY_TO_DISPLAY_STRING_MAP[category]
    return ""


def return_to_good_summary(kwargs, application_id, object_pk):
    if "good_pk" in kwargs:
        return reverse_lazy("applications:add_good_summary", kwargs={"pk": application_id, "good_pk": object_pk})
    else:
        return reverse_lazy("goods:good", kwargs={"pk": object_pk})
