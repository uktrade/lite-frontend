from django.urls import path

from . import views


app_name = "approval_details"

urlpatterns = [
    path("product/", views.ProductInformationView.as_view(), name="product_wizard"),
]
