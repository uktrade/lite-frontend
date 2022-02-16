from django.urls import reverse_lazy

from caseworker.cases.services import get_case_types
from caseworker.core.services import get_countries, get_control_list_entries
from caseworker.flags.services import get_goods_flags, get_destination_flags, get_cases_flags
from caseworker.flags.enums import FlagPermissions

from lite_content.lite_internal_frontend import strings
from lite_content.lite_internal_frontend.flags import CreateFlagForm, EditFlagForm, SetFlagsForm
from lite_content.lite_internal_frontend.strings import FlaggingRules
from lite_forms.components import (
    TextInput,
    Select,
    Option,
    BackLink,
    Form,
    FormGroup,
    RadioButtons,
    NumberInput,
    DetailComponent,
    TextArea,
    Checkboxes,
    HelpSection,
    Filter,
    TokenBar,
    Heading,
)
from lite_forms.generators import confirm_form
from lite_forms.styles import HeadingStyle

level_options = [
    Option("Case", "Case"),
    Option("Organisation", "Organisation"),
    Option("Destination", "Destination"),
    Option("Good", "Good"),
]


_levels = [
    Option(key="Good", value=strings.FlaggingRules.Create.Type.GOOD),
    Option(key="Destination", value=strings.FlaggingRules.Create.Type.DESTINATION),
    Option(key="Case", value=strings.FlaggingRules.Create.Type.APPLICATION),
]


def add_flag_form():
    return Form(
        title=CreateFlagForm.TITLE,
        description=CreateFlagForm.DESCRIPTION,
        questions=[
            TextInput(title=CreateFlagForm.Name.TITLE, description=CreateFlagForm.Name.DESCRIPTION, name="name"),
            Select(
                title=CreateFlagForm.Level.TITLE,
                description=CreateFlagForm.Level.DESCRIPTION,
                name="level",
                options=level_options,
            ),
            RadioButtons(
                title=CreateFlagForm.Colour.TITLE,
                description=CreateFlagForm.Colour.DESCRIPTION,
                name="colour",
                classes=["app-radios--flag-colours"],
                options=[
                    Option("default", "Default"),
                    Option("red", "Red", classes=["app-radios__item--red"]),
                    Option("yellow", "Yellow", classes=["app-radios__item--yellow"]),
                    Option("green", "Green", classes=["app-radios__item--green"]),
                    Option("blue", "Blue", classes=["app-radios__item--blue"]),
                    Option("purple", "Purple", classes=["app-radios__item--purple"]),
                    Option("orange", "Orange", classes=["app-radios__item--orange"]),
                    Option("brown", "Brown", classes=["app-radios__item--brown"]),
                    Option("turquoise", "Turquoise", classes=["app-radios__item--turquoise"]),
                    Option("pink", "Pink", classes=["app-radios__item--pink"]),
                ],
            ),
            TextInput(
                name="label",
                title=CreateFlagForm.Label.TITLE,
                description=CreateFlagForm.Label.DESCRIPTION,
            ),
            NumberInput(
                name="priority", title=CreateFlagForm.Priority.TITLE, description=CreateFlagForm.Priority.DESCRIPTION
            ),
            RadioButtons(
                name="blocks_finalising",
                title=CreateFlagForm.BlocksFinalising.TITLE,
                options=[
                    Option(
                        key=True,
                        value=CreateFlagForm.BlocksFinalising.YES,
                        components=[
                            RadioButtons(
                                name="removable_by",
                                title="Who can remove this flag?",
                                options=[
                                    Option(FlagPermissions.DEFAULT, FlagPermissions.DEFAULT),
                                    Option(
                                        FlagPermissions.AUTHORISED_COUNTERSIGNER,
                                        FlagPermissions.AUTHORISED_COUNTERSIGNER,
                                    ),
                                    Option(
                                        FlagPermissions.HEAD_OF_LICENSING_UNIT_COUNTERSIGNER,
                                        FlagPermissions.HEAD_OF_LICENSING_UNIT_COUNTERSIGNER,
                                    ),
                                ],
                            )
                        ],
                    ),
                    Option(key=False, value=CreateFlagForm.BlocksFinalising.NO),
                ],
                classes=["govuk-radios--inline"],
            ),
        ],
        default_button_name=CreateFlagForm.SUBMIT_BUTTON,
        back_link=BackLink(CreateFlagForm.BACK_LINK, reverse_lazy("flags:flags")),
        javascript_imports={"/javascripts/add-edit-flags.js"},
    )


