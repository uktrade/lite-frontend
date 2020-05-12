from conf.constants import UPDATED_CASES_QUEUE_ID
from lite_content.lite_internal_frontend.cases import GenerateDocumentsPage
from lite_forms.generators import error_page


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


def generate_document_error_page():
    return error_page(
        None, title=GenerateDocumentsPage.TITLE, description=GenerateDocumentsPage.ERROR, show_back_link=True,
    )
