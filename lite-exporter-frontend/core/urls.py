from django.urls import path

from core import views

app_name = "core"
urlpatterns = [
    path("", views.Hub.as_view(), name="hub"),
    path("pick-organisation/", views.PickOrganisation.as_view(), name="pick_organisation"),
]
