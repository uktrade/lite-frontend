from django.urls import path

from end_users import views

app_name = 'end_users'

urlpatterns = [
    # ex: /end-users/
    path('', views.EndUsersList.as_view(), name='end_users'),

    # ex: /<int:pk>/copy-advisory/
    path('<int:pk>/copy-advisory/', views.CopyAdvisory.as_view(), name='copy'),

    # ex: /end-users/apply-for-an-advisory/
    path('apply-for-an-advisory/', views.ApplyForAnAdvisory.as_view(), name='apply'),
]
