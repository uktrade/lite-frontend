from django.shortcuts import render

from caseworker.core.context_processors import lite_menu
from lite_content.lite_internal_frontend.core import get_human_readable_exception


def menu(request):
    return render(request, "core/menu.html", {"title": "Menu"})


def handler403(request, exception):
    return render(
        request,
        template_name="core/error.html",
        context={**get_human_readable_exception(403), **lite_menu(request)},
        status=403,
    )


def handler404(request, exception):
    return render(
        request,
        template_name="core/error.html",
        context={**get_human_readable_exception(404), **lite_menu(request)},
        status=404,
    )


def handler500(request):
    return render(
        request,
        template_name="core/error.html",
        context={**get_human_readable_exception(500), **lite_menu(request)},
        status=404,
    )
