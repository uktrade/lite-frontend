from django import forms


class DenialUploadForm(forms.Form):

    csv_file = forms.FileField(label="Upload a file")

    # the CreateView expects `instance` to be passed in here
    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_csv_file(self):
        value = self.cleaned_data["csv_file"]
        return value.read().decode("utf-8")

    def save(self):
        # the CreateView expects this method
        pass
