from applications.components import back_to_task_list
from lite_forms.components import Form, TextInput


def reference_name_form(application_id):
    return Form(
        title="Enter a reference name for this application",
        description="This will make it easier for you or your organisation to find in the future.",
        questions=[TextInput(name="name"),],
        back_link=back_to_task_list(application_id),
    )
