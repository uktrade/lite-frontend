from django.urls import reverse_lazy

from lite_content.lite_internal_frontend.queues import AddQueueForm, EditQueueForm
from lite_forms.components import Form, TextInput, BackLink


def new_queue_form():
    return Form(
        title=AddQueueForm.TITLE,
        description=AddQueueForm.DESCRIPTION,
        questions=[TextInput(title=AddQueueForm.Name.TITLE, description=AddQueueForm.Name.DESCRIPTION, name="name",)],
        back_link=BackLink(AddQueueForm.BACK, reverse_lazy("queues:manage")),
    )


def edit_queue_form():
    return Form(
        title=EditQueueForm.TITLE,
        description=EditQueueForm.DESCRIPTION,
        questions=[TextInput(title=EditQueueForm.Name.TITLE, description=EditQueueForm.Name.DESCRIPTION, name="name",)],
        back_link=BackLink(EditQueueForm.BACK, reverse_lazy("queues:manage")),
    )
