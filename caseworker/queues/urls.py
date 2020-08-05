from django.urls import path

from queues import views

app_name = "queues"

urlpatterns = [
    path("", views.Cases.as_view(), name="cases", kwargs={"disable_queue_lookup": True}),
    path("<uuid:queue_pk>/", views.Cases.as_view(), name="cases", kwargs={"disable_queue_lookup": True}),
    path("manage/", views.QueuesList.as_view(), name="manage"),
    path("add/", views.AddQueue.as_view(), name="add"),
    path("<uuid:pk>/edit/", views.EditQueue.as_view(), name="edit"),
    path("<uuid:pk>/case-assignments/", views.CaseAssignments.as_view(), name="case_assignments"),
    path("<uuid:pk>/enforcement-xml-export/", views.EnforcementXMLExport.as_view(), name="enforcement_xml_export"),
    path("<uuid:pk>/enforcement-xml-import/", views.EnforcementXMLImport.as_view(), name="enforcement_xml_import"),
]
