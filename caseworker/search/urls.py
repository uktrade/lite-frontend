from django.urls import path

from . import views

app_name = "search"

urlpatterns = [
    path("products/", views.ProductSearchView.as_view(), name="products"),
]
