from django.urls import path

from core import views, api
from queues import views as queues_views

app_name = "core"

urlpatterns = [
    path("", queues_views.Cases.as_view(), name="index", kwargs={"disable_queue_lookup": True}),
    path("menu/", views.menu, name="menu"),
    path("api/cases/<uuid:pk>/", api.Cases.as_view(), name="cases"),
]
