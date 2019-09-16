from django.template.defaultfilters import default
from django.urls import reverse_lazy
from lite_forms.components import Form, BackLink, RadioButtons, Option, TextInput, TextArea, HTMLBlock, Heading, \
    HiddenField
from lite_forms.styles import HeadingStyle

from core.builtins.custom_tags import reference_code
from picklists.services import get_picklists


def respond_to_clc_query_form(request, case):
    return Form(title='Respond to CLC Query',
                questions=[
                    Heading(reference_code(case['query']['id']), HeadingStyle.S),
                    HTMLBlock(html='<div class="app-summary-list app-inset-text">'
                                        '<div class="app-summary-list__item">'
                                            '<p class="govuk-caption-m">Description</p>'
                                            '<p class="govuk-body-m">' + case['query']['good']['description'] + '</p>'
                                        '</div>'
                                        '<div class="app-summary-list__item">'
                                            '<p class="govuk-caption-m">Control list entry</p>'
                                            '<p class="govuk-body-m">' + default(case['query']['good']['control_code'], 'N/A') + '</p>'
                                        '</div>'
                                    '</div>'),
                    HTMLBlock(html='<hr class="lite-horizontal-separator">'),
                    RadioButtons(title='Is this good controlled?',
                                 name='is_good_controlled',
                                 options=[
                                     Option(key='yes',
                                            value='Yes',
                                            show_pane='pane_control_code'),
                                     Option(key='no',
                                            value='No')
                                 ],
                                 classes=['govuk-radios--inline']),
                    TextInput(title='What\'s the good\'s actual control rating?',
                              name='control_code'),
                    RadioButtons(title='Which report summary would you like to use?',
                                 name='report_summary',
                                 options=get_picklists(request, 'report_summary', convert_to_options=True),
                                 classes=['test']),
                    TextArea(title='Good\'s comment',
                             name='comment',
                             extras={
                                 'max_length': 500,
                             }),
                    HiddenField('validate_only', True)
                ],
                default_button_name='Continue to overview',
                back_link=BackLink('Back to case', reverse_lazy('cases:case', kwargs={'pk': case['id']})))
