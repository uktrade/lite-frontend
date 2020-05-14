from lite_forms.generators import error_page


def handler403(request, exception):
    return error_page(None, title="Forbidden", description=exception, show_back_link=False)
