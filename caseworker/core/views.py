from django.shortcuts import render

from caseworker.core.context_processors import lite_menu
from lite_content.lite_internal_frontend.core import get_human_readable_exception


def menu(request):
    return render(request, "core/menu.html", {"title": "Menu"})


def handle_error(status_code):
    def inner(request):
        return render(
            request,
            template_name="core/error.html",
            context={**get_human_readable_exception(status_code), **lite_menu(request)},
            status=status_code,
        )

    return inner