def edit_flag_form():
    return Form(
        title=EditFlagForm.TITLE,
        questions=[
            TextInput(title=EditFlagForm.Name.TITLE, description=EditFlagForm.Name.DESCRIPTION, name="name"),
            RadioButtons(
                title=EditFlagForm.Colour.TITLE,
                description=EditFlagForm.Colour.DESCRIPTION,
                name="colour",
                classes=["app-radios--flag-colours"],
                options=[
                    Option("default", "Default"),
                    Option("red", "Red", classes=["app-radios__item--red"]),
                    Option("yellow", "Yellow", classes=["app-radios__item--yellow"]),
                    Option("green", "Green", classes=["app-radios__item--green"]),
                    Option("blue", "Blue", classes=["app-radios__item--blue"]),
                    Option("purple", "Purple", classes=["app-radios__item--purple"]),
                    Option("orange", "Orange", classes=["app-radios__item--orange"]),
                    Option("brown", "Brown", classes=["app-radios__item--brown"]),
                    Option("turquoise", "Turquoise", classes=["app-radios__item--turquoise"]),
                    Option("pink", "Pink", classes=["app-radios__item--pink"]),
                ],
            ),
            TextInput(name="label", title=EditFlagForm.Label.TITLE, description=EditFlagForm.Label.DESCRIPTION),
            NumberInput(
                name="priority", title=EditFlagForm.Priority.TITLE, description=EditFlagForm.Priority.DESCRIPTION
            ),
            RadioButtons(
                name="blocks_finalising",
                title=EditFlagForm.BlocksFinalising.TITLE,
                options=[
                    Option(
                        key=True,
                        value=EditFlagForm.BlocksFinalising.YES,
                        components=[
                            RadioButtons(
                                name="removable_by",
                                title="Who can remove this flag?",
                                options=[
                                    Option(FlagPermissions.DEFAULT, FlagPermissions.DEFAULT),
                                    Option(
                                        FlagPermissions.AUTHORISED_COUNTERSIGNER,
                                        FlagPermissions.AUTHORISED_COUNTERSIGNER,
                                    ),
                                    Option(
                                        FlagPermissions.HEAD_OF_LICENSING_UNIT_COUNTERSIGNER,
                                        FlagPermissions.HEAD_OF_LICENSING_UNIT_COUNTERSIGNER,
                                    ),
                                ],
                            )
                        ],
                    ),
                    Option(False, EditFlagForm.BlocksFinalising.NO),
                ],
            ),
        ],
        back_link=BackLink(EditFlagForm.BACK_LINK, reverse_lazy("flags:flags")),
        default_button_name=EditFlagForm.SUBMIT_BUTTON,
        javascript_imports={"/javascripts/add-edit-flags.js"},
    )


def select_flagging_rule_type():
    return Form(
        title=strings.FlaggingRules.Create.Type.TITLE,
        questions=[
            RadioButtons(
                name="level",
                options=_levels,
            )
        ],
        back_link=BackLink(strings.FlaggingRules.Create.BACKLINK, reverse_lazy("flags:flagging_rules")),
        default_button_name=strings.FlaggingRules.Create.Type.SAVE,
    )


def get_clc_entry_groups_and_nodes(entries):
    groups = []
    nodes = []

    for item in entries:
        if not item["parent_id"] and not item.get("children"):
            nodes.append({"rating": item["rating"], "text": item["text"]})
            groups.append({"rating": item["rating"], "text": item["text"]})

        if item["parent_id"] and item.get("children"):
            nodes.append({"rating": item["rating"], "text": item["text"]})

        if item.get("children"):
            groups.append({"rating": item["rating"], "text": item["text"]})
            children, child_nodes = get_clc_entry_groups_and_nodes(item["children"])
            if children:
                groups.extend(children)
            if child_nodes:
                nodes.extend(child_nodes)
        elif item["parent_id"]:
            nodes.append({"rating": item["rating"], "text": item["text"]})

    return groups, nodes


