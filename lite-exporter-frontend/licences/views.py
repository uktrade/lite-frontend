from django.shortcuts import render


def index(request):
    context = {
        "title": "Licences",
    }
    return render(request, "licences/index.html", context)
