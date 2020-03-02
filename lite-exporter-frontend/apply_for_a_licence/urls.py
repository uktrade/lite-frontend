from django.urls import path

from apply_for_a_licence import views

app_name = "apply_for_a_licence"

urlpatterns = [
    path("", views.LicenceType.as_view(), name="start"),
    path("licence/", views.ExportLicenceQuestions.as_view(), name="export_licence_questions"),
    path("transhipment/", views.TranshipmentQuestions.as_view(), name="transhipment_questions"),
    path("mod/", views.MODClearanceQuestions.as_view(), name="mod_questions"),
]
