from core.form_components import Section, Form, Question, InputType, HTMLBlock, HiddenField

section1 = Section("Application Information", "", [
    Form("Enter a name or reference for your application", "This can make it easier to find in the future.", [
        Question(title='',
                 description='',
                 input_type=InputType.INPUT,
                 name='name'),
    ]),
    Form("Destination", "", [
        Question(title='',
                 description='',
                 input_type=InputType.INPUT,
                 name='destination'),
    ]),
    Form("Usage", "", [
        Question(title='',
                 description='',
                 input_type=InputType.INPUT,
                 name='usage'),
    ]),
    Form("Activity", "", [
        Question(title='',
                 description='',
                 input_type=InputType.INPUT,
                 name='activity'),
    ]),
])


def preexisting_good_form(id, description, control_code, part_number):
    return Form('Add a pre-existing good to your application', '', [
        HTMLBlock('<div class="govuk-inset-text">'
                  '<p><span style="opacity: 0.6;">Description:</span> ' + description + '</p>'
                  '<p><span style="opacity: 0.6;">Control Code:</span> ' + control_code + '</p>'
                  '<p><span style="opacity: 0.6;">Part Number:</span> ' + part_number + '</p>'
                  '</div>'),
        HiddenField(name='good_id',
                    value=id),
        Question(title='Quantity',
                 description='',
                 input_type=InputType.INPUT,
                 name='quantity'),
        Question(title='Value',
                 description='',
                 input_type=InputType.INPUT,
                 name='value'),
        Question(title='Unit of Measurement',
                 description='',
                 input_type=InputType.INPUT,
                 name='unit'),
    ])
