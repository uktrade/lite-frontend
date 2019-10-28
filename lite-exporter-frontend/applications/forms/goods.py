from lite_forms.components import Form, HiddenField, SideBySideSection, Select, QuantityInput, \
    CurrencyInput

from goods.helpers import good_summary


def preexisting_good_form(good, units):
    return Form(title='Add a pre-existing good to your application',
                questions=[
                    good_summary(good),
                    HiddenField(name='good_id',
                                value=good['id']),
                    CurrencyInput(title='What\'s the value of your goods?',
                                  name='value'),
                    SideBySideSection(questions=[
                        QuantityInput(title='Quantity',
                                      name='quantity'),
                        Select(title='Unit of Measurement',
                               name='unit',
                               options=units)
                    ]),
                ],
                javascript_imports=['/assets/javascripts/specific/add_good.js'])
