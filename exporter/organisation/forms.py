from lite_forms.components import BackLink, DateInput, Form, FileUpload, TextInput


def attach_section_five_certificate_form(back_url):
    return Form(
        title="Attach your section five certificate",
        description="The file must be smaller than 50MB",
        questions=[
            FileUpload(),
            TextInput(name="reference_code", title="Certificate number",),
            DateInput(prefix="expiry_date_", title="Expiry date", description="For example 12 3 2021"),
        ],
        back_link=BackLink("Back", back_url),
    )
