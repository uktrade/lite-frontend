from lite_content.lite_internal_frontend import strings
from django.urls import reverse_lazy

from lite_forms.components import Form, TextInput, BackLink


form = Form(
    title=strings.Queues.QueueAdd.PAGE_HEADING,
    questions=[TextInput(title=strings.Queues.QueueAdd.QUESTION_TITLE, name="name")],
    back_link=BackLink("Back to queues", reverse_lazy("queues:queues")),
)

edit_form = Form(
    title=strings.Queues.QueueEdit.PAGE_HEADING,
    questions=[TextInput(title=strings.Queues.QueueEdit.QUESTION_TITLE, name="name")],
    back_link=BackLink("Back to queues", reverse_lazy("queues:queues")),
)
