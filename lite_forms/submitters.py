from typing import Callable

from django.http import QueryDict

from lite_forms.components import HiddenField, Form, FormGroup
from lite_forms.generators import form_page
from lite_forms.helpers import (
    remove_unused_errors,
    nest_data,
    get_next_form,
    get_form_by_pk,
    flatten_data,
    get_previous_form,
    handle_lists,
)


def submit_single_form(request, form: Form, action: Callable, object_pk=None, override_data=None):
    """
    Function to handle the submission of data for a single, supplied form.

    :param request: Standard Django request object
    :param form: The Form for which to handle a submit
    :param action: The callback action to be invoked to submit the form's data
    :param object_pk: Entity primary key to be supplied with the submission, if any
    :param override_data: Data to be used instead of the request's data, if applicable
    """
    data = request.POST.copy()

    if override_data:
        data = override_data

    if object_pk:
        validated_data, _ = action(request, object_pk, data)
    else:
        validated_data, _ = action(request, data)

    if "errors" in validated_data:
        return (
            form_page(request, form, data=data, errors=validated_data.get("errors")),
            None,
        )

    return None, validated_data


def _prepare_data(request, inject_data):
    data = request.POST.copy()

    # Handle lists (such as checkboxes)
    data = handle_lists(data)

    if data and inject_data:
        for key, value in data.items():
            inject_data[key] = value

        data = QueryDict("", mutable=True)
        data.update(inject_data)

    # Remove form_pk and CSRF from POST data as the new form will replace them
    if "form_pk" in data:
        del data["form_pk"]
    if "csrfmiddlewaretoken" in data:
        del data["csrfmiddlewaretoken"]

    # Post the data to the validator and check for errors
    return data, nest_data(data)


def submit_paged_form(  # noqa
    request, form_group: FormGroup, action: Callable, object_pk=None, inject_data=None, additional_context: dict = None,
):
    """
    Function to handle the submission of the data from one form in a sequence of forms (a FormGroup).
    :param request: Standard Django request object
    :param form_group: The FormGroup that defines the sequence of forms being traversed
    :param action: The callback action to be invoked here to submit the form's data
    :param object_pk: Entity primary key to be supplied with the submission, if any
    :param inject_data: Additional data to be added to the supplied request's data before submitting
    :param additional_context: Adds additional items to context for form
    :return: The next form page to display
    """
    if additional_context is None:
        additional_context = {}

    data, nested_data = _prepare_data(request, inject_data)

    form_pk = request.POST.get("form_pk")
    previous_form = get_previous_form(form_pk, form_group)
    current_form = get_form_by_pk(form_pk, form_group)
    next_form = get_next_form(form_pk, form_group)

    post_data, _ = _prepare_data(request, {})

    if data.get("_action") and data.get("_action") == "back":

        return form_with_hidden_fields(
            request, data, post_data, form=previous_form, return_data=None, additional_context=additional_context
        )

    if object_pk:
        validated_data, _ = action(request, object_pk, nested_data)
    else:
        validated_data, _ = action(request, nested_data)

    # If the API returns errors, add the existing questions to the reloaded form
    errors = validated_data.get("errors")

    if errors:
        errors = flatten_data(errors)
        errors = remove_unused_errors(errors, current_form)

    if errors:
        for key, value in data.items():
            exists = False

            for question in current_form.questions:
                if hasattr(question, "prefix") and question.prefix:
                    if question.prefix in key:
                        exists = True
                        continue
                elif hasattr(question, "name"):
                    if question.name == key:
                        exists = True
                        continue

            if not exists:
                if isinstance(value, list):
                    for sub_value in value:
                        current_form.questions.insert(0, HiddenField(key + "[]", sub_value))
                else:
                    current_form.questions.insert(0, HiddenField(key, value))

        return (
            form_page(
                request,
                current_form,
                data=data,
                errors=errors,
                extra_data={"form_pk": current_form.pk, **additional_context},
            ),
            validated_data,
        )

    # If there aren't any forms left to go through, return the data
    if next_form is None:
        return None, validated_data

    return form_with_hidden_fields(
        request, data, post_data, form=next_form, return_data=validated_data, additional_context=additional_context
    )


def form_with_hidden_fields(request, data, post_data, form, return_data, additional_context):

    for key, value in post_data.items():

        # If the key is already in the questions in the next form, don't copy them
        # because the user will input their answers again
        form_question_names = [q.name for q in form.questions if hasattr(q, "name")]

        if key in form_question_names or f"{key}[]" in form_question_names:
            continue

        # If the keys value is a list, insert each individually
        if isinstance(value, list):
            for sub_value in value:
                form.questions.insert(0, HiddenField(key + "[]", sub_value))
        else:
            form.questions.insert(0, HiddenField(key, value))

    # Go to the next page
    return (
        form_page(request, form, data=data, extra_data={"form_pk": form.pk, **additional_context}),
        return_data,
    )
