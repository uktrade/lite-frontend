from django.urls import path

from . import views

app_name = "cookies"

urlpatterns = [
    path(
        "",
        views.CookiesPreferencesView.as_view(),
        name="cookies-preferences",
    ),
    path("info/", views.CookiesDetailsView.as_view(), name="cookies-details"),
]
