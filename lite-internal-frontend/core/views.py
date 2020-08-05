from django.shortcuts import render


def menu(request):
    return render(request, "core/menu.html", {"title": "Menu"})
