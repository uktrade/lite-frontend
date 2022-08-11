from datetime import date

from exporter.core.helpers import str_to_bool


def get_name_initial_data(good):
    return {"name": good["name"]}


def get_control_list_entry_initial_data(good):
    control_list_entries = []
    is_good_controlled = good["is_good_controlled"]["key"]
    if is_good_controlled == "True":
        control_list_entries = [clc["rating"] for clc in good.get("control_list_entries", [])]

    return {
        "is_good_controlled": is_good_controlled,
        "control_list_entries": control_list_entries,
    }


def get_pv_grading_initial_data(good):
    return {"is_pv_graded": str_to_bool(good["is_pv_graded"].get("key"))}


def get_pv_grading_details_initial_data(good):
    pv_grading_details = good["pv_grading_details"]

    return {
        "prefix": pv_grading_details.get("prefix"),
        "grading": pv_grading_details["grading"].get("key"),
        "suffix": pv_grading_details.get("suffix"),
        "issuing_authority": pv_grading_details.get("issuing_authority"),
        "reference": pv_grading_details.get("reference"),
        "date_of_issue": date.fromisoformat(pv_grading_details["date_of_issue"])
        if pv_grading_details["date_of_issue"]
        else None,
    }
