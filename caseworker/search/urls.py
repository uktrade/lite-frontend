from django.urls import path

from caseworker.search import views

app_name = "search"

urlpatterns = [
    path("", views.SearchForm.as_view(), name="index"),
]
