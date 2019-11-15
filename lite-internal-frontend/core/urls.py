from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.hub, name="hub"),
    path("menu/", views.menu, name="menu"),
]
