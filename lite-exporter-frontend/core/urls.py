from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    # ex: /
    path('', views.hub, name='hub'),
	# ex: /signin
	path('signin', views.signin, name='signin'),
	# ex: /signout
	path('signout', views.signout, name='signout'),
	# ex: /placeholder
	path('placeholder', views.placeholder, name='placeholder'),
]
