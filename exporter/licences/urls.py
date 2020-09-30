from django.urls import path

from exporter.licences import views

app_name = "licences"
urlpatterns = [
    path("", views.ListOpenAndStandardLicences.as_view(), name="list-open-and-standard-licences"),
    path("no-licence-required/", views.ListNoLicenceRequired.as_view(), name="list-no-licence-required"),
    path("clearances/", views.ListClearances.as_view(), name="list-clearances"),
    path("open-general-licences/", views.ListOpenGeneralLicences.as_view(), name="list-open-general-licences"),
    path("<uuid:pk>/", views.Licence.as_view(), name="licence"),
]
