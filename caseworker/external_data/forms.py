from django import forms

from storages.backends.s3boto3 import S3Boto3StorageFile


class DenialUploadForm(forms.Form):

    csv_file = forms.FileField(label="Upload a file")

    # the CreateView expects `instance` to be passed in here
    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_csv_file(self):
        value = self.cleaned_data["csv_file"]
        if isinstance(value, S3Boto3StorageFile):
            s3_obj = value.obj.get()["Body"]
            return s3_obj.read().decode("utf-8")

        return value.read().decode("utf-8")

    def save(self):
        # the CreateView expects this method
        pass


class DenialRevoke(forms.Form):
    comment = forms.CharField(label="Enter a reason why this denial should be revoked", widget=forms.Textarea)
