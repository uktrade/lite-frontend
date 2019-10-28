from lite_forms.components import RadioButtons, Form, Option, FormGroup

from applications.forms.end_user import third_parties_standard_form

option_list = {
    'agent': 'Agent or broker',
    'additional_end_user': 'Additional end user',
    'intermediate_consignee': 'Intermediate consignee',
    'submitter': 'Authorised submitter',
    'consultant': 'Consultant',
    'contact': 'Contact',
    'exporter': 'Exporter'
}


def third_party_forms(export_type):
    if export_type['value'] == 'Permanent':
        form_options = option_list.copy()
        del form_options['additional_end_user']
    else:
        form_options = option_list.copy()
    third_party_form = third_parties_standard_form()
    options = [Option(key, value) for key, value in form_options.items()]
    options.append(Option('other', 'Other', show_or=True))
    third_party_type = Form(title='What type of third party would you like to add?',
                            questions=[
                                RadioButtons('sub_type', options=options)
                            ],
                            default_button_name='Continue')
    third_party_form[0] = third_party_type
    return FormGroup(third_party_form)
