def create_user(user):
    return {
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'email': user['email']
    }


def create_organisation(exporter, type, name):
    return {
        'name': name,
        'type': type,
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


def create_good(description, is_end_product):
    return {
        'description': description,
        'is_good_controlled': 'yes',
        'control_code': 'ML1a',
        'is_good_end_product': is_end_product,
        'part_number': '1234',
        'validate_only': False,
    }


def create_party(name, sub_type, website):
    return {
        'name': name,
        'address': 'Westminster, London SW1A 0AA',
        'country': 'GB',
        'sub_type': sub_type,
        'website': website
    }


def create_document(name, description, s3_key):
    return {
        'name': name,
        's3_key': s3_key,
        'size': 0,
        'description': description
    }


def create_picklist(name, text, type, proviso=None):
    picklist = {
                'name': name,
                'text': text,
                'type': type
            }
    if proviso:
        picklist['proviso'] = proviso
    return picklist


def create_request_data(exporter_user, test_s3_key, gov_user):
    exporter = create_user(exporter_user)
    request_data = {
        'organisation': create_organisation(exporter, 'commercial', 'Archway Communications'),
        'organisation_for_switching_organisations': create_organisation(exporter, 'hmrc', 'Octopus Systems'),
        'good': create_good('Lentils', True),
        'good_end_product_true': create_good('Hot Cross Buns', True),
        'good_end_product_false': create_good('Falafels', False),
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
        'gov_user': create_user(gov_user),
        'end-user': create_party('Government', 'government', 'https://www.gov.uk'),
        'end_user_advisory': {
            'end_user': create_party('Person', 'government', 'https://www.gov.uk'),
            'contact_telephone': 12345678901,
            'contact_email': 'person@gov.uk',
            'reasoning': 'This is the reason for raising the enquiry',
            'note': 'note for end user advisory'
        },
        'ultimate_end_user': create_party('Individual', 'commercial', 'https://www.anothergov.uk'),
        'consignee': create_party('Government', 'government', 'https://www.gov.uk'),
        'third_party': create_party('Individual', 'agent', 'https://www.anothergov.uk'),
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
        'ecju_query_picklist': {
            'name': 'Standard question 1',
            'text': 'Why did the chicken cross the road?',
            'type': 'ecju_query'
        },
        'not_sure_details': {
            'not_sure_details_details': 'something',
            'not_sure_details_control_code': 'ML1a'
        },
        'good_type': {
            'description': 'A goods type',
            'is_good_controlled': True,
            'control_code': 'ML1a',
            'is_good_end_product': True,
            'content_type': 'draft',
        },
        'queue': {
            'team': '00000000-0000-0000-0000-000000000001'
        },
        'document': create_document('document 1', 'document for test setup', test_s3_key),
        'additional_document': create_document('picture', 'document for additional', test_s3_key),
        'proviso_picklist': create_picklist('Misc', 'My proviso advice would be this.', 'proviso', proviso='My proviso would be this.'),
        'standard_advice_picklist': create_picklist('More advice', 'My standard advice would be this.', 'standard_advice'),
        'report_picklist': create_picklist('More advice', 'My standard advice would be this.', 'report_summary')
    }
    return request_data
