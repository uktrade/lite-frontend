from django import forms


class CaseAssignmentRemove(forms.Form):
    assignment_id = forms.CharField(widget=forms.HiddenInput)
