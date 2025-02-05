from django.urls import path

from .views import add, summary


urlpatterns = [
    path("add/", add.AddF680GoodDetails.as_view(), name="f680_good_details"),
    path(
        "<uuid:good_pk>/product-summary/",
        summary.CompleteF680GoodDetailsSummary.as_view(),
        name="f680_good_details_summary",
    ),
    path(
        "<uuid:good_pk>/add-to-application/",
        add.AddF680GoodDetailsToApplication.as_view(),
        name="f680_good_details_to_application",
    ),
    path(
        "<uuid:good_on_application_pk>/product-on-application-summary/",
        summary.CompleteF680GoodDetailsOnApplicationSummary.as_view(),
        name="f680_good_details_on_application_summary",
    ),
]
