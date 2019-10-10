from django.urls import path

from flags import views

app_name = 'flags'
urlpatterns = [
    # ex: /flags/ - View all active flags
    path('', views.FlagsList.as_view(), name='flags'),
    # ex: /flags/assign-flags/
    path('assign-flags/', views.AssignFlags.as_view(), name='assign_flags'),
    # ex: /all/ - view all flags
    path('<str:status>/', views.FlagsList.as_view(), name='flags'),
    # ex: /flags/add/ -  add a new flag
    path('add', views.AddFlag.as_view(), name='add'),
    # ex: /flags/43a88949-5db9-4334-b0cc-044e91827451/ - Go to a flags's detail
    path('<uuid:pk>/profile/', views.ViewFlag.as_view(), name='flag'),
    # ex: /flags/<uuid:pk>/edit - edit a flag
    path('<uuid:pk>/edit/', views.EditFlag.as_view(), name='edit'),
    # ex: /flags/<uuid:pk>/edit/deactivate - deactivate or reactivate a flag
    path('<uuid:pk>/edit/<str:status>/', views.ChangeFlagStatus.as_view(), name='change_status'),
]
