from django.urls import path

from . import views


app_name = "f680"  # /PS-IGNORE

urlpatterns = [
    path("f680/", views.F680Create.as_view(), name="add_f680"),  # /PS-IGNORE
    path(
        "f680/approval-questions/", views.F680ApprovalQuestions.as_view(), name="f680_approval_questions"  # /PS-IGNORE
    ),
    path("f680/<uuid:pk>/task-list/", views.GetF680Application.as_view(), name="f680_task_list"),  # /PS-IGNORE
]
