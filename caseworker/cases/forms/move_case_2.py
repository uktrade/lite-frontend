from django.http import HttpRequest
from django.urls import reverse

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit, Layout, HTML
from django import forms
from django.template.loader import render_to_string
from lite_content.lite_internal_frontend.cases import Manage
from caseworker.queues.services import get_queues


class MoveCase(forms.Form):
    note = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

    def layout(self, context, request):
        self.helper.layout = Layout(
            HTML.h1(Manage.MoveCase.TITLE),
            Submit("Save", "Save"),
        )