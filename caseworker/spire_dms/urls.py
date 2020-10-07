from django.urls import path

from caseworker.spire_dms import views


app_name = "spire_dms"

urlpatterns = [
    path("application/", views.SpireApplicationSearch.as_view(), name="application-search"),
]
