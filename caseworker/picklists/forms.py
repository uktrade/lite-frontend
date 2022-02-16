from django.urls import reverse_lazy

from lite_content.lite_internal_frontend import picklists
from lite_forms.components import TextInput, TextArea, Form, Button, MarkdownArea, HiddenField, BackLink, HelpSection
from lite_forms.styles import ButtonStyle


def add_picklist_item_form(picklist_type):
    return Form(
        title=getattr(picklists.NewPicklistForm, picklist_type.upper()),
        questions=[
            TextInput(
                title=picklists.NewPicklistForm.Name.TITLE, name="name", classes=["govuk-!-width-three-quarters"]
            ),
            HiddenField("type", picklist_type),
            TextArea(
                title=picklists.NewPicklistForm.Text.TITLE,
                name="text",
                rows=20,
                extras={
                    "max_length": 5000,
                },
                classes=["govuk-!-width-three-quarters"],
            ),
        ],
        back_link=BackLink(
            picklists.NewPicklistForm.BACK_LINK, reverse_lazy("picklists:picklists") + f"?type={picklist_type}"
        ),
    )


def edit_picklist_item_form(picklist_item):
    return Form(
        title="Edit " + picklist_item["name"],
        questions=[
            TextInput(title="Name", name="name"),
            HiddenField("type", picklist_item["type"]["key"]),
            TextArea(
                title="Text",
                name="text",
                extras={
                    "max_length": 5000,
                },
            ),
        ],
        back_link=BackLink(
            "Back to " + picklist_item["name"],
            reverse_lazy("picklists:picklist_item", kwargs={"pk": picklist_item["id"]}),
        ),
        default_button_name="Save",
    )


def add_letter_paragraph_form(picklist_type):
    return Form(
        title=picklists.NewPicklistForm.LETTER_PARAGRAPH,
        questions=[
            HiddenField("type", picklist_type),
            TextInput(title=picklists.NewPicklistForm.Name.TITLE, name="name", classes=["govuk-!-width-full"]),
            MarkdownArea(
                title=picklists.NewPicklistForm.Text.TITLE,
                name="text",
                extras={
                    "max_length": 5000,
                },
            ),
        ],
        helpers=[HelpSection(picklists.NewPicklistForm.HELP, None, "teams/markdown-help.html")],
    )


def edit_letter_paragraph_form(picklist_item):
    return Form(
        title=picklists.NewPicklistForm.EDIT_PREFIX + " " + picklist_item["name"],
        questions=[
            HiddenField("type", picklist_item["type"]["key"]),
            TextInput(title=picklists.NewPicklistForm.Name.TITLE, name="name", classes=["govuk-!-width-full"]),
            MarkdownArea(
                title=picklists.NewPicklistForm.Text.TITLE,
                name="text",
                extras={
                    "max_length": 5000,
                },
            ),
        ],
        helpers=[HelpSection(picklists.NewPicklistForm.HELP, None, "teams/markdown-help.html")],
    )


def deactivate_picklist_item(picklist_item):
    return Form(
        title="Are you sure you want to deactivate " + picklist_item["name"] + "?",
        description="You can always reactivate it later if need be.",
        questions=[],
        back_link=BackLink("Back", reverse_lazy("picklists:edit", kwargs={"pk": picklist_item["id"]})),
        buttons=[
            Button("Deactivate", "submit", ButtonStyle.WARNING),
            Button(
                "Cancel",
                "cancel",
                ButtonStyle.SECONDARY,
                reverse_lazy("picklists:edit", kwargs={"pk": picklist_item["id"]}),
            ),
        ],
    )


def reactivate_picklist_item(picklist_item):
    return Form(
        title="Are you sure you want to reactivate " + picklist_item["name"] + "?",
        description="You can always deactivate it later if need be.",
        questions=[],
        back_link=BackLink("Back", reverse_lazy("picklists:edit", kwargs={"pk": picklist_item["id"]})),
        buttons=[
            Button("Reactivate", "submit", ButtonStyle.DEFAULT),
            Button(
                "Cancel",
                "cancel",
                ButtonStyle.SECONDARY,
                reverse_lazy("picklists:edit", kwargs={"pk": picklist_item["id"]}),
            ),
        ],
    )
