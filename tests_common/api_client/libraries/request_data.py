import random
import string

from faker import Faker

fake = Faker()

example_goods = [
    {"name": "Rifle", "description": "Firearms"},
    {"name": "Gatling gun", "description": "Firearms"},
    {"name": "Router", "description": "Network router"},
    {"name": "Artillery", "description": "Firearms"},
    {"name": "Spectrometer", "description": "Specialized optics"},
    {"name": "CCD Detector", "description": "Image sensor"},
    {"name": "Cryptographical software", "description": "Encryption software"},
    {"name": "Aileron", "description": "Aircraft component"},
    {"name": "Ammunition", "description": "Sporting shotgun ammunition"},
    {"name": "Assembly board", "description": "Electronics assembly board"},
]


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
        "eori_number": "GB123456789000",
        "phone_number": "+441234567890",
        "website": "http://somewebsite.com",
        "sic_number": "12345",
        "vat_number": "GB123456789",
        "registration_number": "09876543",
        "user": exporter,
        "site": {
            "name": "Headquarters",
            "address": {
                "address_line_1": "42 Question Road",
                "postcode": "BC1 2DE",
                "city": "London",
                "region": "London",
                "country": "GB",
            },
        },
    }


def build_organisation(name, type, address, eori_number, registration_number):
    return {
        "name": name,
        "type": type,
        "eori_number": eori_number,
        "sic_number": "12345",
        "vat_number": "GB123456789",
        "registration_number": registration_number,
        "phone_number": "+441234567890",
        "website": "http://www.example-org.com",
        "user": {"email": "name@example.com"},
        "site": {"name": "site", "address": {"address_line_1": address}},
    }


def build_good(name, description, control_list_entry="ML1a", part_number="1234"):
    return {
        "name": name,
        "description": description,
        "is_good_controlled": True,
        "control_list_entries": [control_list_entry],
        "part_number": part_number,
        "validate_only": False,
        "is_pv_graded": "no",
        "item_category": "group1_device",
        "is_military_use": "yes_designed",
        "modified_military_use_details": "",
        "is_component": "no",
        "uses_information_security": True,
        "information_security_details": "",
    }


def build_party(name, sub_type, website, party_type):
    data = {
        "name": name,
        "address": fake.street_address() + ", " + fake.postalcode() + ", " + fake.city() + ", " + fake.state(),
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


def random_colour():
    return random.choice(["red", "orange", "blue", "yellow", "green", "pink", "purple", "brown", "turquoise"])


def random_part_number(max_len=16):
    def randstr(len):
        return "".join(random.choice(string.ascii_uppercase) for _ in range(len))

    def randint(len):
        return "".join(random.choice(string.digits) for _ in range(len))

    return f"{randstr(2)}-{randstr(4)}-{randint(8)}"


def build_request_data(exporter_user, gov_user):
    exporter = build_user(exporter_user)
    good = random.choice(example_goods)
    request_data = {
        "organisation": build_organisation_with_user(exporter, "commercial", "Archway Communications"),
        # Please leave this as HMRC as tests depend on this being HMRC.
        "organisation_for_switching_organisations": build_organisation_with_user(
            exporter, "hmrc", "HMRC Wayne Enterprises"
        ),
        "good": build_good(good["name"], good["description"], part_number=random_part_number()),
        "application": {
            "name": "application",
            "application_type": "siel",
            "export_type": "permanent",
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": fake.ean(length=8),
        },
        "gov_user": build_user(gov_user),
        "end-user": build_party(fake.name(), "government", fake.url(), "end_user"),
        "end_user_advisory": {
            "end_user": build_party(fake.name(), "government", fake.url(), "end_user"),
            "contact_telephone": fake.ean(length=13),
            "contact_email": fake.free_email(),
            "reasoning": fake.bs(),
            "note": fake.bs(),
        },
        "ultimate_end_user": build_party(fake.name(), "commercial", fake.url(), "ultimate_end_user"),
        "consignee": build_party(fake.name(), "government", fake.url(), "consignee"),
        "third_party": build_party(fake.name(), "government", fake.url(), "third_party"),
        "add_good": {"good_id": "", "quantity": 1234, "unit": "NAR", "value": 123.45, "is_good_incorporated": True},
        "clc_good": {
            "description": fake.bs(),
            "is_good_controlled": None,
            "control_list_entries": [],
            "is_good_incorporated": True,
            "part_number": fake.ean(length=8),
            "validate_only": False,
            "details": fake.bs(),
            "is_pv_graded": "no",
            "item_category": "group1_device",
            "is_military_use": "yes_designed",
            "modified_military_use_details": "",
            "is_component": "no",
            "uses_information_security": False,
            "information_security_details": "",
            "status": "query",
        },
        "grading_good": {
            "description": fake.bs(),
            "is_good_controlled": True,
            "control_list_entries": ["ML1a"],
            "is_good_incorporated": True,
            "part_number": fake.ean(length=8),
            "validate_only": False,
            "details": fake.bs(),
            "is_pv_graded": "grading_required",
            "item_category": "group1_device",
            "is_military_use": "yes_designed",
            "modified_military_use_details": "",
            "is_component": "no",
            "uses_information_security": False,
            "information_security_details": "",
            "status": "query",
        },
        "add_exhibition_good": {"good_id": "", "item_type": "video"},
        "case_note": {"text": fake.bs(), "is_visible_to_exporter": True},
        "edit_case_app": {"name": fake.bs()},
        "ecju_query": {"question": fake.bs() + "?", "query_type": "ecju_query"},
        "ecju_query_picklist": {
            "name": fake.bs(),
            "text": fake.bs() + "?",
            "type": "ecju_query",
        },
        "flag": {
            "colour": random_colour(),
            "label": "Test label",
            "priority": 0,
            "team": "00000000-0000-0000-0000-000000000001",
        },
        "not_sure_details": {"not_sure_details_details": fake.bs(), "not_sure_details_control_code": "ML1a"},
        "good_type": {
            "description": fake.bs(),
            "is_good_controlled": True,
            "control_list_entries": ["ML1a"],
            "is_good_incorporated": True,
            "content_type": "draft",
        },
        "queue": {"team": "00000000-0000-0000-0000-000000000001"},
        "proviso_picklist": build_picklist_data(
            "Misc",
            fake.bs(),
            "proviso",
            proviso="My proviso would be this.",
        ),
        "standard_advice_picklist": build_picklist_data("More advice", fake.bs(), "standard_advice"),
        "report_picklist": build_picklist_data(fake.bs(), fake.bs(), "report_summary"),
        "letter_paragraph_picklist": build_picklist_data("Letter Paragraph 1", fake.bs(), "letter_paragraph"),
        "document_template": {"case_types": ["siel", "oiel"]},
        "export_user": {
            "email": exporter["email"],
            "user_profile": {"first_name": exporter["first_name"], "last_name": exporter["last_name"]},
            "sites": {},
            "role": "00000000-0000-0000-0000-000000000003",
        },
        "exhibition_details": {
            "title": fake.bs(),
            "first_exhibition_date": "3000-02-01",
            "required_by_date": "3000-01-01",
        },
        "declaration": {
            "submit_declaration": True,
            "agreed_to_foi": True,
            "agreed_to_declaration": True,
            "foi_reason": "No objection",
            "agreed_to_declaration_text": "I AGREE",
        },
    }
    return request_data
