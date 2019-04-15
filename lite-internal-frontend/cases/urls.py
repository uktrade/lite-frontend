from django.urls import path

from . import views

app_name = 'cases'
urlpatterns = [
    # ex: /
    path('', views.index, name='cases'),
    # ex: /43a88949-5db9-4334-b0cc-044e91827451
    path('<uuid:pk>', views.case, name='case'),
    # ex: /43a88949-5db9-4334-b0cc-044e91827451/manage
    path('<uuid:pk>/manage', views.ManageCase.as_view(), name='manage'),
    path('<uuid:pk>/decide', views.DecideCase.as_view(), name='decide')
]
