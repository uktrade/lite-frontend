from django.shortcuts import render

from libraries.forms.components import Option, RadioButtons, HiddenField, Form, BackLink


def form_page(request, form, data=None, errors=None, extra_data=None):
    """
    Returns a standard GOV.UK Design System styled form page.
    """
    context = {
        'page': form,
        'title': form.title if errors is None else 'Error: ' + form.title,
        'data': data,
        'errors': errors,
    }

    if extra_data:
        context.update(extra_data)

    return render(request, 'form.html', context)


def success_page(request, title, secondary_title, description, what_happens_next, links):
    """
    Returns a standard GOV.UK Design System styled success page.
    """
    context = {
        'title': title,
        'secondary_title': secondary_title,
        'description': description,
        'what_happens_next': what_happens_next,
        'links': links,
    }
    return render(request, 'confirmation.html', context)


def error_page(request, description, title='An error occurred', show_back_link=True):
    """
    Returns a standard GOV.UK Design System styled error page.
    """
    context = {
        'title': title,
        'description': description,
        'show_back_link': show_back_link,
    }
    return render(request, 'error.html', context)


def confirm_form(title, confirmation_name, back_url, back_link_text, hidden_field=None,
                      description='', yes_label='Yes', no_label='No', submit_button_text='Submit'):
    inputs = [RadioButtons(title='', name=confirmation_name, description='',
                           options=[Option(key='yes', value=yes_label), Option(key='no', value=no_label)])]
    if hidden_field is not None:
        inputs.append(HiddenField(name='form_name', value=hidden_field))

    return Form(title=title,
                description=description,
                questions=inputs,
                back_link=BackLink(back_link_text, back_url),
                default_button_name=submit_button_text
                )
