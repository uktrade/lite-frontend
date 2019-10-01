def create_user(user):
    return {
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'email': user['email']
    }

def create_organisation(exporter, name):
    return {
        'name': name,
        'sub_type': 'commercial',
        'eori_number': '1234567890AAA',
        'sic_number': '2345',
        'vat_number': 'GB1234567',
        'registration_number': '09876543',
        'user': exporter,
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
    }

def create_request_data(exporter_user, gov_user, test_s3_key):
    exporter = create_user(exporter_user)
    gov = create_user(gov_user)
    return {
        'organisation': create_organisation(exporter, 'Test Org'),
        'organisation_for_switching_organisations': create_organisation(exporter, 'Octopus Systems'),
        'good': {
            'description': 'Lentils',
            'is_good_controlled': 'yes',
            'control_code': 'ML1a',
            'is_good_end_product': True,
            'part_number': '1234',
            'validate_only': False,
        },
        'good_end_product_true': {
            'description': 'Hot Cross Buns',
            'is_good_controlled': 'yes',
            'control_code': 'ML1a',
            'is_good_end_product': True,
            'part_number': '1234',
            'validate_only': False
        },
        'good_end_product_false': {
            'description': 'Falafels',
            'is_good_controlled': 'yes',
            'control_code': 'ML1a',
            'is_good_end_product': False,
            'part_number': '1234',
            'validate_only': False,
        },
        'gov_user': gov,
        'export_user': {
            'email': exporter['email'],
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
            'text': 'I Am Easy to Find',
            'is_visible_to_exporter': True
        },
        'ecju_query': {
            'question': 'This is a question, please answer'
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
