import csv
import io
import os

from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings

from storages.backends.s3boto3 import S3Boto3StorageFile


class DenialUploadForm(forms.Form):

    csv_file = forms.FileField(label="Upload a file")

    # the CreateView expects `instance` to be passed in here
    def __init__(self, instance, *args, **kwargs):
        self.set_required_headers_from_example_csv()
        super().__init__(*args, **kwargs)

    def set_required_headers_from_example_csv(self):
        # Set required_headers from the example csv so they stay up to date
        file_path = os.path.join(settings.BASE_DIR, "caseworker/external_data/example.csv")
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.required_headers = reader.fieldnames

    def clean_csv_file(self):
        value = self.cleaned_data["csv_file"]
        if isinstance(value, S3Boto3StorageFile):
            s3_obj = value.obj.get()["Body"]
            return s3_obj.read().decode("utf-8")
        value = value.read().decode("utf-8")

        csv_file = io.StringIO(value)
        reader = csv.DictReader(csv_file)
        # Check if required headers are present
        if not (set(self.required_headers)).issubset(set(reader.fieldnames)):  # type: ignore
            raise ValidationError("Missing required headers in CSV file")

        return value

    def save(self):
        # the CreateView expects this method
        pass


class DenialRevoke(forms.Form):
    comment = forms.CharField(label="Enter a reason why this denial should be revoked", widget=forms.Textarea)
