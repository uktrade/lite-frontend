from django.shortcuts import render

from lite_forms.components import (
    RadioButtons,
    Option,
    HiddenField,
    Form,
    BackLink,
    Summary,
)
from lite_forms.helpers import conditional


def form_page(request, form, data=None, errors=None, extra_data=None):
    """
    Returns a standard GOV.UK Design System styled form page.
    """
    context = {
        "page": form,
        "title": form.title if errors is None else "Error: " + form.title,
        "data": data,
        "errors": errors,
        "form_pk": 0,
    }

    if extra_data:
        context.update(extra_data)

    return render(request, "form.html", context)


def success_page(
    request,
    title,
    secondary_title,
    description,
    what_happens_next,
    links,
    includes=None,
    animated=False,
    back_link=None,
    additional_context=None,
):
    """
    Returns a standard GOV.UK Design System styled success page.
    """
    if additional_context is None:
        additional_context = {}

    context = {
        "title": title,
        "secondary_title": secondary_title,
        "description": description,
        "what_happens_next": what_happens_next,
        "includes": includes,
        "links": links,
        "back_link": back_link,
        "animated": animated,
    }
    if additional_context:
        context.update(additional_context)
    return render(request, "confirmation.html", context)


def error_page(request, description, title="An error occurred", show_back_link=True):
    """
    Returns a standard GOV.UK Design System styled error page.
    """
    context = {
        "title": title,
        "description": description,
        "show_back_link": show_back_link,
    }
    return render(request, "error.html", context)


def confirm_form(
    title,
    confirmation_name,
    back_url,
    back_link_text,
    hidden_field=None,
    summary: Summary = None,
    description="",
    yes_label="Yes",
    no_label="No",
    submit_button_text="Submit",
    side_by_side=False,
    container="two-pane",
):
    inputs = [
        conditional(summary is not None, summary),
        RadioButtons(
            name=confirmation_name,
            options=[
                Option(key="yes", value=yes_label),
                Option(key="no", value=no_label),
            ],
            classes=["govuk-radios--inline"] if side_by_side else [],
        ),
        conditional(hidden_field is not None, HiddenField(name="form_name", value=hidden_field)),
    ]

    return Form(
        title=title,
        description=description,
        questions=inputs,
        back_link=BackLink(back_link_text, back_url),
        default_button_name=submit_button_text,
        container=container,
    )
