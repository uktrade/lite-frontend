from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
	# ex: /
	path('', views.hub, name='hub'),
	# ex: /login
	path('login/', views.login, name='login'),
	# ex: /logout
	path('logout/', views.logout, name='logout'),
]
