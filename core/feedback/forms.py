from django import forms


class FeedbackForm(forms.Form):
    feedback = forms.CharField(label="Please type your feedback here: ", widget=forms.Textarea)
