from lite_content.lite_internal_frontend import strings
from django.urls import reverse_lazy
from lite_forms.components import (
    Form,
    FormGroup,
    TextInput,
    BackLink,
    Checkboxes,
    Option,
    RadioButtonsImage,
)

from letter_templates.services import get_letter_layouts


def _letter_layout_options():
    options = []
    for letter_layout in get_letter_layouts():
        filename = letter_layout["filename"]
        options.append(
            Option(
                letter_layout["id"], letter_layout["name"], img_url=f"/assets/images/letter_templates/{ filename }.png"
            )
        )

    return options


def add_letter_template():
    return FormGroup(
        forms=[
            Form(
                title=strings.LetterTemplates.AddLetterTemplate.Name.TITLE,
                description=strings.LetterTemplates.AddLetterTemplate.Name.HINT,
                questions=[TextInput(name="name")],
                back_link=BackLink(
                    strings.LetterTemplates.AddLetterTemplate.Name.BACK_LINK,
                    reverse_lazy("letter_templates:letter_templates"),
                ),
                default_button_name=strings.LetterTemplates.AddLetterTemplate.Name.CONTINUE_BUTTON,
            ),
            Form(
                title=strings.LetterTemplates.AddLetterTemplate.CaseTypes.TITLE,
                questions=[
                    Checkboxes(
                        name="case_types",
                        options=[
                            Option(
                                "application", strings.LetterTemplates.AddLetterTemplate.CaseTypes.Types.APPLICATION
                            ),
                            Option(
                                "goods_query", strings.LetterTemplates.AddLetterTemplate.CaseTypes.Types.GOODS_QUERY
                            ),
                            Option(
                                "end_user_advisory_query",
                                strings.LetterTemplates.AddLetterTemplate.CaseTypes.Types.END_USER_ADVISORY,
                            ),
                        ],
                    )
                ],
                default_button_name=strings.LetterTemplates.AddLetterTemplate.CaseTypes.CONTINUE_BUTTON,
            ),
            Form(
                title=strings.LetterTemplates.AddLetterTemplate.Layout.TITLE,
                questions=[RadioButtonsImage(name="layout", options=_letter_layout_options(),)],
                default_button_name=strings.LetterTemplates.AddLetterTemplate.Layout.CONTINUE_BUTTON,
            ),
        ]
    )


def edit_letter_template(letter_template):
    return Form(
        title=strings.LetterTemplates.EditLetterTemplate.TITLE % letter_template["name"],
        questions=[
            TextInput(
                title=strings.LetterTemplates.EditLetterTemplate.Name.TITLE,
                description=strings.LetterTemplates.EditLetterTemplate.Name.HINT,
                name="name",
            ),
            Checkboxes(
                title=strings.LetterTemplates.EditLetterTemplate.CaseTypes.TITLE,
                name="case_types",
                options=[
                    Option("application", strings.LetterTemplates.EditLetterTemplate.CaseTypes.Types.APPLICATION),
                    Option("goods_query", strings.LetterTemplates.EditLetterTemplate.CaseTypes.Types.GOODS_QUERY),
                    Option(
                        "end_user_advisory_query",
                        strings.LetterTemplates.EditLetterTemplate.CaseTypes.Types.END_USER_ADVISORY,
                    ),
                ],
            ),
            RadioButtonsImage(
                title=strings.LetterTemplates.EditLetterTemplate.Layout.TITLE,
                name="layout",
                options=_letter_layout_options(),
            ),
        ],
        back_link=BackLink(
            "Back to " + letter_template["name"],
            reverse_lazy("letter_templates:letter_template", kwargs={"pk": letter_template["id"]}),
        ),
        default_button_name=strings.LetterTemplates.EditLetterTemplate.BUTTON_NAME,
    )
