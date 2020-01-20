from lite_content.lite_internal_frontend import strings
from django.urls import reverse_lazy

from lite_forms.components import Form, TextInput, BackLink


def new_queue_form():
    return Form(
        title=strings.Queues.QueueAdd.TITLE,
        description=strings.Queues.QueueAdd.DESCRIPTION,
        questions=[
            TextInput(
                title=strings.Queues.QueueAdd.Name.TITLE,
                description=strings.Queues.QueueAdd.Name.DESCRIPTION,
                name="name",
            )
        ],
        back_link=BackLink(strings.Queues.QueueAdd.BACK, reverse_lazy("queues:queues")),
    )


def edit_queue_form():
    return Form(
        title=strings.Queues.QueueEdit.TITLE,
        description=strings.Queues.QueueEdit.DESCRIPTION,
        questions=[
            TextInput(
                title=strings.Queues.QueueEdit.Name.TITLE,
                description=strings.Queues.QueueEdit.Name.DESCRIPTION,
                name="name",
            )
        ],
        back_link=BackLink(strings.Queues.QueueEdit.BACK, reverse_lazy("queues:queues")),
    )
