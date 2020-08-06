from django.urls import path

import caseworker.core.views
import caseworker.core.api
import caseworker.queues.views


app_name = "core"

urlpatterns = [
    path("", caseworker.queues.views.Cases.as_view(), name="index", kwargs={"disable_queue_lookup": True}),
    path("menu/", caseworker.core.views.menu, name="menu"),
    path("api/cases/<uuid:pk>/", caseworker.core.api.Cases.as_view(), name="cases"),
]
