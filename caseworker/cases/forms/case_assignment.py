from django import forms


class CaseAssignmentRemove(forms.Form):
    class Layout:
        DOCUMENT_TITLE = "Remove case adviser"

    assignment_id = forms.CharField(widget=forms.HiddenInput)


class CaseOfficerRemove(forms.Form):
    class Layout:
        DOCUMENT_TITLE = "Remove Licensing Unit case officer"
