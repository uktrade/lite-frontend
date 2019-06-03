from libraries.forms.components import Question, Form, InputType

form = Form(title='Add Department', description='', caption='', questions=[
    Question(title='Name',
             description='',
             input_type=InputType.INPUT,
             name='name'),
])

edit_form = Form(title='Edit Department', description='', caption='', questions=[
    Question(title='Name',
             description='',
             input_type=InputType.INPUT,
             name='name'),
])
