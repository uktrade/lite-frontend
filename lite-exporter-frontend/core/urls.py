from django.urls import path

from core import views

app_name = "core"
urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("pick-organisation/", views.PickOrganisation.as_view(), name="pick_organisation"),
]
