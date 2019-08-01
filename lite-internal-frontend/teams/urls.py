from django.urls import path

from teams import views

app_name = 'teams'
urlpatterns = [
    # ex: /team/
    path('', views.Team.as_view(), name='team'),

    # ex: /teams/
    path('s/', views.TeamsList.as_view(), name='teams'),
    # ex: /teams/add/
    path('s/add', views.AddTeam.as_view(), name='add'),
    # ex: /teams/<uuid:pk>/
    path('s/<uuid:pk>', views.TeamDetail.as_view(), name='team'),
    # ex: /teams/<uuid:pk>/edit/
    path('s/<uuid:pk>/edit', views.EditTeam.as_view(), name='edit'),
]
