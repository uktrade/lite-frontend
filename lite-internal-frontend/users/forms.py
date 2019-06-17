from libraries.forms.components import Question, Form, InputType, ArrayQuestion


def add_user_form(teams):
    return Form(title='Add User', description='', caption='', questions=[
            Question(title='Email',
                     description='',
                     input_type=InputType.INPUT,
                     name='email'),
            ArrayQuestion(title='Team',
                          description='',
                          input_type=InputType.SELECT,
                          name='team',
                          data=teams),
        ])


def edit_user_form(teams):
    return Form(title='Edit User', description='', caption='', questions=[
            Question(title='Email',
                     description='',
                     input_type=InputType.INPUT,
                     name='email'),
            ArrayQuestion(title='Team',
                          description='',
                          input_type=InputType.SELECT,
                          name='team',
                          data=teams),
        ])
