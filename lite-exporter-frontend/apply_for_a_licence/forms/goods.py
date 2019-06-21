from libraries.forms.components import Form, HTMLBlock, HiddenField, Question, SideBySideSection, InputType, \
    ArrayQuestion


def preexisting_good_form(id, description, control_code, part_number, units):
    return Form('Add a pre-existing good to your application', '', [
        HTMLBlock('<div class="govuk-inset-text">'
                  '<p><span style="opacity: 0.6;">Description:</span> ' + description + '</p>'
                  '<p><span style="opacity: 0.6;">Control Code:</span> ' + control_code + '</p>'
                  '<p><span style="opacity: 0.6;">Part Number:</span> ' + part_number + '</p>'
                  '</div>'),
        HiddenField(name='good_id',
                    value=id),
        Question(title='What\'s the value of your goods?',
                 description='',
                 input_type=InputType.CURRENCY,
                 name='value'),
        SideBySideSection(questions=[
            Question(title='Quantity',
                     description='',
                     input_type=InputType.QUANTITY,
                     name='quantity'),
            ArrayQuestion(title='Unit of Measurement',
                          description='',
                          input_type=InputType.SELECT,
                          name='unit',
                          data=units)
        ]),
    ], javascript_imports=[
        '/assets/javascripts/specific/add_good.js'
    ])
