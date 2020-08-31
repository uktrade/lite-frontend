from django.urls import path

from caseworker.search import views

app_name = "search"

urlpatterns = [
    path("", views.Search.as_view(), name="index"),
]
