from django.http import HttpRequest

from lite_forms.components import HiddenField, Form, FormGroup
from lite_forms.generators import form_page
from lite_forms.helpers import remove_unused_errors, nest_data, get_next_form_after_pk, get_form_by_pk


def submit_single_form(request: HttpRequest, form: Form, post_to, pk=None, override_data=None):
    data = request.POST.copy()

    if override_data:
        data = override_data

    if pk:
        validated_data, status_code = post_to(request, pk, data)
    else:
        validated_data, status_code = post_to(request, data)

    if 'errors' in validated_data:
        return form_page(request, form, data=data, errors=validated_data.get('errors')), None

    return None, validated_data


def submit_paged_form(request: HttpRequest, form_group: FormGroup, post_to, pk=None):
    data = request.POST.copy()

    # Get the next form based off form_pk
    current_form = get_form_by_pk(data.get('form_pk'), form_group)
    next_form = get_next_form_after_pk(data.get('form_pk'), form_group)

    # Remove form_pk and CSRF from POST data as the new form will replace them
    del data['form_pk']
    del data['csrfmiddlewaretoken']

    # Post the data to the validator and check for errors
    nested_data = nest_data(data)
    if pk:
        validated_data, status_code = post_to(request, pk, nested_data)
    else:
        validated_data, status_code = post_to(request, nested_data)

    # If the API returns errors, add the existing questions to the reloaded form
    if remove_unused_errors(validated_data.get('errors'), current_form):
        errors = validated_data.get('errors')

        for question in current_form.questions:
            if hasattr(question, 'name') and errors.get(question.name):
                current_form.questions.append(HiddenField(question.name, errors.get(question.name)))

        return form_page(request, current_form, data=data, errors=validated_data['errors']), validated_data

    # If there aren't any forms left to go through, return the data
    if next_form is None:
        return None, validated_data

    # Add existing post data to new form as hidden fields
    for key, value in data.items():
        next_form.questions.append(HiddenField(key, value))

    # Go to the next page
    return form_page(request, next_form), validated_data
