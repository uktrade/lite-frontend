from django.conf import settings
from django.urls import path

from exporter.apply_for_a_licence import views

from exporter.apply_for_a_licence.f680 import views as f680


app_name = "apply_for_a_licence"

urlpatterns = [
    path("", views.LicenceType.as_view(), name="start"),
    path("export/", views.ExportLicenceQuestions.as_view(), name="export_licence_questions"),
    path("f680/", f680.AddF680.as_view(), name="f680_questions"),  # /PS-IGNORE
    path("f680/<uuid:pk>/task-list/", f680.GetF680Application.as_view(), name="f680_task_list"),
]

if not settings.FEATURE_FLAG_ONLY_ALLOW_SIEL:
    urlpatterns += [
        path("transhipment/", views.TranshipmentQuestions.as_view(), name="transhipment_questions"),
        path("mod/", views.MODClearanceQuestions.as_view(), name="mod_questions"),
        path("<str:ogl>/", views.OpenGeneralLicenceQuestions.as_view(), name="ogl_questions"),
        path("<str:ogl>/<uuid:pk>/", views.OpenGeneralLicenceSubmit.as_view(), name="ogl_submit"),
    ]
