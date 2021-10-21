from django.urls import path

from caseworker.advice import views

urlpatterns = [
    path("", views.AdvicePlaceholderView.as_view(), name="advice_placeholder"),
    path("case-details/", views.CaseDetailView.as_view(), name="case_details"),
    path("select-advice/", views.SelectAdviceView.as_view(), name="select_advice"),
    path("approve-all/", views.GiveApprovalAdviceView.as_view(), name="approve_all"),
    path("refuse-all/", views.RefusalAdviceView.as_view(), name="refuse_all"),
    path("view-my-advice/", views.AdviceDetailView.as_view(), name="view_my_advice"),
    path("edit-advice/", views.EditAdviceView.as_view(), name="edit_advice"),
    path("delete-advice/", views.DeleteAdviceView.as_view(), name="delete_advice"),
]
