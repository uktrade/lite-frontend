from django.urls import path

from core import views
from queues import views as queues_views

app_name = "core"

urlpatterns = [
    path("", queues_views.Cases.as_view(), name="index", kwargs={"disable_queue_lookup": True}),
    path("menu/", views.menu, name="menu"),
]
