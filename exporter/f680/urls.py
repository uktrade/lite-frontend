from django.urls import path

from . import views


app_name = "f680"

urlpatterns = [
    path("apply/", views.F680ApplicationCreateView.as_view(), name="apply"),
    path("<uuid:pk>/apply/", views.F680ApplicationSummaryView.as_view(), name="summary"),
    path("<uuid:pk>/apply/products/", views.F680ApplicationProductsView.as_view(), name="products"),
    path("<uuid:pk>/submitted/", views.F680ApplicationSubmittedView.as_view(), name="submitted"),
]
