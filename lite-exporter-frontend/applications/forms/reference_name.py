from applications.components import back_to_task_list
from lite_forms.components import Form, TextInput


def reference_name_form(application_id):
    return Form(
        title="Application reference",
        description="Name and save this application so you can refer back to it when needed.",
        questions=[TextInput(name="name"),],
        back_link=back_to_task_list(application_id),
    )
