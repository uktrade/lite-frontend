org_name = 'Test Org'
org_name_for_switching_organisations = 'Octopus Systems'
logging = True
case_note_text = 'I Am Easy to Find'
ecju_query_text = 'This is a question, please answer'
good_end_product_true = 'Hot Cross Buns'
good_end_product_false = 'Falafels'


def create_request_data(exporter_user, gov_user, test_s3_key):
    return {
        'organisation': {
            'name': org_name,
            'sub_type': 'commercial',
            'eori_number': '1234567890AAA',
            'sic_number': '2345',
            'vat_number': 'GB1234567',
            'registration_number': '09876543',
            'user': {
                'first_name': exporter_user['first_name'],
                'last_name': exporter_user['last_name'],
                'email': exporter_user['email']
            },
            'site': {
                'name': 'Headquarters',
                'address': {
                    'address_line_1': '42 Question Road',
                    'postcode': 'Islington',
                    'city': 'London',
                    'region': 'London',
                    'country': 'GB'
                }
            }
        },
        'organisation_for_switching_organisations': {
            'name': org_name_for_switching_organisations,
            'sub_type': 'commercial',
            'eori_number': '1234567890AAA',
            'sic_number': '2345',
            'vat_number': 'GB1234567',
            'registration_number': '09876543',
            'user': {
                'first_name': exporter_user['first_name'],
                'last_name': exporter_user['last_name'],
                'email': exporter_user['email']
            },
            'site': {
                'name': 'Headquarters',
                'address': {
                    'address_line_1': '42 Question Road',
                    'postcode': 'Islington',
                    'city': 'London',
                    'region': 'London',
                    'country': 'GB'
                }
            }
        },
        'good': {
            'description': 'Lentils',
            'is_good_controlled': 'yes',
            'control_code': 'ML1a',
            'is_good_end_product': True,
            'part_number': '1234',
            'validate_only': False,
        },
        'good_end_product_true': {
            'description': good_end_product_true,
            'is_good_controlled': 'yes',
            'control_code': 'ML1a',
            'is_good_end_product': True,
            'part_number': '1234',
            'validate_only': False
        },
        'good_end_product_false': {
            'description': good_end_product_false,
            'is_good_controlled': 'yes',
            'control_code': 'ML1a',
            'is_good_end_product': False,
            'part_number': '1234',
            'validate_only': False,
        },
        'gov_user': {
            'email': gov_user['email'],
            'first_name': gov_user['first_name'],
            'last_name': gov_user['last_name']
        },
        'export_user': {
            'email': exporter_user['email'],
            'password': 'password'
        },
        'draft': {
            'name': 'application',
            'licence_type': 'standard_licence',
            'export_type': 'permanent',
            'have_you_been_informed': 'yes',
            'reference_number_on_information_form': '1234'
        },
        'end-user': {
            'name': 'Government',
            'address': 'Westminster, London SW1A 0AA',
            'country': 'GB',
            'sub_type': 'government',
            'website': 'https://www.gov.uk'
        },
        "end_user_advisory": {
            "end_user": {
                "name": "Person",
                "address": "Westminster, London SW1A 0AA",
                "country": "GB",
                "sub_type": "government",
                "website": "https://www.gov.uk"
            },
            "contact_telephone": 12345678901,
            "contact_email": "person@gov.uk",
            "reasoning": "This is the reason for raising the enquiry",
            "note": "note for end user advisory"
        },
        'ultimate_end_user': {
            'name': 'Individual',
            'address': 'Bullring, Birmingham SW1A 0AA',
            'country': 'GB',
            'sub_type': 'commercial',
            'website': 'https://www.anothergov.uk'
        },
        'consignee': {
            'name': 'Government',
            'address': 'Westminster, London SW1A 0BB',
            'country': 'GB',
            'sub_type': 'government',
            'website': 'https://www.gov.uk'
        },
        "third_party": {
            "name": "Individual",
            "address": "Ukraine, 01532",
            "country": "UA",
            "sub_type": "agent",
            "website": "https://www.anothergov.uk"
        },
        'add_good': {
            'good_id': '',
            'quantity': 1234,
            'unit': 'NAR',
            'value': 123.45
        },
        'clc_good': {
            'description': 'Targus',
            'is_good_controlled': 'unsure',
            'control_code': 'ML1a',
            'is_good_end_product': True,
            'part_number': '1234',
            'validate_only': False,
            'details': 'Kebabs'
        },
        'case_note': {
            'text': case_note_text,
            'is_visible_to_exporter': True
        },
        'ecju_query': {
            'question': ecju_query_text
        },
        "ecju_query_picklist": {
            "name": "Standard question 1",
            "text": "Why did the chicken cross the road?",
            "type": "ecju_query"
        },
        'document': {
            'name': 'document 1',
            's3_key': test_s3_key,
            'size': 0,
            'description': 'document for test setup'
        },
        "additional_document": {
            'name': 'picture',
            's3_key': test_s3_key,
            'size': 0,
            'description': 'document for additional'
        },
        "proviso_picklist": {
            "name": "Misc",
            "text": "My proviso advice would be this.",
            "proviso": "My proviso would be this.",
            "type": "proviso"
        },
        "standard_advice_picklist": {
            "name": "More advice",
            "text": "My standard advice would be this.",
            "type": "standard_advice"
        },
        "report_picklist": {
            "name": "More advice",
            "text": "My standard advice would be this.",
            "type": "report_summary"
        }
    }
