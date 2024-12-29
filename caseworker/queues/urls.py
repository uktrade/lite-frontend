from django.urls import path

from caseworker.advice.views.bulk_approval import BulkApprovalView, BulkCountersignApprovalView
from caseworker.queues.views import case_assignments, cases, enforcement, queues

app_name = "queues"

urlpatterns = [
    path("", cases.Cases.as_view(), name="cases", kwargs={"disable_queue_lookup": True}),
    path("<uuid:queue_pk>/", cases.Cases.as_view(), name="cases", kwargs={"disable_queue_lookup": True}),
    path("manage/", queues.QueuesList.as_view(), name="manage"),
    path("add/", queues.AddQueue.as_view(), name="add"),
    path("<uuid:pk>/edit/", queues.EditQueue.as_view(), name="edit"),
    path(
        "<uuid:pk>/case-assignment-select-role/",
        case_assignments.CaseAssignmentAllocateRole.as_view(),
        name="case_assignment_select_role",
    ),
    path(
        "<uuid:pk>/case-assignment-assign-to-me/",
        case_assignments.CaseAssignmentAllocateToMe.as_view(),
        name="case_assignment_assign_to_me",
    ),
    path(
        "<uuid:pk>/case-assignments-assign-case-officer/",
        case_assignments.CaseAssignmentsCaseOfficer.as_view(),
        name="case_assignments_case_officer",
    ),
    path(
        "<uuid:pk>/case-assignments-assign-user/",
        case_assignments.CaseAssignmentsCaseAssignee.as_view(),
        name="case_assignments_assign_user",
    ),
    path(
        "<uuid:pk>/enforcement-xml-export/", enforcement.EnforcementXMLExport.as_view(), name="enforcement_xml_export"
    ),
    path(
        "<uuid:pk>/enforcement-xml-import/", enforcement.EnforcementXMLImport.as_view(), name="enforcement_xml_import"
    ),
    path("<uuid:pk>/bulk-approve/", BulkApprovalView.as_view(), name="bulk_approval"),
    path(
        "<uuid:pk>/bulk-countersign-approve/", BulkCountersignApprovalView.as_view(), name="bulk_countersign_approval"
    ),
]
