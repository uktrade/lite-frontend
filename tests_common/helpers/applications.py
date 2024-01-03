from faker import Faker

fake = Faker()

good_default = {
    "good_id": "",
    "quantity": 1234,
    "unit": "MTR",
    "value": 10.24,
    "is_good_incorporated": True,
    "is_good_pv_graded": "no",
    "item_category": "group1_components",
    "is_military_use": "yes_designed",
    "is_component": "yes_modified",
    "component_details": "modified component details",
    "uses_information_security": True,
    "information_security_details": "details about security",
}


def create_standard_application(api_test_client, context, app_data, submit=True):
    api_test_client.api_client.auth_exporter_user(api_test_client.context["org_id"])
    goods = []

    products = (p.strip() for p in app_data["product"].split(","))
    for i, product in enumerate(products):
        data = api_test_client.api_client.request_data["good"]
        data["part_number"] = app_data.get("part_number", data["part_number"])
        data["name"] = product.strip()
        data["control_list_entries"] = [app_data["clc_rating"]]
        new_good = api_test_client.goods.post_good(data)
        api_test_client.api_client.add_to_context("good_id", new_good["id"])
        # To support multiple goods
        api_test_client.api_client.add_to_context(f"all_goods_{i}", {"id": new_good["id"], "name": data["name"]})

        current_good = good_default.copy()
        current_good["good_id"] = new_good["id"]
        goods.append(current_good)

        standard_application_submit(api_test_client, context, app_data, goods, submit)


def create_standard_application_with_reused_goods(api_test_client, context, app_data, submit=True):
    api_test_client.api_client.auth_exporter_user(api_test_client.context["org_id"])
    goods = []

    products = list(p.strip() for p in app_data["name"].split(","))
    data_context = api_test_client.api_client.context
    matching_values = [value for key, value in data_context.items() if key.startswith("all_goods_")]

    for good in matching_values:
        current_good = good_default.copy()
        current_good["good_id"] = good["id"]
        if good["name"] in products:
            goods.append(current_good)

    standard_application_submit(api_test_client, context, app_data, goods, submit)


def standard_application_submit(api_test_client, context, app_data, goods, submit):
    draft_id = api_test_client.applications.add_draft(
        draft={
            "name": app_data["name"],
            "application_type": "siel",
            "export_type": "permanent",
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "1234",
        },
        good=goods,
        end_user={
            "name": app_data["end_user_name"],
            "address": app_data["end_user_address"],
            "country": app_data["country"],
            "sub_type": "government",
            "website": fake.uri(),
            "type": "end_user",
            "signatory_name_euu": app_data["end_user_name"],
        },
        ultimate_end_user={
            "name": fake.name(),
            "address": fake.street_address() + ", " + fake.state() + ", " + fake.postcode(),
            "country": "GB",
            "sub_type": "commercial",
            "website": fake.uri(),
            "type": "ultimate_end_user",
        },
        consignee={
            "name": app_data["consignee_name"],
            "address": app_data["consignee_address"],
            "country": app_data["country"],
            "sub_type": "government",
            "website": fake.uri(),
            "type": "consignee",
        },
        third_party={
            "name": fake.name(),
            "address": fake.street_address() + ", " + fake.state() + ", " + fake.postcode(),
            "country": "UA",
            "sub_type": "government",
            "role": "agent",
            "website": fake.uri(),
            "type": "third_party",
        },
        end_use_details={
            "intended_end_use": app_data["end_use"],
            "is_military_end_use_controls": False,
            "is_informed_wmd": False,
            "is_suspected_wmd": False,
            "is_eu_military": False,
        },
        route_of_goods={"is_shipped_waybill_or_lading": True},
        additional_information={"is_mod_security_approved": app_data.get("is_mod_security_approved", False)},
    )

    if not submit:
        context.app_id = api_test_client.context["draft_id"]
        return

    data = api_test_client.applications.submit_application(draft_id)
    context.app_id = api_test_client.context["application_id"]
    context.case_id = api_test_client.context["application_id"]
    context.reference_code = api_test_client.context["reference_code"]
    context.app_name = app_data["name"]
    context.application_data = app_data
