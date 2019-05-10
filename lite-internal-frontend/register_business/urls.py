from django.urls import path

from . import views

app_name = 'register_business'
urlpatterns = [
    path('', views.RegisterBusiness.as_view(), name='register'),
]
