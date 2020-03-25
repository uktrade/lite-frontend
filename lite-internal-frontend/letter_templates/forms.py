from cases.constants import CaseType
from cases.services import get_case_types, get_decisions
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
    RadioButtons,
)

from letter_templates.services import get_letter_layouts
from lite_forms.helpers import conditional


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


def add_letter_template(request):
    possible_case_types = get_case_types(request, type_only=False)
    chosen_case_types = request.POST.getlist("case_types")
    is_application_case_types_only = CaseType.HMRC_REFERENCE.value not in chosen_case_types

    if is_application_case_types_only:
        # iterate through all case-types and determine if the ones we have chosen are of type "application"
        for possible_case_type in possible_case_types:
            if (
                possible_case_type["reference"]["key"] in chosen_case_types
                and not possible_case_type["type"]["key"] == CaseType.APPLICATION.value
            ):
                is_application_case_types_only = False
                break

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
                        name="case_types[]",
                        options=[
                            Option(case_type["reference"]["key"], case_type["reference"]["value"])
                            for case_type in possible_case_types
                        ],
                        classes=["govuk-checkboxes--small"],
                    )
                ],
                default_button_name=strings.LetterTemplates.AddLetterTemplate.CaseTypes.CONTINUE_BUTTON,
            ),
            conditional(
                is_application_case_types_only,
                Form(
                    title=strings.LetterTemplates.EditLetterTemplate.Decisions.TITLE,
                    description=strings.LetterTemplates.EditLetterTemplate.Decisions.DESCRIPTION,
                    questions=[
                        Checkboxes(
                            name="decisions[]",
                            options=[
                                Option(decision["key"], decision["value"]) for decision in get_decisions(request)[0]
                            ],
                            classes=["govuk-checkboxes--small"],
                        )
                    ],
                    default_button_name=strings.LetterTemplates.AddLetterTemplate.CaseTypes.CONTINUE_BUTTON,
                ),
            ),
            Form(
                title=strings.LetterTemplates.AddLetterTemplate.VisibleToExporter.TITLE,
                description=strings.LetterTemplates.AddLetterTemplate.VisibleToExporter.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="visible_to_exporter",
                        options=[
                            Option(
                                key=True, value=strings.LetterTemplates.AddLetterTemplate.VisibleToExporter.YES_OPTION
                            ),
                            Option(
                                key=False, value=strings.LetterTemplates.AddLetterTemplate.VisibleToExporter.NO_OPTION
                            ),
                        ],
                    ),
                ],
                default_button_name=strings.LetterTemplates.AddLetterTemplate.VisibleToExporter.BUTTON,
            ),
            Form(
                title=strings.LetterTemplates.AddLetterTemplate.Layout.TITLE,
                questions=[RadioButtonsImage(name="layout", options=_letter_layout_options())],
                default_button_name=strings.LetterTemplates.AddLetterTemplate.Layout.CONTINUE_BUTTON,
            ),
        ]
    )


def edit_letter_template(letter_template, case_type_options, decision_options):
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
                name="case_types[]",
                options=case_type_options,
                classes=["govuk-checkboxes--small"],
            ),
            Checkboxes(
                title=strings.LetterTemplates.EditLetterTemplate.Decisions.TITLE,
                description=strings.LetterTemplates.EditLetterTemplate.Decisions.DESCRIPTION,
                name="decisions[]",
                options=decision_options,
                classes=["govuk-checkboxes--small"],
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
