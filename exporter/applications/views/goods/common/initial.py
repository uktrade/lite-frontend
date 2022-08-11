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
