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


def create_keys(d, keys, value):
    keys = keys.split(".")
    for k in keys[:-1]:
        if k not in d:
            d[k] = {}
        d = d[k]
    d[keys[-1]] = value


def nest_data(sent_data):
    data = {}

    for q, v in sent_data.items():
        create_keys(data, q, v)

    return data
