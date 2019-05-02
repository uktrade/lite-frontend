def get_form_by_id(id, sections):
    for form in sections.forms:
        if form.id == id:
            return form
    return


def get_next_form_after_id(id, sections):
    next_one = False
    for form in sections.forms:
        if next_one:
            return form
        if form.id == id:
            next_one = True
    return
