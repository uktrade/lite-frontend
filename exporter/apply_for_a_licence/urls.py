from django.conf import settings
from django.urls import path

from exporter.apply_for_a_licence import views


app_name = "apply_for_a_licence"

urlpatterns = [
    path("", views.LicenceTypeView.as_view(), name="start"),
]

if not settings.FEATURE_FLAG_ONLY_ALLOW_SIEL:
    urlpatterns += [
        path("transhipment/", views.TranshipmentQuestions.as_view(), name="transhipment_questions"),
        path("<str:ogl>/", views.OpenGeneralLicenceQuestions.as_view(), name="ogl_questions"),
        path("<str:ogl>/<uuid:pk>/", views.OpenGeneralLicenceSubmit.as_view(), name="ogl_submit"),
    ]
