from django.urls import path

from . import views

app_name = 'applications'
urlpatterns = [
    # ex: /applications/
    path('', views.ApplicationsList.as_view(), name='applications'),
    # ex: /applications/43a88949-5db9-4334-b0cc-044e91827451/
    path('<uuid:pk>/', views.ApplicationDetail.as_view(), name='application'),
    # ex: /applications/43a88949-5db9-4334-b0cc-044e91827451/
    path('<uuid:pk>/case-notes/', views.CaseNotes.as_view(), name='case_notes'),
]
