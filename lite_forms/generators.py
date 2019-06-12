from django.shortcuts import render


def form_page(request, form, data=None, errors=None, extra_data=None):
    """
    Returns a standard GOV.UK Design System styled form page.
    """
    context = {
        'page': form,
        'title': form.title,
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
