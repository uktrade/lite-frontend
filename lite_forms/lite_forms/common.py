from lite_forms.components import TextInput, Select


def address_questions(countries, prefix='address.'):
    return [TextInput(title='Building and street',
                      description='<span class="govuk-visually-hidden">line 1 of 2</span>',
                      name=prefix + 'address_line_1'),
            TextInput(title='',
                      description='<span class="govuk-visually-hidden">line 2 of 2</span>',
                      name=prefix + 'address_line_2'),
            TextInput(title='Town or city',
                      name='city'),
            TextInput(title=prefix + 'County/State',
                      name='region'),
            TextInput(title=prefix + 'Postal Code',
                      name='postcode'),
            Select(title='Country',
                   name=prefix + 'country',
                   options=countries)]
