from libraries.forms.components import Question, Form, InputType

form = Form(title='Add Team', description='', caption='', questions=[
    Question(title='Name',
             description='',
             input_type=InputType.INPUT,
             name='name'),
])

edit_form = Form(title='Edit Team', description='', caption='', questions=[
    Question(title='Name',
             description='',
             input_type=InputType.INPUT,
             name='name'),
])
