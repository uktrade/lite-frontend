from django.urls import path

from . import views

app_name = 'applications'
urlpatterns = [
    # ex: /
    path('', views.index, name='applications'),
    # ex: /43a88949-5db9-4334-b0cc-044e91827451/
    path('<uuid:id>/', views.application, name='application'),
]
