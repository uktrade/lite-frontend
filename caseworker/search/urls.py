from django.conf import settings
from django.urls import path

from caseworker.search import views

app_name = "search"

urlpatterns = [
    path("applications/", views.ApplicationSearchView.as_view(), name="applications"),
    path("applications/suggest/", views.ApplicationAutocompleteView.as_view(), name="api-search-suggest"),
]

if settings.FEATURE_PRODUCTPEDIA_ON:

    urlpatterns += [
        path("products/", views.ProductSearchView.as_view(), name="products"),
        path("products/suggest/", views.ProductAutocompleteView.as_view(), name="api-search-suggest-product"),
        path("products/<str:pk>/", views.ProductDetailSpireView.as_view(), name="product-details"),
        path("products/<uuid:pk>/", views.ProductDetailLiteView.as_view(), name="product-details"),
    ]
