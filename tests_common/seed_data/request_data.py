org_name = 'Test Org'
org_name_for_switching_organisations = 'Octopus Systems'
logging = True
case_note_text = 'I Am Easy to Find'
ecju_query_text = 'This is a question, please answer'
first_name = 'Test'
last_name = 'Lite'
good_end_product_true = 'Hot Cross Buns'
good_end_product_false = 'Falafels'

def get_request_data(exporter_user_email):
    return {
        'organisation': {
            'name': org_name,
            'sub_type': 'commercial',
            'eori_number': '1234567890AAA',
            'sic_number': '2345',
            'vat_number': 'GB1234567',
            'registration_number': '09876543',
            'user': {
                'first_name': first_name,
                'last_name': last_name,
                'email': exporter_user_email
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
                'first_name': first_name,
                'last_name': last_name,
                'email': exporter_user_email
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
            'email': 'test-uat-user@digital.trade.gov.uk',
            'first_name': 'ecju',
            'last_name': 'user'},
        'export_user': {
            'email': exporter_user_email,
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
            'country': 'Ukraine',
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
        'document': {
            'name': 'document 1',
            's3_key': env('TEST_S3_KEY'),
            'size': 0,
            'description': 'document for test setup'
        }
    }
