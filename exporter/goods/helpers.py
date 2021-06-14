from django.urls import reverse_lazy

from core.helpers import format_date
from core.builtins.custom_tags import default_na
from exporter.core.constants import PRODUCT_CATEGORY_FIREARM, FIREARM_AMMUNITION_COMPONENT_TYPES
from exporter.core.helpers import convert_control_list_entries
from lite_forms.components import Summary


def good_summary(good):
    if not good:
        return

    values = {
        "Name": good["description"] if not good["name"] else good["name"],
        "Control list entries": convert_control_list_entries(good["control_list_entries"]),
        "Part number": default_na(good["part_number"]),
    }

    if good["item_category"]["key"] == PRODUCT_CATEGORY_FIREARM:
        firearm_type = good["firearm_details"]["type"]["key"]

        if firearm_type in FIREARM_AMMUNITION_COMPONENT_TYPES:
            values["Number of items"] = str(good["firearm_details"].get("number_of_items"))

    return Summary(values=values, classes=["govuk-summary-list--no-border"],)


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


def get_sporting_shotgun_form_title(product_type):
    if product_type == "firearms":
        return "Is the product a sporting shotgun?"
    elif product_type == "ammunition":
        return "Is the product sporting shotgun ammunition?"
    elif product_type == "components_for_firearms":
        return "Is the product a component of a sporting shotgun?"
    elif product_type == "components_for_ammunition":
        return "Is the product a component of sporting shotgun ammunition?"


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


def serialize_goods_data(request, json):
    json["item_category"] = json.get("item_category", "group2_firearms")

    if "is_pv_graded" in json and json["is_pv_graded"] == "yes":
        if "reference" in json:
            json["pv_grading_details"] = {
                "grading": json["grading"],
                "custom_grading": json["custom_grading"],
                "prefix": json["prefix"],
                "suffix": json["suffix"],
                "issuing_authority": json["issuing_authority"],
                "reference": json["reference"],
                "date_of_issue": format_date(json, "date_of_issue"),
            }

    if "item_category" in json and json["item_category"] == "group2_firearms":
        add_firearm_details_to_data(request, json)


def add_section_certificate_details(firearm_details, json):
    if "section_certificate_step" in json:
        firearm_details["is_covered_by_firearm_act_section_one_two_or_five"] = json.get(
            "is_covered_by_firearm_act_section_one_two_or_five", ""
        )
        firearm_details["firearms_act_section"] = json.get("firearms_act_section", "")
    if "firearms_certificate_uploaded" in json:
        certificate_missing = json.get("section_certificate_missing", False)
        if not certificate_missing:
            firearm_details["section_certificate_number"] = json.get("section_certificate_number")
            formatted_section_certificate_date = format_date(json, "section_certificate_date_of_expiry")
            firearm_details["section_certificate_date_of_expiry"] = (
                formatted_section_certificate_date if formatted_section_certificate_date != "--" else None
            )
            firearm_details["section_certificate_missing"] = False
            firearm_details["section_certificate_missing_reason"] = ""
        else:
            firearm_details["section_certificate_missing"] = True
            firearm_details["section_certificate_missing_reason"] = json.get("section_certificate_missing_reason", "")
            firearm_details["section_certificate_number"] = ""


def add_identification_marking_details(firearm_details, json):
    if "number_of_items_step" in json:
        try:
            firearm_details["number_of_items"] = int(json.get("number_of_items"))
        except ValueError:
            firearm_details["number_of_items"] = 0

    if "identification_markings_step" in json:
        # parent component doesnt get sent when empty unlike the remaining form fields
        firearm_details["has_identification_markings"] = json.get("has_identification_markings", "")
        firearm_details["no_identification_markings_details"] = json.get("no_identification_markings_details")
        del json["no_identification_markings_details"]

    if "capture_serial_numbers_step" in json:
        try:
            number_of_items = int(json.get("number_of_items"))
        except ValueError:
            number_of_items = 0

        serial_numbers = []
        for i in range(number_of_items):
            serial_numbers.append(json.get(f"serial_number_input_{i}", ""))
        firearm_details["serial_numbers"] = serial_numbers


def add_rfd_certificate_details(firearm_details, json, request):
    if "firearms_dealer_certificate_step" in json:
        firearm_details["document_on_organisation"] = {
            "expiry_date": format_date(json, "expiry_date_"),
            "reference_code": json["reference_code"],
            "document_type": "rfd-certificate",
            "document": request.session.get("rfd_certificate", None),
        }


def add_rfd_details(firearm_details, json):
    if "registered_firearm_dealer_step" in json:
        firearm_details["is_registered_firearm_dealer"] = json.get("is_registered_firearm_dealer")
    elif firearm_details and "is_registered_firearm_dealer" not in firearm_details:
        firearm_details["is_registered_firearm_dealer"] = False


def add_sporting_shotgun_details(firearm_details, json):
    if "sporting_shotgun_step" in json:
        firearm_details["type"] = json.get("type")
        firearm_details["is_sporting_shotgun"] = json.get("is_sporting_shotgun")
    elif firearm_details and "is_sporting_shotgun" not in firearm_details:
        firearm_details["is_sporting_shotgun"] = False


def add_year_of_manufacture_details(firearm_details, json):
    if "firearm_year_of_manufacture_step" in json:
        firearms_year_of_manufacture = json.pop("year_of_manufacture")
        if firearms_year_of_manufacture == "":
            firearms_year_of_manufacture = None
        firearm_details["year_of_manufacture"] = firearms_year_of_manufacture
    elif firearm_details and "year_of_manufacture" not in firearm_details:
        firearm_details["year_of_manufacture"] = 0


def add_replica_details(firearm_details, json):
    if "is_replica_step" in json:
        firearm_details["type"] = json.get("type")
        firearm_details["is_replica"] = json.get("is_replica")
        firearm_details["replica_description"] = json.get("replica_description", "")
        del json["replica_description"]


def add_calibre_details(firearm_details, json):
    if "firearm_calibre_step" in json:
        firearm_calibre = json.pop("calibre")
        if firearm_calibre == "":
            firearm_calibre = None
        firearm_details["calibre"] = firearm_calibre


def add_product_type(firearm_details, json):
    if "product_type_step" in json:
        # parent component doesnt get sent when empty unlike the remaining form fields
        firearm_details["type"] = json.get("type")


def add_firearm_details_to_data(request, json):
    """
    Return a firearm_details dictionary to be used when creating/editing a group 2 firearm good
    Mutable - items in firearm_details are removed from the original json (duplicates)
    """
    firearm_details = {}

    add_product_type(firearm_details, json)

    add_rfd_certificate_details(firearm_details, json, request)

    add_sporting_shotgun_details(firearm_details, json)

    add_rfd_details(firearm_details, json)

    add_identification_marking_details(firearm_details, json)

    add_year_of_manufacture_details(firearm_details, json)

    add_replica_details(firearm_details, json)

    add_calibre_details(firearm_details, json)

    add_section_certificate_details(firearm_details, json)

    for name in [
        "date_of_deactivation",
        "has_proof_mark",
        "no_proof_mark_details",
        "is_deactivated",
        "deactivation_standard",
        "deactivation_standard_other",
        "is_deactivated_to_standard",
    ]:
        if name in json:
            firearm_details[name] = json.pop(name)

    if firearm_details:
        json["firearm_details"] = firearm_details

    return json
