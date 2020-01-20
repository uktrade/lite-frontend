from django.urls import path

from queues import views

app_name = "queues"
urlpatterns = [
    path("", views.QueuesList.as_view(), name="queues"),
    path("add", views.AddQueue.as_view(), name="add"),
    path("<uuid:pk>/", views.EditQueue.as_view(), name="edit"),
    path("<uuid:pk>/case-assignments/", views.CaseAssignments.as_view(), name="case_assignments"),
]
