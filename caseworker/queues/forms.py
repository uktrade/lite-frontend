from django import forms
from django.urls import reverse_lazy

from storages.backends.s3boto3 import S3Boto3StorageFile

from lite_content.lite_internal_frontend.queues import AddQueueForm, EditQueueForm
from lite_forms.components import Form, TextInput, BackLink, Select
from caseworker.queues.services import get_queues


def new_queue_form(request):
    return Form(
        title=AddQueueForm.TITLE,
        description=AddQueueForm.DESCRIPTION,
        questions=[
            TextInput(
                title=AddQueueForm.Name.TITLE,
                description=AddQueueForm.Name.DESCRIPTION,
                name="name",
            ),
            Select(
                title=AddQueueForm.CountersigningQueue.TITLE,
                description=AddQueueForm.CountersigningQueue.DESCRIPTION,
                options=get_queues(
                    request=request, disable_pagination=True, convert_to_options=True, users_team_first=True
                ),
                name="countersigning_queue",
            ),
        ],
        back_link=BackLink(AddQueueForm.BACK, reverse_lazy("queues:manage")),
    )


def remove_current_queue_id(options, queue_id):
    new_options = options
    for option in new_options:
        if option.key == str(queue_id):
            new_options.remove(option)
            break

    return new_options


def edit_queue_form(request, queue_id):
    return Form(
        title=EditQueueForm.TITLE,
        description=EditQueueForm.DESCRIPTION,
        questions=[
            TextInput(
                title=EditQueueForm.Name.TITLE,
                description=EditQueueForm.Name.DESCRIPTION,
                name="name",
            ),
            Select(
                title=EditQueueForm.CountersigningQueue.TITLE,
                description=EditQueueForm.CountersigningQueue.DESCRIPTION,
                options=remove_current_queue_id(
                    get_queues(
                        request=request, disable_pagination=True, convert_to_options=True, users_team_first=True
                    ),
                    queue_id,
                ),
                name="countersigning_queue",
            ),
        ],
        back_link=BackLink(EditQueueForm.BACK, reverse_lazy("queues:manage")),
    )


class EnforcementXMLImportForm(forms.Form):

    file = forms.FileField(label="Upload a file", widget=forms.FileInput(attrs={"accept": "text/xml"}))

    # the CreateView expects `instance` to be passed in here
    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_file(self):
        value = self.cleaned_data["file"]
        if isinstance(value, S3Boto3StorageFile):
            s3_obj = value.obj.get()["Body"]
            return s3_obj.read().decode("utf-8")

        return value.read().decode("utf-8")

    def save(self):
        # the CreateView expects this method
        pass
