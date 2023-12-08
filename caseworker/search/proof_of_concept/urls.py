from django.urls import path

from . import views

app_name = "search_proof_of_concept"

urlpatterns = [
    path("applications/", views.ApplicationSearchView.as_view(), name="applications"),
    path("applications/suggest/", views.ApplicationAutocompleteView.as_view(), name="api-search-suggest"),
]
