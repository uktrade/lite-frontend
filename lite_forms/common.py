from lite_forms.components import TextInput, Select, ControlListEntryInput


def country_question(countries, prefix="address."):
    return Select(title="Country", name=prefix + "country", options=countries)


def address_questions(countries, prefix="address."):
    return [
        TextInput(title="Building and street", accessible_description="line 1 of 2", name=prefix + "address_line_1",),
        TextInput(title="", accessible_description="line 2 of 2", name=prefix + "address_line_2",),
        TextInput(title="Town or city", name=prefix + "city"),
        TextInput(title="County or state", name=prefix + "region"),
        TextInput(title="Postcode", name=prefix + "postcode"),
        country_question(countries, prefix),
    ]


def control_list_entry_question(
    control_list_entries,
    title="Control list classification",
    description="For example, ML1a",
    name="control_list_entry",
    inset_text=True,
):
    classes = ["govuk-inset-text"] if inset_text else []
    return ControlListEntryInput(
        title=title, name=name, description=description, options=control_list_entries, classes=classes,
    )


def pv_grading_question(
    pv_gradings,
    title="PV grading",
    description="For example, UK OFFICIAL-SENSITIVE",
    name="pv_grading",
    inset_text=True,
):
    classes = ["govuk-inset-text"] if inset_text else []
    return ControlListEntryInput(title=title, name=name, description=description, options=pv_gradings, classes=classes,)
