from django.urls import path

from apply_for_a_licence import views

app_name = "apply_for_a_licence"

urlpatterns = [
    path("", views.LicenceType.as_view(), name="start"),
    path("export/", views.ExportLicenceQuestions.as_view(), name="export_licence_questions"),
    path("trade-control/", views.TradeControlLicenceQuestions.as_view(), name="trade_control_licence_questions"),
    path("transhipment/", views.TranshipmentQuestions.as_view(), name="transhipment_questions"),
    path("mod/", views.MODClearanceQuestions.as_view(), name="mod_questions"),
    path("<str:ogl>/", views.OpenGeneralLicenceQuestions.as_view(), name="ogl_questions"),
    path("<str:ogl>/<uuid:pk>/", views.OpenGeneralLicenceSubmit.as_view(), name="ogl_submit"),
]
