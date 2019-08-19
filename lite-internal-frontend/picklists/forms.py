from django.urls import reverse_lazy

from core.builtins.custom_tags import get_string
from libraries.forms.components import Question, Form, InputType, Option, Select, BackLink, Button, ButtonStyle, \
    TextArea

_name = Question(title='Name',
                 description='',
                 input_type=InputType.INPUT,
                 name='name')

_picklist_type = Select(name='type',
                        options=[Option('proviso', 'Proviso'),
                                 Option('ecju_query', 'ECJU Query'),
                                 Option('letter_paragraph', 'Letter Paragraph'),
                                 Option('annual_report_summary', 'Annual Report Summary'),
                                 Option('standard_advice', 'Standard Advice'),
                                 Option('footnotes', 'Footnote')],
                        title='Type')

_text = TextArea(title='Add text for picklist item',
                 description='',
                 name='text',
                 extras={
                     'max_length': 5000,
                 })

_back_link = BackLink('Back to picklists', '#')


def add_picklist_item_form():
    return Form(title=get_string('picklist.create'),
                description='',
                questions=[
                    _name,
                    _picklist_type,
                    _text,
                ],
                back_link=_back_link,
                default_button_name='Save')


def edit_picklist_item_form(picklist_item):
    deactivate_button = Button('Deactivate',
                               '',
                               ButtonStyle.WARNING,
                               reverse_lazy('picklists:deactivate',
                                            kwargs={'pk': picklist_item['picklist_item']['id']}),
                               True)
    activate_button = Button('Reactivate',
                             '',
                             ButtonStyle.SECONDARY,
                             reverse_lazy('picklists:reactivate',
                                          kwargs={'pk': picklist_item['picklist_item']['id']}),
                             True)

    if picklist_item['picklist_item']['status']['key'] == 'deactivated':
        button = activate_button
    else:
        button = deactivate_button

    return Form(title=get_string('picklist.edit'),
                description='',
                questions=[
                    _name,
                    _picklist_type,
                    _text,
                ],
                back_link=BackLink('Back to ' + picklist_item['picklist_item']['name'],
                                   reverse_lazy('picklists:picklist_item',
                                                kwargs={'pk': picklist_item['picklist_item']['id']})),
                buttons=[
                    Button('Save', 'submit', ButtonStyle.DEFAULT),
                    button,
                ])


def deactivate_picklist_item(picklist_item):
    return Form(title='Are you sure you want to deactivate ' + picklist_item['picklist_item']['name'] + '?',
                description='You can always reactivate it later if need be.',
                questions=[],
                back_link=BackLink('Back',
                                   reverse_lazy('picklists:edit',
                                                kwargs={'pk': picklist_item['picklist_item']['id']})),
                buttons=[
                    Button('Deactivate', 'submit', ButtonStyle.WARNING),
                    Button('Cancel',
                           'cancel',
                           ButtonStyle.SECONDARY,
                           reverse_lazy('picklists:edit',
                                        kwargs={'pk': picklist_item['picklist_item']['id']}))
                ])


def reactivate_picklist_item(picklist_item):
    return Form(title='Are you sure you want to reactivate ' + picklist_item['picklist_item']['name'] + '?',
                description='You can always deactivate it later if need be.',
                questions=[],
                back_link=BackLink('Back',
                                   reverse_lazy('picklists:edit',
                                                kwargs={'pk': picklist_item['picklist_item']['id']})),
                buttons=[
                    Button('Reactivate', 'submit', ButtonStyle.DEFAULT),
                    Button('Cancel',
                           'cancel',
                           ButtonStyle.SECONDARY,
                           reverse_lazy('picklists:edit',
                                        kwargs={'pk': picklist_item['picklist_item']['id']}))
                ])
