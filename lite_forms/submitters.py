from typing import Callable

from lite_forms.components import HiddenField, Form, FormGroup
from lite_forms.generators import form_page
from lite_forms.helpers import remove_unused_errors, nest_data, get_next_form, get_form_by_pk, flatten_data, \
    get_previous_form


def submit_single_form(request, form: Form, action: Callable, pk=None, override_data=None):
    data = request.POST.copy()

    if override_data:
        data = override_data

    if pk:
        validated_data, _ = action(request, pk, data)
    else:
        validated_data, _ = action(request, data)

    if 'errors' in validated_data:
        return form_page(request, form, data=data, errors=validated_data.get('errors')), None

    return None, validated_data


def _prepare_data(request, inject_data, expect_many_values):
    data = request.POST.copy()

    if inject_data:
        data = dict(list(inject_data.items()) + list(data.items()))

    # Remove form_pk and CSRF from POST data as the new form will replace them
    del data['form_pk']
    del data['csrfmiddlewaretoken']

    # Ensure data which is expected to have multiple values.
    for many_value_key in expect_many_values:
        data[many_value_key] = request.POST.getlist(many_value_key)

    # Post the data to the validator and check for errors
    return data, nest_data(data)


def submit_paged_form(
    request,
    form_group: FormGroup,
    action: Callable,
    object_pk=None,
    inject_data=None,
    expect_many_values=None,
):
    if expect_many_values is None:
        expect_many_values = []

    data, _ = _prepare_data(request, inject_data, expect_many_values)

    form_pk = request.POST.get('form_pk')
    previous_form = get_previous_form(form_pk, form_group)
    current_form = get_form_by_pk(form_pk, form_group)
    next_form = get_next_form(form_pk, form_group)

    if data.get('_action') and data.get('_action') == 'back':
        data = request.POST.copy()
        del data['form_pk']
        return form_page(request, previous_form, data=data, extra_data={'form_pk': previous_form.pk}), None

    if object_pk:
        validated_data, _ = action(request, object_pk, data)
    else:
        validated_data, _ = action(request, data)

    # If the API returns errors, add the existing questions to the reloaded form
    errors = validated_data.get('errors')

    if errors:
        errors = flatten_data(errors)
        errors = remove_unused_errors(errors, current_form)

    if errors:
        for key, value in data.items():
            exists = False

            for question in current_form.questions:
                if hasattr(question, 'name'):
                    if question.name == key:
                        exists = True
                        continue

            if not exists:
                current_form.questions.insert(0, HiddenField(key, value))

        return form_page(request, current_form, data=data, errors=errors, extra_data={'form_pk': current_form.pk}), validated_data

    # If there aren't any forms left to go through, return the data
    if next_form is None:
        return None, validated_data

    # Add existing post data to new form as hidden fields
    for key, value in data.items():
        if key in expect_many_values:
            for sub_value in value:
                next_form.questions.insert(0, HiddenField(key, sub_value))
        else:
            next_form.questions.insert(0, HiddenField(key, value))

    # Go to the next page
    return form_page(request, next_form, data=data, extra_data={'form_pk': next_form.pk}), validated_data
