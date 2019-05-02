def get_form_by_pk(pk, section):
    for form in section.forms:
        if form.pk == pk:
            return form
    return


def get_next_form_after_pk(pk, section):
    next_one = False
    for form in section.forms:
        if next_one:
            return form
        if str(form.pk) == str(pk):
            next_one = True
    return
