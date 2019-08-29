from lite_forms.components import Form, TextInput

from core.builtins.custom_tags import get_string

form = Form(title=get_string('queues.queue_add.page_heading'), questions=[
    TextInput(title=get_string('queues.queue_add.question_title'),
              name='name'),
])

edit_form = Form(title=get_string('queues.queue_edit.page_heading'), questions=[
    TextInput(title=get_string('queues.queue_edit.question_title'),
              name='name'),
])
