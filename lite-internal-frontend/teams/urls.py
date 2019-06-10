from django.urls import path

from teams import views

app_name = 'teams'
urlpatterns = [
    # ex: /
    path('', views.TeamsList.as_view(), name='teams'),
	# ex: /users/add/
	path('add', views.AddTeam.as_view(), name='add'),
	# ex: /users/43a88949-5db9-4334-b0cc-044e91827451/ - Go to a user's profile
	path('<uuid:pk>/', views.EditTeam.as_view(), name='edit'),
]
