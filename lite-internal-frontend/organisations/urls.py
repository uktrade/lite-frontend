from django.urls import path

from organisations import views

app_name = 'organisations'

urlpatterns = [
    # ex: /
    path('', views.OrganisationList.as_view(), name='organisations'),
    # ex: /43a88949-5db9-4334-b0cc-044e91827451/
    path('<uuid:pk>/', views.OrganisationDetail.as_view(), name='organisation'),
]
