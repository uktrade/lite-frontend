def build_user(user):
    return {
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
    }


def build_organisation_with_user(exporter, type, name):
    return {
        "name": name,
        "type": type,
        "eori_number": "1234567890AAA",
        "sic_number": "2345",
        "vat_number": "GB1234567",
        "registration_number": "09876543",
        "user": exporter,
        "site": {
            "name": "Headquarters",
            "address": {
                "address_line_1": "42 Question Road",
                "postcode": "Islington",
                "city": "London",
                "region": "London",
                "country": "GB",
            },
        },
    }


def build_good(description, control_code="ML1a", part_number="1234"):
    return {
        "description": description,
        "is_good_controlled": "yes",
        "control_code": control_code,
        "part_number": part_number,
        "validate_only": False,
        "is_pv_graded": "no",
    }


def build_party(name, sub_type, website, party_type):
    data = {
        "name": name,
        "address": "Westminster, London SW1A 0AA",
        "country": "GB",
        "sub_type": sub_type,
        "website": website,
        "type": party_type,
    }
    if party_type == "third_party":
        data["role"] = "agent"
    return data


def build_picklist_data(name, text, type, proviso=None):
    picklist = {"name": name, "text": text, "type": type}
    if proviso:
        picklist["proviso"] = proviso
    return picklist


def build_request_data(exporter_user, gov_user):
    exporter = build_user(exporter_user)
    request_data = {
        "organisation": build_organisation_with_user(exporter, "commercial", "Square Is Circle Ltd"),
        # Please leave this as HMRC as tests depend on this being HMRC.
        "organisation_for_switching_organisations": build_organisation_with_user(
            exporter, "hmrc", "HMRC Wayne Enterprises"
        ),
        "good": build_good("Lentils"),
        "application": {
            "name": "application",
            "application_type": "standard",
            "export_type": "permanent",
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "1234",
        },
        "gov_user": build_user(gov_user),
        "end-user": build_party("Government", "government", "https://www.gov.uk", "end_user"),
        "end_user_advisory": {
            "end_user": build_party("Person", "government", "https://www.gov.uk", "end_user"),
            "contact_telephone": 12345678901,
            "contact_email": "person@gov.uk",
            "reasoning": "This is the reason for raising the enquiry",
            "note": "note for end user advisory",
        },
        "ultimate_end_user": build_party("Individual", "commercial", "https://www.anothergov.uk", "ultimate_end_user"),
        "consignee": build_party("Government", "government", "https://www.gov.uk", "consignee"),
        "third_party": build_party("Individual", "government", "https://www.anothergov.uk", "third_party"),
        "add_good": {"good_id": "", "quantity": 1234, "unit": "NAR", "value": 123.45, "is_good_incorporated": True},
        "clc_good": {
            "description": "Targus",
            "is_good_controlled": "unsure",
            "control_code": "ML1a",
            "is_good_incorporated": True,
            "part_number": "1234",
            "validate_only": False,
            "details": "Kebabs",
            "is_pv_graded": "no",
        },
        "grading_good": {
            "description": "Targus",
            "is_good_controlled": "yes",
            "control_code": "ML1a",
            "is_good_incorporated": True,
            "part_number": "1234",
            "validate_only": False,
            "details": "Kebabs",
            "is_pv_graded": "grading_required",
        },
        "case_note": {"text": "I Am Easy to Find", "is_visible_to_exporter": True},
        "edit_case_app": {"name": "new app name!"},
        "ecju_query": {"question": "This is a question, please answer"},
        "ecju_query_picklist": {
            "name": "Standard question 1",
            "text": "Why did the chicken cross the road?",
            "type": "ecju_query",
        },
        "not_sure_details": {"not_sure_details_details": "something", "not_sure_details_control_code": "ML1a"},
        "good_type": {
            "description": "A goods type",
            "is_good_controlled": True,
            "control_code": "ML1a",
            "is_good_incorporated": True,
            "content_type": "draft",
        },
        "queue": {"team": "00000000-0000-0000-0000-000000000001"},
        "proviso_picklist": build_picklist_data(
            "Misc", "My proviso advice would be this.", "proviso", proviso="My proviso would be this.",
        ),
        "standard_advice_picklist": build_picklist_data(
            "More advice", "My standard advice would be this.", "standard_advice"
        ),
        "report_picklist": build_picklist_data("More advice", "My standard advice would be this.", "report_summary"),
        "letter_paragraph_picklist": build_picklist_data(
            "Letter Paragraph 1", "My letter paragraph is this.", "letter_paragraph"
        ),
        "document_template": {"case_types": ["siel", "oiel"]},
        "export_user": {
            "email": exporter["email"],
            "user_profile": {"first_name": "Bruce", "last_name": "Wayne"},
            "sites": {},
        },
    }
    return request_data
