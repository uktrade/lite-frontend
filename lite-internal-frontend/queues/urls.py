from django.urls import path

from conf.constants import ALL_CASES_QUEUE_ID
from queues import views

app_name = "queues"

urlpatterns = [
    path("", views.Cases.as_view(), name="cases", kwargs={"queue_pk": ALL_CASES_QUEUE_ID}),
    path("<uuid:queue_pk>/", views.Cases.as_view(), name="cases"),
    path("manage/", views.QueuesList.as_view(), name="manage"),
    path("add/", views.AddQueue.as_view(), name="add"),
    path("<uuid:pk>/edit/", views.EditQueue.as_view(), name="edit"),
    path("<uuid:pk>/case-assignments/", views.CaseAssignments.as_view(), name="case_assignments"),
]
