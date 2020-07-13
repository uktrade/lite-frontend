import datetime

from django.contrib import messages
from django.http import StreamingHttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler, s3_client

from cases.constants import CaseType
from cases.forms.additional_contacts import add_additional_contact_form
from cases.forms.assign_users import assign_case_officer_form, assign_user_and_work_queue, users_team_queues
from cases.forms.attach_documents import attach_documents_form
from cases.forms.change_status import change_status_form
from cases.forms.done_with_case import done_with_case_form
from cases.forms.move_case import move_case_form
from cases.forms.next_review_date import set_next_review_date_form
from cases.forms.rerun_routing_rules import rerun_routing_rules_confirmation_form
from cases.helpers.advice import get_advice_additional_context
from cases.helpers.case import CaseView, Tabs, Slices
from cases.services import (
    get_case,
    post_case_notes,
    put_case_queues,
    put_case_officer,
    delete_case_officer,
    put_unassign_queues,
    post_case_additional_contacts,
    put_rerun_case_routing_rules,
    patch_case,
    put_application_status,
    put_next_review_date,
)
from cases.services import post_case_documents, get_document
from compliance.services import get_compliance_licences
from conf import settings
from conf.settings import AWS_STORAGE_BUCKET_NAME
from core.services import get_permissible_statuses
from lite_content.lite_internal_frontend import cases
from lite_content.lite_internal_frontend.cases import DoneWithCaseOnQueueForm
from lite_forms.components import FiltersBar, TextInput
from lite_forms.generators import error_page, form_page
from lite_forms.helpers import conditional
from lite_forms.views import SingleFormView
from queues.services import put_queue_single_case_assignment, get_queue
from users.services import get_gov_user_from_form_selection


class CaseDetail(CaseView):
    def get_open_application(self):
        self.tabs = self.get_tabs()
        self.tabs.append(Tabs.ADVICE)
        self.slices = [
            Slices.GOODS,
            Slices.DESTINATIONS,
            Slices.OPEN_APP_PARTIES,
            conditional(self.case.data["inactive_parties"], Slices.DELETED_ENTITIES),
            Slices.LOCATIONS,
            *conditional(
                self.case.data["goodstype_category"]["key"] != "cryptographic",
                [Slices.END_USE_DETAILS, Slices.ROUTE_OF_GOODS],
                [],
            ),
            Slices.SUPPORTING_DOCUMENTS,
            conditional(self.case.data["export_type"]["key"] == "temporary", Slices.TEMPORARY_EXPORT_DETAILS),
        ]

        self.additional_context = {
            **get_advice_additional_context(self.request, self.case, self.permissions),
            "is_case_oiel_final_advice_only": False,
        }
        if "goodstype_category" in self.case.data:
            self.additional_context["is_case_oiel_final_advice_only"] = self.case.data["goodstype_category"]["key"] in [
                "media",
                "cryptographic",
                "dealer",
                "uk_continental_shelf",
            ]

    def get_standard_application(self):
        self.tabs = self.get_tabs()
        self.tabs.append(Tabs.ADVICE)
        self.slices = [
            Slices.GOODS,
            Slices.DESTINATIONS,
            conditional(self.case.data["inactive_parties"], Slices.DELETED_ENTITIES),
            Slices.LOCATIONS,
            Slices.END_USE_DETAILS,
            Slices.ROUTE_OF_GOODS,
            Slices.SUPPORTING_DOCUMENTS,
        ]
        self.additional_context = get_advice_additional_context(self.request, self.case, self.permissions)

    def get_hmrc_application(self):
        self.slices = [
            conditional(self.case.data["reasoning"], Slices.HMRC_NOTE),
            Slices.GOODS,
            Slices.DESTINATIONS,
            Slices.LOCATIONS,
            Slices.SUPPORTING_DOCUMENTS,
        ]
        self.additional_context = get_advice_additional_context(self.request, self.case, self.permissions)

    def get_exhibition_clearance_application(self):
        self.tabs = self.get_tabs()
        self.tabs.append(Tabs.ADVICE)
        self.slices = [
            Slices.EXHIBITION_DETAILS,
            Slices.GOODS,
            Slices.LOCATIONS,
            Slices.SUPPORTING_DOCUMENTS,
        ]
        self.additional_context = get_advice_additional_context(self.request, self.case, self.permissions)

    def get_gifting_clearance_application(self):
        self.tabs = self.get_tabs()
        self.tabs.append(Tabs.ADVICE)
        self.slices = [Slices.GOODS, Slices.DESTINATIONS, Slices.LOCATIONS, Slices.SUPPORTING_DOCUMENTS]
        self.additional_context = get_advice_additional_context(self.request, self.case, self.permissions)

    def get_f680_clearance_application(self):
        self.tabs = self.get_tabs()
        self.tabs.append(Tabs.ADVICE)
        self.slices = [
            Slices.GOODS,
            Slices.DESTINATIONS,
            Slices.F680_DETAILS,
            Slices.END_USE_DETAILS,
            Slices.SUPPORTING_DOCUMENTS,
        ]
        self.additional_context = get_advice_additional_context(self.request, self.case, self.permissions)

    def get_end_user_advisory_query(self):
        self.slices = [Slices.END_USER_DETAILS]

    def get_goods_query(self):
        self.slices = [Slices.GOODS_QUERY]
        if self.case.data["clc_responded"] or self.case.data["pv_grading_responded"]:
            self.slices.insert(0, Slices.GOODS_QUERY_RESPONSE)

    def get_open_registration(self):
        self.slices = [Slices.OPEN_GENERAL_LICENCE]

    def get_compliance_site(self):
        self.tabs = self.get_tabs()
        self.tabs.insert(1, Tabs.COMPLIANCE_LICENCES)
        self.slices = [Slices.COMPLIANCE_VISITS, Slices.OPEN_LICENCE_RETURNS]
        filters = FiltersBar([TextInput(name="reference", title=cases.CasePage.LicenceFilters.REFERENCE),])
        self.additional_context = {
            "data": get_compliance_licences(
                self.request, self.case.id, self.request.GET.get("reference", ""), self.request.GET.get("page", 1),
            ),
            "licences_filters": filters,
        }

    def get_compliance_visit(self):
        self.tabs = self.get_tabs()
        self.tabs.insert(1, Tabs.COMPLIANCE_LICENCES)
        self.slices = [Slices.COMPLIANCE_VISIT_DETAILS]
        filters = FiltersBar([TextInput(name="reference", title=cases.CasePage.LicenceFilters.REFERENCE),])
        self.additional_context = {
            "data": get_compliance_licences(
                self.request,
                self.case.data["site_case_id"],
                self.request.GET.get("reference", ""),
                self.request.GET.get("page", 1),
            ),
            "licences_filters": filters,
        }


