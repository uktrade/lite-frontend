from django.urls import path

from departments import views

app_name = 'departments'
urlpatterns = [
    # ex: /
    path('', views.DepartmentsList.as_view(), name='departments'),
	# ex: /users/add/
	path('add', views.AddDepartment.as_view(), name='add'),
	# ex: /users/43a88949-5db9-4334-b0cc-044e91827451/ - Go to a user's profile
	path('<uuid:pk>/', views.EditDepartment.as_view(), name='edit'),
]
