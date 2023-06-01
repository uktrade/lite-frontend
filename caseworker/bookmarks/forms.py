from django import forms
from django.forms.widgets import HiddenInput


class DeleteBookmark(forms.Form):
    id = forms.CharField(widget=HiddenInput)
    return_to = forms.CharField(widget=HiddenInput)
    name = forms.CharField(required=False)
    submit = forms.CharField()
