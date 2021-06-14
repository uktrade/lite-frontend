from exporter.goods import services
from exporter.core.constants import FIREARM_AMMUNITION_COMPONENT_TYPES
from exporter.core.helpers import remove_prefix
from core.helpers import format_date


def serialize_good_on_app_data(request, json, good=None, preexisting=False):
    if json.get("good_on_app_value") or json.get("good_on_app_value") == "":
        post_data = remove_prefix(json, "good_on_app_")
    else:
        post_data = json
    for key in {"value", "quantity"} & set(post_data.keys()):
        if "," in post_data[key]:
            post_data[key] = post_data[key].replace(",", "")

    if json.get("date_of_deactivationday"):
        post_data["date_of_deactivation"] = format_date(post_data, "date_of_deactivation")

    post_data = services.add_firearm_details_to_data(request, post_data)

    # Adding new good to the application
    firearm_details = post_data.get("firearm_details")
    if firearm_details:
        if not preexisting and good:
            firearm_details["number_of_items"] = good["firearm_details"]["number_of_items"]
            if good["firearm_details"]["has_identification_markings"] is True:
                firearm_details["serial_numbers"] = good["firearm_details"]["serial_numbers"]
            else:
                firearm_details["serial_numbers"] = list()

            if good["firearm_details"]["type"]["key"] in FIREARM_AMMUNITION_COMPONENT_TYPES:
                post_data["quantity"] = good["firearm_details"]["number_of_items"]
                post_data["unit"] = "NAR"  # number of articles
            else:
                firearm_details["number_of_items"] = post_data["quantity"]

        if preexisting and good:
            if good["firearm_details"]["type"]["key"] in FIREARM_AMMUNITION_COMPONENT_TYPES:
                post_data["quantity"] = firearm_details.get("number_of_items", 0)
                post_data["unit"] = "NAR"  # number of articles

    return post_data
