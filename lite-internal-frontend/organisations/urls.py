from django.urls import path

from flags.views import AssignFlags
from organisations import views

app_name = "organisations"

urlpatterns = [
    path("", views.OrganisationList.as_view(), name="organisations"),
    path("<uuid:pk>/", views.OrganisationDetail.as_view(), name="organisation"),
    path("<uuid:pk>/assign-flags/", AssignFlags.as_view(), name="assign_flags"),
    path("hmrc/", views.HMRCList.as_view(), name="hmrc"),
    path("register/", views.RegisterBusiness.as_view(), name="register"),
    path("register-hmrc/", views.RegisterHMRC.as_view(), name="register_hmrc"),
]
