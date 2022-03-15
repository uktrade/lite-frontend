create = {
    "name": "application",
    "application_type": "siel",
    "export_type": "permanent",
    "have_you_been_informed": "yes",
    "reference_number_on_information_form": "42693635",
}


submit = {
    "submit_declaration": True,
    "agreed_to_foi": True,
    "agreed_to_declaration": True,
    "foi_reason": "No objection",
    "agreed_to_declaration_text": "I AGREE",
}


def status(status):
    return {"status": status}
