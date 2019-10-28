from lite_forms.components import Form, TextInput


def reference_name_form():
    return Form(title='Enter a reference name for this application',
                description='This will make it easier for you or your organisation to find in the future.',
                questions=[
                    TextInput(name='name'),
                ],
                default_button_name='Save')
