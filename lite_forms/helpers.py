import copy
from collections.abc import MutableMapping

from markdown import markdown

from lite_forms.components import FormGroup


def get_form_by_pk(form_pk, form_group: FormGroup):
    for form in form_group.forms:
        if str(form.pk) == str(form_pk):
            return copy.deepcopy(form)
    return


def get_previous_form(form_pk, form_group: FormGroup):
    for form in form_group.forms:
        # If the current form is the final form in the group
        if int(form.pk) == int(form_pk) - 1:
            return copy.deepcopy(form)
    return


def get_next_form(form_pk, form_group: FormGroup):
    next_one = False
    for form in form_group.forms:
        if next_one:
            return copy.deepcopy(form)
        if str(form.pk) == str(form_pk):
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

    if not errors:
        return {}

    for question in form.questions:
        if hasattr(question, "name") and errors.get(question.name):
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


def flatten_data(d, parent_key="", sep="."):
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


def conditional(condition: bool, obj, else_obj=None):
    """
    Returns the object depending on a condition
    Optionally: returns else_obj if it is set
    """
    if condition:
        return obj

    return else_obj


def heading_used_as_label(components):
    single_input = None

    if components:
        for component in components:
            if hasattr(component, "title"):
                if single_input:
                    # If single_input has already been found, then we have multiple inputs
                    # and the heading cannot be used for multiple inputs
                    return None
                else:
                    single_input = component.name

    return single_input


def convert_to_markdown(text):
    if text:
        text = markdown(text, extensions=["nl2br"])
        # Replace leading (<p>) & trailing (</p>) p tags as they are not needed
        text = text.replace("<p>", "")
        text = text.replace("</p>", "")
        return text
    else:
        return None
