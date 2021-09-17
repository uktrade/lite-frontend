from django.http import HttpRequest
from django.urls import reverse

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit, Layout, HTML
from django import forms
from django.template.loader import render_to_string
from lite_content.lite_internal_frontend.cases import Manage
from caseworker.queues.services import get_queues


class SiteFormMixin:
    @property
    def serialized_data(self):
        data = self.cleaned_data.copy()
        return data

    def add_form_errors(self, errors):
        for key, value in errors.items():
            if key in self.declared_fields:
                self.add_error(key, value)

    def clean(self):
        return self.cleaned_data

    def flatten_errors(self, errors):
        if errors.get("address"):
            if isinstance(errors["address"], list):
                del errors["address"]
            elif isinstance(errors["address"], dict):
                return {**errors, **errors.pop("address")}
        return errors


class MoveCase(SiteFormMixin, forms.Form):
    note = forms.CharField(required=False)
    queues = forms.ChoiceField(
        label="", choices=[], widget=forms.CheckboxSelectMultiple(), required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    def layout(self, context, request):
        queue_data = get_queues(request)
        self.declared_fields["queues"].choices = [
            (q["name"], q["team"]["name"])
            for q in queue_data
        ]
        self.helper.layout = Layout(
            HTML.h1(Manage.MoveCase.TITLE),
            HTML(render_to_string("forms/filter.html")) if queue_data else None,
            "queues" if queue_data else HTML.warning("No items"),
            Submit("Save", "Save"),
        )