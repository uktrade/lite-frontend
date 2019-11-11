from django.urls import reverse_lazy
from lite_forms.components import Form, FormGroup, TextInput, BackLink, Checkboxes, Option, RadioButtonsImage

from core.builtins.custom_tags import get_string
from letter_templates.services import get_letter_layouts


def _letter_layout_options():
    options = []
    for letter_layout in get_letter_layouts():
        filename = letter_layout['filename']
        options.append(Option(
            letter_layout["id"],
            letter_layout["name"],
            img_url=f"/assets/images/letter_templates/{ filename }.png"
        ))

    return options


def add_letter_template():
    return FormGroup(
        forms=[
            Form(title=get_string('letter_templates.add_letter_template.name.title'),
                 description=get_string('letter_templates.add_letter_template.name.hint'),
                 questions=[
                     TextInput(name='name')
                 ],
                 back_link=BackLink(get_string('letter_templates.add_letter_template.name.back_link'),
                                    reverse_lazy('letter_templates:letter_templates')),
                 default_button_name=get_string('letter_templates.add_letter_template.name.continue_button')),
            Form(title=get_string('letter_templates.add_letter_template.case_types.title'),
                 questions=[
                     Checkboxes(
                         name='restricted_to',
                         options=[
                             Option('application', 'Applications'),
                             Option('clc_query', 'Control List Classification Queries'),
                             Option('end_user_advisory_query', 'End User Advisory Queries'),
                         ])
                 ],
                 default_button_name=get_string('letter_templates.add_letter_template.case_types.continue_button')),
            Form(title=get_string('letter_templates.add_letter_template.layout.title'),
                 questions=[
                     RadioButtonsImage(
                         name='layout',
                         options=_letter_layout_options(),
                     )
                 ],
                 default_button_name=get_string('letter_templates.add_letter_template.layout.continue_button'))
        ])


def edit_letter_template(letter_template):
    return Form(title=get_string('letter_templates.edit_letter_template.title') % letter_template['name'],
                questions=[
                    TextInput(title=get_string('letter_templates.edit_letter_template.name.title'),
                              description=get_string('letter_templates.edit_letter_template.name.hint'),
                              name='name'),
                    Checkboxes(
                        title=get_string('letter_templates.edit_letter_template.case_types.title'),
                        name='restricted_to',
                        options=[
                            Option('application', 'Application'),
                            Option('clc_query', 'CLC Query'),
                            Option('end_user_advisory_query', 'End User Advisory Query'),
                        ]),
                    RadioButtonsImage(
                        title=get_string('letter_templates.edit_letter_template.layout.title'),
                        name='layout',
                        options=_letter_layout_options(),
                    )
                ],
                back_link=BackLink('Back to ' + letter_template['name'],
                                   reverse_lazy('letter_templates:letter_template',
                                                kwargs={'pk': letter_template['id']})),
                default_button_name=get_string('letter_templates.edit_letter_template.button_name'))
