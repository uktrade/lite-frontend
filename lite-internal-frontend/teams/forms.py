from lite_forms.components import Form, TextInput

form = Form(title="Add Team", questions=[TextInput(title="Name", name="name"),])

edit_form = Form(title="Edit Team", questions=[TextInput(title="Name", name="name"),])