class CaseNotes(TemplateView):
    def post(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        response, status_code = post_case_notes(request, case_id, request.POST)

        if status_code != 201:
            return error_page(request, response.get("errors")["text"][0])

        return redirect(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case_id, "tab": "activity"})
        )


class ImDoneView(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.data = {"queues": [str(kwargs["queue_pk"])]}
        self.context = {"case": case}
        has_review_date = (
            case.next_review_date
            and datetime.datetime.strptime(case.next_review_date, "%Y-%m-%d").date() > timezone.now().date()
        )
        self.form = done_with_case_form(request, self.object_pk, has_review_date)
        self.action = put_unassign_queues
        self.success_url = reverse_lazy("queues:cases", kwargs={"queue_pk": kwargs["queue_pk"]})
        self.success_message = DoneWithCaseOnQueueForm.SUCCESS_MESSAGE.format(case.reference_code)


class ChangeStatus(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        case = get_case(request, self.object_pk)
        self.case_type = case.type
        self.case_sub_type = case.sub_type
        permissible_statuses = get_permissible_statuses(request, case)
        self.data = case.data
        self.form = change_status_form(get_queue(request, kwargs["queue_pk"]), case, permissible_statuses)
        self.context = {"case": case}

    def get_action(self):
        if (
            self.case_type == CaseType.APPLICATION.value
            or self.case_sub_type == CaseType.HMRC.value
            or self.case_sub_type == CaseType.EXHIBITION.value
        ):
            return put_application_status
        else:
            return patch_case

    def get_success_url(self):
        messages.success(self.request, cases.ChangeStatusPage.SUCCESS_MESSAGE)
        return reverse_lazy("cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk})


class MoveCase(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.data = case
        self.form = move_case_form(request, get_queue(request, kwargs["queue_pk"]), case)
        self.action = put_case_queues
        self.context = {"case": case}
        self.success_message = cases.Manage.MoveCase.SUCCESS_MESSAGE
        self.success_url = reverse_lazy(
            "cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk}
        )


class AddAnAdditionalContact(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = add_additional_contact_form(request, self.kwargs["queue_pk"], self.object_pk)
        self.action = post_case_additional_contacts
        self.success_message = cases.CasePage.AdditionalContactsTab.SUCCESS_MESSAGE
        self.context = {"case": get_case(request, self.object_pk)}
        self.success_url = reverse(
            "cases:case",
            kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk, "tab": "additional-contacts"},
        )


@method_decorator(csrf_exempt, "dispatch")
class AttachDocuments(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        case = get_case(request, case_id)

        form = attach_documents_form(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case_id, "tab": "documents"})
        )

        return form_page(request, form, extra_data={"case_id": case_id, "case": case})

    @csrf_exempt
    def post(self, request, **kwargs):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        case_id = str(kwargs["pk"])
        data = []

        files = request.FILES.getlist("file")
        if len(files) != 1:
            return error_page(None, "We had an issue uploading your files. Try again later.")
        file = files[0]
        data.append(
            {
                "name": file.original_name,
                "s3_key": file.name,
                "size": int(file.size // 1024) if file.size else 0,  # in kilobytes
                "description": request.POST["description"],
            }
        )

        # Send LITE API the file information
        case_documents, _ = post_case_documents(request, case_id, data)

        if "errors" in case_documents:
            return error_page(None, "We had an issue uploading your files. Try again later.")

        return redirect(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case_id, "tab": "documents"})
        )


class Document(TemplateView):
    def get(self, request, **kwargs):
        file_pk = str(kwargs["file_pk"])

        document, _ = get_document(request, file_pk)
        original_file_name = document["document"]["name"]

        # Stream file
        def generate_file(result):
            for chunk in iter(lambda: result["Body"].read(settings.STREAMING_CHUNK_SIZE), b""):
                yield chunk

        s3 = s3_client()
        s3_key = document["document"]["s3_key"]
        s3_response = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_key)
        _kwargs = {}
        if s3_response.get("ContentType"):
            _kwargs["content_type"] = s3_response["ContentType"]
        response = StreamingHttpResponse(generate_file(s3_response), **_kwargs)
        response["Content-Disposition"] = f'attachment; filename="{original_file_name}"'
        return response


class CaseOfficer(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.data = {"gov_user_pk": case.case_officer.get("id")}
        self.form = assign_case_officer_form(
            request,
            case.case_officer,
            self.kwargs["queue_pk"],
            self.object_pk,
            is_compliance=True if case.case_type["type"]["key"] == CaseType.COMPLIANCE.value else False,
        )
        self.context = {"case": case}
        self.success_url = reverse("cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk})
        self.get_action()

    def get_action(self):
        action = self.get_validated_data().get("_action")
        case_type = self.context["case"]["case_type"]["type"]["key"]

        if action == "delete":
            self.success_message = (
                "Inspector removed" if case_type == CaseType.COMPLIANCE.value else "Case officer removed"
            )
            return delete_case_officer
        else:
            self.success_message = (
                "Inspector set successfully"
                if case_type == CaseType.COMPLIANCE.value
                else "Case officer set successfully"
            )
            return put_case_officer


class UserWorkQueue(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.form = assign_user_and_work_queue(request)
        self.action = get_gov_user_from_form_selection
        self.context = {"case": case}

    def get_success_url(self):
        user_id = self.get_validated_data().get("user").get("id")
        return reverse_lazy(
            "cases:assign_user_queue",
            kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk, "user_pk": user_id},
        )


class UserTeamQueue(SingleFormView):
    def init(self, request, **kwargs):
        user_pk = str(kwargs["user_pk"])
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.form = users_team_queues(request, str(kwargs["pk"]), user_pk)
        self.action = put_queue_single_case_assignment
        self.context = {"case": case}

    def get_success_url(self):
        return reverse_lazy("cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk})


class RerunRoutingRules(SingleFormView):
    def init(self, request, **kwargs):
        self.action = put_rerun_case_routing_rules
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.context = {"case": case}
        self.form = rerun_routing_rules_confirmation_form()
        self.success_url = reverse_lazy(
            "cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk}
        )

    def post(self, request, **kwargs):
        self.init(request, **kwargs)
        if not request.POST.get("confirm"):
            return form_page(
                request,
                self.get_form(),
                data=self.get_data(),
                errors={"confirm": ["select an option"]},
                extra_data=self.context,
            )
        elif request.POST.get("confirm") == "no":
            return redirect(self.success_url)

        return super(RerunRoutingRules, self).post(request, **kwargs)


class NextReviewDate(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_case(request, self.object_pk)
        self.form = set_next_review_date_form(self.kwargs["queue_pk"], self.object_pk,)
        self.success_url = reverse("cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk})

    def get_action(self):
        action = self.get_validated_data().get("_action")

        if action == "submit":
            self.success_message = "Next review date set successfully"
            return put_next_review_date

    def get_data(self):
        data = self.data
        date_fields = ["next_review_date"]
        for field in date_fields:
            if data.get(field, False):
                date_split = data[field].split("-")
                data[field + "year"], data[field + "month"], data[field + "day"] = date_split
        return data
