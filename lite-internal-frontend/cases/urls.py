from django.urls import path

from cases import views

app_name = 'cases'
urlpatterns = [
    # ex: /
    path('', views.index, name='cases'),
    # ex: /43a88949-5db9-4334-b0cc-044e91827451
    path('<uuid:pk>/', views.ViewCase.as_view(), name='case'),
    # ex: /43a88949-5db9-4334-b0cc-044e91827451/manage
    path('<uuid:pk>/manage', views.ManageCase.as_view(), name='manage'),
    # ex: /43a88949-5db9-4334-b0cc-044e91827451/decide
    path('<uuid:pk>/decide', views.DecideCase.as_view(), name='decide')
]
