from core.constants import COMPONENT_DETAILS_MAP


def get_is_component_initial_data(good_details):
    is_component_key = good_details.get("is_component", {}).get("key")
    if not is_component_key or is_component_key == "no":
        return {"is_component": False}
    return {"is_component": True}


def get_component_details_initial_data(good_details):
    is_component_key = good_details.get("is_component", {}).get("key")
    if is_component_key and not is_component_key == "no":
        return {
            COMPONENT_DETAILS_MAP[is_component_key]: good_details["component_details"],
            "component_type": is_component_key,
        }
    return {}
