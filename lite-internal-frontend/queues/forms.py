from core.builtins.custom_tags import get_string
from libraries.forms.components import Question, Form, InputType

form = Form(title=get_string('queues.queue_add.page_heading'), description='', caption='', questions=[
    Question(title=get_string('queues.queue_add.question_title'),
             description='',
             input_type=InputType.INPUT,
             name='name'),
])

edit_form = Form(title=get_string('queues.queue_edit.page_heading'), description='', caption='', questions=[
    Question(title=get_string('queues.queue_edit.question_title'),
             description='',
             input_type=InputType.INPUT,
             name='name'),
])
