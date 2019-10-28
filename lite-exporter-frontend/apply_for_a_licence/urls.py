from django.urls import path

from apply_for_a_licence import views

app_name = 'apply_for_a_licence'

urlpatterns = [
    # ex: /start/
    path('start/', views.InitialQuestions.as_view(), name='start'),
]
