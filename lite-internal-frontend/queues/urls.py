from django.urls import path

from queues import views

app_name = 'queues'
urlpatterns = [
    # ex: /queues/
    path('', views.QueuesList.as_view(), name='queues'),
    # ex: /queues/add/
    path('add', views.AddQueue.as_view(), name='add'),
    # ex: /queues/<uuid:pk>/ - Go to a queues's detail
    path('<uuid:pk>/', views.EditQueue.as_view(), name='edit'),
    # ex: /queues/<uuid:pk>/case-assignments/ - Assign users to cases pertaining to that queue
    path('<uuid:pk>/case-assignments/', views.CaseAssignments.as_view(), name='case_assignments'),
]
