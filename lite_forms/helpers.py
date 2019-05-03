def get_form_by_pk(pk, section):
    for form in section.forms:
        if str(form.pk) == str(pk):
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


def nest_data(sent_data):
    data = {}

    for q, v in sent_data.items():
        if '.' not in q:
            data[q] = v
            continue

        nest_name = q.split('.')[0]

        if nest_name not in data:
            data[nest_name] = {}

        data[nest_name][q.split('.')[1]] = v

    return data
