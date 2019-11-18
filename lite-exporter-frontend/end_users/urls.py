from django.urls import path

from end_users import views

app_name = "end_users"

urlpatterns = [
    # ex: /end-users/
    path("", views.EndUsersList.as_view(), name="end_users"),
    # ex: /end-users/1234567890/
    path("<int:pk>/", views.EndUserDetailEmpty.as_view(), name="end_user"),
    # ex: /end-users/1234567890/copy-advisory/
    path("<int:pk>/copy-advisory/", views.CopyAdvisory.as_view(), name="copy"),
    # ex: /end-users/apply-for-an-advisory/
    path("apply-for-an-advisory/", views.ApplyForAnAdvisory.as_view(), name="apply"),
    # ex: /end-users/1234567890/<str:type>/
    path("<int:pk>/<str:type>/", views.EndUserDetail.as_view(), name="end_user_detail"),
    # ex: /end-users/1234567890/ecju-queries/43a88949-5db9-4334-b0cc-044e91827451
    path("<int:pk>/ecju-queries/<uuid:query_pk>/", views.RespondToQuery.as_view(), name="respond_to_query"),
]
