from django.urls import reverse_lazy

from core.builtins.custom_tags import default_na
from core.constants import (
    CaseStatusEnum,
    SerialChoices,
)

from lite_forms.components import Summary

from core.constants import ProductCategories

from exporter.core.constants import FIREARM_AMMUNITION_COMPONENT_TYPES
from exporter.core.helpers import convert_control_list_entries


def good_summary(good):
    if not good:
        return

    values = {
        "Name": good["description"] if not good["name"] else good["name"],
        "Control list entries": convert_control_list_entries(good["control_list_entries"]),
        "Part number": default_na(good["part_number"]),
    }

    if good["item_category"]["key"] == ProductCategories.PRODUCT_CATEGORY_FIREARM:
        firearm_type = good["firearm_details"]["type"]["key"]

        if firearm_type in FIREARM_AMMUNITION_COMPONENT_TYPES:
            values["Number of items"] = str(good["firearm_details"].get("number_of_items"))

    return Summary(
        values=values,
        classes=["govuk-summary-list--no-border"],
    )


COMPONENT_SELECTION_TO_DETAIL_FIELD_MAP = {
    "yes_designed": "designed_details",
    "yes_modified": "modified_details",
    "yes_general": "general_details",
}


ITEM_CATEGORY_TO_DISPLAY_STRING_MAP = {
    "group3_software": "software",
    "group3_technology": "technology",
    "software_related_to_firearms": "software",
    "technology_related_to_firearms": "technology",
}


def get_category_display_string(category):
    if category in ITEM_CATEGORY_TO_DISPLAY_STRING_MAP.keys():
        return ITEM_CATEGORY_TO_DISPLAY_STRING_MAP[category]
    return ""


def return_to_good_summary(kwargs, application_id, object_pk):
    if "good_pk" in kwargs:
        return reverse_lazy("applications:add_good_summary", kwargs={"pk": application_id, "good_pk": object_pk})
    else:
        return reverse_lazy("goods:good", kwargs={"pk": object_pk})


def is_firearms_act_status_changed(initial, updated):
    if (
        initial["is_covered_by_firearm_act_section_one_two_or_five"] == "Yes"
        and updated["is_covered_by_firearm_act_section_one_two_or_five"] == "Yes"
    ) and initial["firearms_act_section"] != updated["firearms_act_section"]:
        return True

    if (
        initial["is_covered_by_firearm_act_section_one_two_or_five"] == "Yes"
        and updated["is_covered_by_firearm_act_section_one_two_or_five"] != "Yes"
    ):
        return True

    return False


def requires_serial_numbers(application, good_on_application):
    if application["status"]["key"] not in [
        CaseStatusEnum.SUBMITTED,
        CaseStatusEnum.FINALISED,
    ]:
        return False

    firearm_details = good_on_application.get("firearm_details")
    if not firearm_details:
        return False

    if firearm_details["serial_numbers_available"] == SerialChoices.NOT_AVAILABLE:
        return False

    serial_numbers = firearm_details["serial_numbers"]
    added_serial_numbers = [sn for sn in serial_numbers if sn]
    number_of_items = firearm_details["number_of_items"]

    return number_of_items != len(added_serial_numbers)
