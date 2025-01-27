from django.urls import path

from . import views


app_name = "f680"

urlpatterns = [
    path("apply/", views.F680ApplicationCreateView.as_view(), name="apply"),
    path("<uuid:pk>/apply/", views.F680ApplicationSummaryView.as_view(), name="summary"),
    path("<uuid:pk>/apply/products/", views.F680ApplicationProductsView.as_view(), name="products"),
    path("<uuid:pk>/apply/end_user/add/", views.F680ApplicationEndUserView.as_view(), name="add_end_user"),
    # path("<uuid:pk>/apply/consignee/add/", views.F680ApplicationConsigneeView.as_view(), name="add_consignee"),
    # path("<uuid:pk>/apply/third-party/add/", views.F680ApplicationThirdPartyView.as_view(), name="add_third_party"),
    # path(
    #     "<uuid:pk>/apply/ultimate-end-user/add/",
    #     views.F680ApplicationUltimateEndUserView.as_view(),
    #     name="add_ultimate_end_user",
    # ),
    path("<uuid:pk>/submitted/", views.F680ApplicationSubmittedView.as_view(), name="submitted"),
]
