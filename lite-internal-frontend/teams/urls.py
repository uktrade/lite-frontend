from django.urls import path

from teams import views

app_name = 'teams'
urlpatterns = [
    # ex: /
    path('', views.TeamsList.as_view(), name='teams'),
	# ex: /teams/add/
	path('add', views.AddTeam.as_view(), name='add'),
	# ex: /teams/43a88949-5db9-4334-b0cc-044e91827451/
	path('<uuid:pk>', views.TeamDetail.as_view(), name='team'),
	# ex: /teams/43a88949-5db9-4334-b0cc-044e91827451/edit
	path('<uuid:pk>/edit', views.EditTeam.as_view(), name='edit'),
]
