from django.urls import path

from end_users import views

app_name = "end_users"

urlpatterns = [
    path("", views.EndUsersList.as_view(), name="end_users"),
    path("<uuid:pk>/", views.EndUserDetailEmpty.as_view(), name="end_user"),
    path("<uuid:pk>/copy-advisory/", views.CopyAdvisory.as_view(), name="copy"),
    path("apply-for-an-advisory/", views.ApplyForAnAdvisory.as_view(), name="apply"),
    path("<uuid:pk>/<str:type>/", views.EndUserDetail.as_view(), name="end_user_detail"),
]
