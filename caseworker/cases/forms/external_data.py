from django import forms


class SanctionRevoke(forms.Form):
    comment = forms.CharField(label="Enter a reason why this sanction match should be removed", widget=forms.Textarea)
