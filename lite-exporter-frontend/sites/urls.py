from django.urls import path

from . import views

app_name = 'sites'
urlpatterns = [
    # ex: /sites/
    path('', views.Sites.as_view(), name='sites'),
    # ex: /sites/new/
    path('new/', views.NewSite.as_view(), name='new'),
    # ex: /sites/new/
    path('<uuid:pk>/edit/', views.EditSite.as_view(), name='edit'),
]
