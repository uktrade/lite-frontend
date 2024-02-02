from core.common.forms import BaseForm
from django import forms
from django.template.loader import render_to_string

from crispy_forms_gds.layout import HTML, Button
from django.template.defaultfilters import linebreaksbr


class ECJUQueryRespondForm(BaseForm):
    class Layout:
        TITLE = "Respond to query"

    response = forms.CharField(
        label="Send a message to the exporter (optional)",
        widget=forms.Textarea(attrs={"rows": 7, "class": "govuk-!-margin-top-4"}),
        required=False,
    )

    def __init__(
        self,
        ecju_query,
        documents,
        case_id,
        ecju_response,
        *args,
        **kwargs,
    ):

        self.ecju_query = ecju_query
        self.case_id = case_id
        self.ecju_response = ecju_response
        self.documents = documents

        self.declared_fields["response"] = forms.CharField(
            initial=self.ecju_response,
            label="Send a message to the exporter (optional)",
            required=False,
            widget=forms.Textarea(attrs={"id": "response", "rows": 7, "class": "govuk-!-margin-top-4"}),
        )

        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return [
            HTML.p(f'<div class="app-ecju-query__text"> {linebreaksbr(self.ecju_query["question"]) }</div>'),
            HTML.p("Your application will be paused until the caseworker receives a response. To reply: "),
            HTML.p("1. Edit and submit your application as required or send a written message below."),
            HTML.p("2. Then select 'Continue' to notify the case worker that the query has been answered."),
            "response",
            HTML.p("<div class=" "govuk-hint" ">You can enter upto 2200 characters</div>"),
            HTML.h2("Documents"),
            Button.secondary("add_document", "Attach a document"),
            HTML(
                render_to_string(
                    "ecju-queries/ecju-documents.html",
                    {"documents": self.documents, "ecju_query": self.ecju_query, "case_id": self.case_id},
                )
            ),
            HTML.p(""),
        ]

    def get_layout_actions(self):
        layout_actions = super().get_layout_actions()

        layout_actions.append(
            Button.secondary("cancel", "Cancel"),
        )

        return layout_actions


class ECJUQueryRespondConfirmForm(BaseForm):
    class Layout:
        TITLE = "Confirm you have responsed to this query"

    def get_layout_fields(self):
        return []

    def get_layout_actions(self):
        layout_actions = super().get_layout_actions()

        layout_actions.append(
            Button.secondary("cancel", "Cancel"),
        )

        return layout_actions
