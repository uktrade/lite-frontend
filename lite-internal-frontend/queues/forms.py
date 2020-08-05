from django.urls import reverse_lazy

from lite_content.lite_internal_frontend.queues import AddQueueForm, EditQueueForm
from lite_forms.components import Form, TextInput, BackLink, Select
from queues.services import get_queues


def new_queue_form(request):
    return Form(
        title=AddQueueForm.TITLE,
        description=AddQueueForm.DESCRIPTION,
        questions=[
            TextInput(title=AddQueueForm.Name.TITLE, description=AddQueueForm.Name.DESCRIPTION, name="name",),
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
            TextInput(title=EditQueueForm.Name.TITLE, description=EditQueueForm.Name.DESCRIPTION, name="name",),
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
