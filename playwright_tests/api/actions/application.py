from .requests_helper import post, put


def create_draft_application(fixture, headers):
    return post("applications/", {"json": fixture, "headers": headers}).json()


def add_good_to_application(application_id, fixture, headers):
    post(f"applications/{application_id}/goods/", {"json": fixture, "headers": headers})


def add_location_to_application(application_id, fixture, headers):
    post(f"applications/{application_id}/sites/", {"json": fixture, "headers": headers})


def add_end_user_to_application(application_id, fixture, headers):
    return post(f"applications/{application_id}/parties/", {"json": fixture, "headers": headers}).json()


def add_document_to_application_end_user(application_id, end_user_id, fixture, headers):
    post(f"applications/{application_id}/parties/{end_user_id}/document/", {"json": fixture, "headers": headers})


def add_ultimate_end_user_to_application(application_id, fixture, headers):
    post(f"applications/{application_id}/parties/", {"json": fixture, "headers": headers})


def add_consignee_to_application(application_id, fixture, headers):
    post(f"applications/{application_id}/parties/", {"json": fixture, "headers": headers})


def add_third_party_to_application(application_id, fixture, headers):
    post(f"applications/{application_id}/parties/", {"json": fixture, "headers": headers})


def add_end_use_details_to_application(application_id, fixture, headers):
    put(f"applications/{application_id}/end-use-details/", {"json": fixture, "headers": headers})


def add_route_of_goods_to_application(application_id, fixture, headers):
    put(f"applications/{application_id}/route-of-goods/", {"json": fixture, "headers": headers})


def submit_application(application_id, fixture, headers):
    return put(f"applications/{application_id}/submit/", {"json": fixture, "headers": headers}).json()


def change_application_status(application_id, fixture, headers):
    return put(f"applications/{application_id}/status/", {"json": fixture, "headers": headers})
