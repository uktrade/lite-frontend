from django.urls import path

from conf.constants import ALL_CASES_QUEUE_ID
from core import views
from queues import views as queues_views

app_name = "core"

urlpatterns = [
    path("", queues_views.Cases.as_view(), name="index", kwargs={"queue_pk": ALL_CASES_QUEUE_ID}),
    path("menu/", views.menu, name="menu"),
]
