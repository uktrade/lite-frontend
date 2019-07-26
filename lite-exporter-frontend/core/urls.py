from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
	# ex: /
	path('', views.hub, name='hub'),
]
