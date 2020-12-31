from core import client


def get_routing_rules(request, params=""):
    data = client.get(request, f"/routing-rules/?{params}")
    return data.json(), data.status_code


def get_routing_rule(request, id):
    data = client.get(request, f"/routing-rules/{id}")
    return data.json(), data.status_code


def _remove_none_from_post_data_additional_rules_list(json):
    """
    removes hidden field value from json field "additional_rules" list,
        which is there to ensure field exists for editing purposes
    :param json: this is data that is going to be posted
    """
    data = json
    additional_rules = json.get("additional_rules", [])
    data["additional_rules"] = list(set([rule for rule in additional_rules if rule != "None"]))
    return data


def convert_flags_to_list(data):
    if "flags_to_include" in data:
        data["flags_to_include"] = [flag_id.strip() for flag_id in data["flags_to_include"].split(",") if flag_id]
    if "flags_to_exclude" in data:
        data["flags_to_exclude"] = [flag_id.strip() for flag_id in data["flags_to_exclude"].split(",") if flag_id]

    return data


def post_routing_rule(request, json):
    data = _remove_none_from_post_data_additional_rules_list(json)
    data = convert_flags_to_list(data)
    response = client.post(request, "/routing-rules/", data)
    return response.json(), response.status_code


def validate_put_routing_rule(request, id, json):
    data = json
    data["validate_only"] = True
    return put_routing_rule(request, id, data)


def put_routing_rule(request, id, json):
    data = _remove_none_from_post_data_additional_rules_list(json)
    data = convert_flags_to_list(data)
    response = client.put(request, f"/routing-rules/{id}", data)
    return response.json(), response.status_code


def put_routing_rule_active_status(request, id, json):
    data = json
    # the confirm name is the name of the form
    data["status"] = data["form_name"]

    data = client.put(request, f"/routing-rules/{id}/status/", data)
    return data.json(), data.status_code
