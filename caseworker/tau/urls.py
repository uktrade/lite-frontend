from django.urls import path

from caseworker.tau.views import TAUHome, TAUEdit, TAUMoveCaseForward, Document

app_name = "tau"

urlpatterns = [
    path("", TAUHome.as_view(), name="home"),
    path("edit/<good_id>", TAUEdit.as_view(), name="edit"),
    path("move-case-forward/", TAUMoveCaseForward.as_view(), name="move_case_forward"),
    path("<uuid:file_pk>/", Document.as_view(), name="document"),
]
