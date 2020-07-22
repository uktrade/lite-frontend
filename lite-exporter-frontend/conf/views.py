from lite_forms.generators import error_page


def handler403(request, exception):
    return error_page(request, title="Forbidden", description=exception, show_back_link=True)