def select_condition_and_flag(request, type: str):
    flags = []
    is_for_verified_goods_only = None

    if type == "Good":
        flags = get_goods_flags(request=request)
        is_for_verified_goods_only = RadioButtons(
            name="is_for_verified_goods_only",
            options=[
                Option(key=True, value=FlaggingRules.Create.Condition_and_flag.YES_OPTION),
                Option(key=False, value=FlaggingRules.Create.Condition_and_flag.NO_OPTION),
            ],
            title=FlaggingRules.Create.Condition_and_flag.GOODS_QUESTION,
        )
        entries = get_control_list_entries(request)
        clc_groups, clc_nodes = get_clc_entry_groups_and_nodes(entries)

        # if the child node has children of its own then that needs to selectable as
        # both individual entry as well as group entry because of this duplicates are
        # possible in the combined list hence remove them. We need groups at the top
        # because autocomplete only shows first 10 entries which makes it difficult to
        # select certain groups otherwise. eg ML10b1 comes before ML1
        combined_entries = list(clc_groups)
        rating_seen = set([item["rating"] for item in combined_entries])
        for item in clc_nodes:
            if item["rating"] not in rating_seen:
                rating_seen.add(item["rating"])
                combined_entries.append(item)

        clc_nodes_options = [
            Option(
                key=item["rating"],
                value=item["rating"],
                description=item["text"],
            )
            for item in clc_nodes
        ]

        clc_groups_options = [
            Option(
                key=item["rating"],
                value=item["rating"],
                description=item["text"],
            )
            for item in clc_groups
        ]

        clc_combined_options = [
            Option(
                key=item["rating"],
                value=item["rating"],
                description=item["text"],
            )
            for item in combined_entries
        ]

        return Form(
            title="Set flagging rules",
            questions=[
                Heading("Add a condition", HeadingStyle.S),
                TokenBar(
                    title="Select individual control list entries",
                    name="matching_values",
                    description="Type to get suggestions. For example, ML1a.",
                    options=clc_nodes_options,
                ),
                TokenBar(
                    title="Select a control list entry group",
                    name="matching_groups",
                    description="Type to get suggestions. For example, ML8.\nThis will add every control list entry under ML8.",
                    options=clc_groups_options,
                ),
                TokenBar(
                    title="Excluded control list entries",
                    name="excluded_values",
                    description="Type to get suggestions. For example, ML1a, ML8.\nThis will exclude ML1a and every control list entry under ML8.",
                    options=clc_combined_options,
                ),
                Heading("Set an action", HeadingStyle.S),
                Select(title=strings.FlaggingRules.Create.Condition_and_flag.FLAG, name="flag", options=flags),
                is_for_verified_goods_only,
            ],
            default_button_name="Create flagging rule",
        )
    elif type == "Destination":
        flags = get_destination_flags(request=request)

        return Form(
            title="Set flagging rules",
            questions=[
                Heading("Add a condition", HeadingStyle.S),
                TokenBar(
                    title="Select destinations",
                    name="matching_values",
                    description="Type to get suggestions. For example, Australia",
                    options=get_countries(request, convert_to_options=True),
                ),
                Heading("Add an action", HeadingStyle.S),
                Select(title=strings.FlaggingRules.Create.Condition_and_flag.FLAG, name="flag", options=flags),
            ],
            default_button_name="Create flagging rule",
        )
    elif type == "Case":
        case_type_options = [Option(option["key"], option["value"]) for option in get_case_types(request)]
        flags = get_cases_flags(request=request)

        return Form(
            title="Set flagging rules",
            questions=[
                Heading("Add a condition", HeadingStyle.S),
                TokenBar(
                    title="Select application type",
                    name="matching_values",
                    description="Type to get suggestions.\nFor example, Standard Individual Export Licence",
                    options=case_type_options,
                ),
                Heading("Add an action", HeadingStyle.S),
                Select(title=strings.FlaggingRules.Create.Condition_and_flag.FLAG, name="flag", options=flags),
            ],
            default_button_name="Create flagging rule",
        )


def create_flagging_rules_formGroup(request=None, type=None):
    return FormGroup(
        [select_flagging_rule_type(), select_condition_and_flag(request=request, type=type)],
    )


def deactivate_or_activate_flagging_rule_form(title, description, confirm_text, status):
    return confirm_form(
        title=title,
        description=description,
        back_link_text=strings.FlaggingRules.Status.BACK,
        back_url=reverse_lazy("flags:flagging_rules"),
        yes_label=confirm_text,
        no_label=strings.FlaggingRules.Status.CANCEL,
        hidden_field=status,
        confirmation_name="confirm",
    )


def set_flags_form(flags, level, show_case_header=False, show_sidebar=False):
    form = Form(
        title=getattr(SetFlagsForm, level).TITLE,
        description=getattr(SetFlagsForm, level).DESCRIPTION,
        questions=[
            Filter(placeholder=getattr(SetFlagsForm, level).FILTER),
            Checkboxes(
                name="flags[]",
                options=flags,
                filterable=True,
                disabled_hint="You do not have permission to remove this flag.",
            ),
            DetailComponent(
                title=getattr(SetFlagsForm, level).Note.TITLE,
                components=[
                    TextArea(name="note", classes=["govuk-!-margin-0"]),
                ],
            ),
        ],
        default_button_name=getattr(SetFlagsForm, level).SUBMIT_BUTTON,
        container="case" if show_case_header else "two-pane",
        javascript_imports={"/javascripts/flags-permission-hints.js"},
    )

    if show_sidebar:
        form.helpers = [HelpSection("Setting flags on:", "", includes="case/includes/selection-sidebar.html")]

    return form
