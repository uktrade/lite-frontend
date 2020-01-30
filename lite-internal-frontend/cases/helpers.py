from django.urls import reverse_lazy

from conf.constants import UPDATED_CASES_QUEUE_ID
from lite_content.lite_internal_frontend.strings import QUEUE_ALL_CASES
from lite_forms.components import Breadcrumbs, BackLink, HiddenField


def clean_advice(json):
    import ast

    def _clean_dict_item(item):
        return ast.literal_eval(item)

    json = json.copy()

    json["goods"] = _clean_dict_item(json["goods"])
    json["goods_types"] = _clean_dict_item(json["goods_types"])
    json["countries"] = _clean_dict_item(json["countries"])
    json["ultimate_end_users"] = _clean_dict_item(json["ultimate_end_users"])
    json["third_parties"] = _clean_dict_item(json["third_parties"])
    json["denial_reasons"] = json.getlist("denial_reasons")

    if json.get("end_user"):
        json["end_user"] = json["end_user"]
    else:
        json["end_user"] = ""

    if json.get("consignee"):
        json["consignee"] = json["consignee"]
    else:
        json["consignee"] = ""

    return json


def add_hidden_advice_data(questions_list, data):
    questions_list.append(HiddenField("goods", data.getlist("goods")))
    questions_list.append(HiddenField("goods_types", data.getlist("goods_types")))
    questions_list.append(HiddenField("countries", data.getlist("countries")))
    questions_list.append(HiddenField("end_user", data.get("end_user", "")))
    questions_list.append(HiddenField("consignee", data.get("consignee", "")))
    questions_list.append(HiddenField("ultimate_end_users", data.getlist("ultimate_end_users")))
    questions_list.append(HiddenField("third_parties", data.getlist("third_parties")))
    return questions_list


def check_matching_advice(user_id, advice, goods_or_destinations):
    first_advice = None
    pre_data = None

    # Checks if the item of advice which is owned by the user is in the selected advice that they are trying to edit
    def is_in_goods_or_destinations(item, goods_or_destinations):
        goods_or_destinations = str(goods_or_destinations)
        if (
            str(item.get("good")) in goods_or_destinations
            or str(item.get("end_user")) in goods_or_destinations
            or str(item.get("ultimate_end_user")) in goods_or_destinations
            or str(item.get("third_party")) in goods_or_destinations
            or str(item.get("consignee")) in goods_or_destinations
            or str(item.get("goods_type")) in goods_or_destinations
            or str(item.get("country")) in goods_or_destinations
        ):
            return True
        return False

    # Pre-populate data only in the instance that all the data contained within all selected advice matches
    for item in [
        x for x in advice if x["user"]["id"] == user_id and is_in_goods_or_destinations(x, goods_or_destinations)
    ]:
        # Sets up the first piece of advice to compare against then skips to the next cycle of the loop
        if first_advice is None:
            first_advice = item
            pre_data = {
                "type": {"key": first_advice["type"]["key"], "value": first_advice["type"]["value"]},
                "proviso": first_advice.get("proviso"),
                "denial_reasons": first_advice.get("denial_reasons"),
                "advice": first_advice.get("text"),
                "note": first_advice.get("note"),
            }
            continue

        # End loop if any data does not match
        if not first_advice["type"]["key"] == item["type"]["key"]:
            pre_data = None
            break
        else:
            if not first_advice.get("proviso") == item.get("proviso"):
                pre_data = None
                break
            if not first_advice.get("denial_reasons") == item.get("denial_reasons"):
                pre_data = None
                break
            if not first_advice.get("text") == item.get("text"):
                pre_data = None
                break
            if not first_advice.get("note") == item.get("note"):
                pre_data = None
                break

    return pre_data


def get_updated_cases_banner_queue_id(current_queue_id, queues):
    if current_queue_id != UPDATED_CASES_QUEUE_ID:
        for queue in queues:
            if queue["id"] == UPDATED_CASES_QUEUE_ID and queue["case_count"]:
                return UPDATED_CASES_QUEUE_ID


def case_view_breadcrumbs(case: dict, current_view: str):
    """
    Returns a Breadcrumb bar suitable for forms
    Pulls the reference code from case
    Current view is the title of the page the breadcrumb bar is on
    """
    return Breadcrumbs(
        [
            BackLink(QUEUE_ALL_CASES, reverse_lazy("cases:cases")),
            BackLink(case["reference_code"], reverse_lazy("cases:case", kwargs={"pk": case["id"]})),
            BackLink(current_view),
        ]
    )
