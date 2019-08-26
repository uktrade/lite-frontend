from collections.abc import MutableMapping


def get_form_by_pk(pk, form_group):
    for form in form_group:
        if str(form.pk) == str(pk):
            return form
    return


def get_next_form_after_pk(pk, form_group):
    next_one = False
    for form in form_group:
        if next_one:
            return form
        if str(form.pk) == str(pk):
            next_one = True
    return


def remove_unused_errors(errors, form):
    """
    Removes all errors that don't belong to a form's fields
    :param errors: ['errors'] children
    :param form: Form object
    :return: Array of cleaned errors
    """
    cleaned_errors = {}

    for question in form.questions:
        if hasattr(question, 'name') and errors.get(question.name):
            cleaned_errors[question.name] = errors.get(question.name)

    return cleaned_errors


def nest_data(sent_data):
    """
    Nests strings into dictionaries eg
    {
        'site.name': 'SITE1'
    }
    becomes
    {
        'site': {
            'name': 'SITE1'
        }
    }
    """

    def _create_keys(d, keys, value):
        keys = keys.split(".")
        for k in keys[:-1]:
            if k not in d:
                d[k] = {}
            d = d[k]
        d[keys[-1]] = value

    data = {}

    for q, v in sent_data.items():
        _create_keys(data, q, v)

    return data


def flatten_data(d, parent_key='', sep='.'):
    """
    Flattens dictionaries eg
    {
        'site': {
            'name': 'SITE1'
        }
    }
    becomes
    {
        'site.name': 'SITE1'
    }
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_data(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)