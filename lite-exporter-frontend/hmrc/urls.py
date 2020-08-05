from django.urls import path

from hmrc import views

app_name = "hmrc"

urlpatterns = [
    path("raise-a-query/", views.SelectAnOrganisation.as_view(), name="raise_a_query"),
    path("<uuid:org_id>/reference-name/", views.ReferenceName.as_view(), name="reference_name"),
]
