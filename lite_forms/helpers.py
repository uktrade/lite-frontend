from collections.abc import MutableMapping

from django.shortcuts import render


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


def _create_keys(d, keys, value):
    keys = keys.split(".")
    for k in keys[:-1]:
        if k not in d:
            d[k] = {}
        d = d[k]
    d[keys[-1]] = value


def nest_data(sent_data):
    """
    Nests strings into dictionaries eg
    {
        'site.name': 'SITE1'
    }
    becomes
    {'site': {
            'name': 'SITE1'
        }
    }
    """
    data = {}

    for q, v in sent_data.items():
        _create_keys(data, q, v)

    return data


def flatten_data(d, parent_key='', sep='.'):
    """
    Flattens dictionaries eg
    {'site': {
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


def success_page(request, title, secondary_title, description, what_happens_next, links):
    context = {
        'title': title,
        'secondary_title': secondary_title,
        'description': description,
        'what_happens_next': what_happens_next,
        'links': links,
    }
    return render(request, 'confirmation.html', context)
