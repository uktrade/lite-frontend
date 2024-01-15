from django import forms


class CloseQuery(forms.Form):
    reason_for_closing_query = forms.CharField(widget=forms.Textarea, label="", required=False)
