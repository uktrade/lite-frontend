from django.shortcuts import render, redirect


def hub(request):
    return redirect("/cases/")


def menu(request):
    return render(request, "core/menu.html", {"title": "Menu"})
