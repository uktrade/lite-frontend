from http import HTTPStatus

from django.contrib import messages
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
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
from cases.helpers import get_updated_cases_banner_queue_id
from cases.services import (
    get_case,
    post_case_notes,
    put_application_status,
    get_activity,
    put_case_queues,
    put_end_user_advisory_query,
    _get_total_goods_value,
    put_goods_query_status,
    get_case_officer,
    put_case_officer,
    delete_case_officer,
    put_unassign_queues,
    get_user_case_queues,
    get_case_additional_contacts,
    post_case_additional_contacts,
)
from cases.services import post_case_documents, get_case_documents, get_document
from conf import settings
from conf.constants import ALL_CASES_QUEUE_ID, GENERATED_DOCUMENT, Statuses
from conf.settings import AWS_STORAGE_BUCKET_NAME
from core.builtins.custom_tags import friendly_boolean
from core.helpers import convert_dict_to_query_params
from core.services import get_status_properties, get_user_permissions, get_permissible_statuses
from lite_content.lite_exporter_frontend import applications
from lite_content.lite_internal_frontend import cases
from lite_content.lite_internal_frontend.cases import CasesListPage
from lite_forms.components import FiltersBar, AutocompleteInput, Option, HiddenField, Select, Checkboxes
from lite_forms.generators import error_page, form_page
from lite_forms.helpers import conditional
from lite_forms.views import SingleFormView
from queues.services import get_cases_search_data, put_queue_single_case_assignment, get_queue
from users.services import get_gov_user_from_form_selection


class Cases(TemplateView):
    def get(self, request, **kwargs):
        """
        Show a list of cases pertaining to that queue.
        """
        case_type = request.GET.get("case_type")
        status = request.GET.get("status")
        sort = request.GET.get("sort")
        queue_id = request.GET.get("queue_id", ALL_CASES_QUEUE_ID)
        case_officer = request.GET.get("case_officer")
        assigned_user = request.GET.get("assigned_user")
        hidden = request.GET.get("hidden")

        # Page parameters
        params = {"page": int(request.GET.get("page", 1))}
        if queue_id:
            params["queue_id"] = queue_id
        if sort:
            params["sort"] = sort
        if status:
            params["status"] = status
        if case_type:
            params["case_type"] = case_type
        if case_officer:
            params["case_officer"] = case_officer
        if assigned_user:
            params["assigned_user"] = assigned_user
        if hidden:
            params["hidden"] = hidden

        data = get_cases_search_data(request, convert_dict_to_query_params(params))
        updated_cases_banner_queue_id = get_updated_cases_banner_queue_id(queue_id, data["results"]["queues"])

        # Filter bar
        filters = data["results"]["filters"]
        statuses = [Option(option["key"], option["value"]) for option in filters["statuses"]]
        case_types = [Option(option["key"], option["value"]) for option in filters["case_types"]]
        gov_users = [Option(option["key"], option["value"]) for option in filters["gov_users"]]

        filters = FiltersBar(
            [
                conditional(queue_id, HiddenField(name="queue_id", value=queue_id)),
                Select(name="case_type", title=CasesListPage.Filters.CASE_TYPE, options=case_types),
                Select(name="status", title=CasesListPage.Filters.CASE_STATUS, options=statuses),
                AutocompleteInput(
                    name="case_officer",
                    title=CasesListPage.Filters.CASE_OFFICER,
                    options=[Option("not_assigned", CasesListPage.Filters.NOT_ASSIGNED), *gov_users],
                ),
                AutocompleteInput(
                    name="assigned_user",
                    title=CasesListPage.Filters.ASSIGNED_USER,
                    options=[Option("not_assigned", CasesListPage.Filters.NOT_ASSIGNED), *gov_users],
                ),
                conditional(
                    data["results"]["is_work_queue"],
                    Checkboxes(
                        name="hidden",
                        options=[Option("true", CasesListPage.Filters.HIDDEN)],
                        classes=["govuk-checkboxes--small"],
                    ),
                ),
            ]
        )

        context = {
            "title": data["results"]["queue"]["name"],
            "data": data,
            "queue": data["results"]["queue"],
            "page": params.pop("page"),
            "params": params,
            "params_str": convert_dict_to_query_params(params),
            "updated_cases_banner_queue_id": updated_cases_banner_queue_id,
            "filters": filters,
            "is_all_cases_queue": queue_id == ALL_CASES_QUEUE_ID,
        }

        return render(request, "cases/index.html", context)

    def post(self, request, **kwargs):
        """ Assign users depending on what cases were selected. """
        queue_id = request.GET.get("queue_id", ALL_CASES_QUEUE_ID)
        return redirect(
            reverse("queues:case_assignments", kwargs={"pk": queue_id})
            + "?cases="
            + ",".join(request.POST.getlist("cases"))
        )


def get_additional_information(case):
    """
    Returns an additional information component to be rendered by templates.
    """
    field_titles = {
        "electronic_warfare_requirement": applications.AdditionalInformation.ELECTRONIC_WARFARE_REQUIREMENT,
        "expedited": applications.AdditionalInformation.EXPEDITED,
        "expedited_date": applications.AdditionalInformation.EXPEDITED_DATE,
        "foreign_technology": applications.AdditionalInformation.FOREIGN_TECHNOLOGY,
        "foreign_technology_type": applications.AdditionalInformation.FOREIGN_TECHNOLOGY_TYPE,
        "locally_manufactured": applications.AdditionalInformation.LOCALLY_MANUFACTURED,
        "mtcr_type": applications.AdditionalInformation.MTCR_TYPE,
        "uk_service_equipment": applications.AdditionalInformation.UK_SERVICE_EQUIPMENT,
        "uk_service_equipment_type": applications.AdditionalInformation.UK_SERVICE_EQUIPMENT_TYPE,
        "value": applications.AdditionalInformation.VALUE,
    }

    values_to_print = []

    for field, title in field_titles.items():
        value = case.get(field)
        if value is not None:
            values_to_print.append(
                {
                    "Number": len(values_to_print) + 1,
                    "Description": title,
                    "Answer": (
                        friendly_boolean(value)
                        if isinstance(value, bool)
                        else value["value"]
                        if isinstance(value, dict)
                        else value
                    ),
                    "SubAnswer": case.get(f"{field}_description") if case.get(field) is True else None,
                }
            )

    return values_to_print


class ViewCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        case = get_case(request, case_id)
        case_type = case["case_type"]["type"]["key"]
        case_sub_type = case["case_type"]["sub_type"]["key"]
        user_assigned_queues, _ = get_user_case_queues(request, case_id)
        queue = None
        queue_id = request.GET.get("queue_id")
        is_system_queue = True

        if queue_id:
            queue = get_queue(request, queue_id)
            if queue.get("queue"):
                queue = queue["queue"]
                is_system_queue = queue.get("is_system_queue", True)
            else:
                queue = None

        if "application" in case:
            status_props, _ = get_status_properties(request, case["application"]["status"]["key"])
            can_set_done = (
                not status_props["is_terminal"] and case["application"]["status"]["key"] != Statuses.APPLICANT_EDITING
            )
        else:
            status_props, _ = get_status_properties(request, case["query"]["status"]["key"])
            can_set_done = (
                not status_props["is_terminal"] and case["query"]["status"]["key"] != Statuses.APPLICANT_EDITING
            )

        context = {
            "activity": get_activity(request, case_id),
            "case": case,
            "queue": queue,
            "permissions": get_user_permissions(request),
            "permissible_statuses": get_permissible_statuses(request, case_type),
            "status_is_read_only": status_props["is_read_only"],
            "status_is_terminal": status_props["is_terminal"],
            "user_assigned_queues": user_assigned_queues["queues"],
            "can_set_done": can_set_done,
            "is_system_queue": is_system_queue,
        }

        if case_sub_type == CaseType.END_USER_ADVISORY.value:
            return render(request, "case/queries/end-user-advisory.html", context)
        elif case_sub_type == CaseType.GOODS.value:
            context["good"] = case["query"]["good"]
            context["verified"] = case["query"]["good"]["status"]["key"] == "verified"
            return render(request, "case/queries/goods-query-case.html", context)
        elif case_sub_type == CaseType.HMRC.value:
            context["total_goods_value"] = _get_total_goods_value(case)
            return render(request, "case/queries/hmrc-case.html", context)
        elif case_sub_type in [
            CaseType.EXHIBITION.value,
            CaseType.F680.value,
            CaseType.GIFTING.value,
        ]:
            if case_sub_type != CaseType.EXHIBITION.value:
                context["total_goods_value"] = _get_total_goods_value(case)
            if case_sub_type == CaseType.F680.value:
                context["case"]["application"]["additional_information"] = get_additional_information(
                    case["application"]
                )
            return render(request, "case/applications/mod-clearance.html", context)
        elif case_type == CaseType.APPLICATION.value:
            context["total_goods_value"] = _get_total_goods_value(case)
            if case_sub_type == CaseType.OPEN.value:
                return render(request, "case/applications/open-licence-case.html", context)
            elif case_sub_type == CaseType.STANDARD.value:
                return render(request, "case/applications/standard-licence-case.html", context)
        raise Exception("Invalid case_sub_type: {}".format(case_sub_type))

    def post(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        response, status_code = post_case_notes(request, case_id, request.POST)

        if status_code != 201:

            errors = response.get("errors")
            if errors.get("text"):
                error = errors.get("text")[0]
                error = error.replace("This field", "Case note")
                error = error.replace("this field", "the case note")  # TODO: Move to API

            else:
                error_list = []
                for key in errors:
                    error_list.append("{field}: {error}".format(field=key, error=errors[key][0]))
                error = "\n".join(error_list)
            return error_page(request, error)

        return redirect(reverse("cases:case", kwargs={"pk": case_id}) + "#case_notes")


class CaseProcessedByUser(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        self.action = put_unassign_queues
        self.form = done_with_case_form(request, self.object_pk)

    def get_success_url(self):
        queue_id = self.request.GET.get("queue_id")
        if queue_id:
            return reverse_lazy("cases:cases") + "?queue_id=" + queue_id
        else:
            return reverse_lazy("cases:cases")


class CaseProcessedByUserForQueue(TemplateView):
    def get(self, request, pk, queue_id):
        data, status_code = put_unassign_queues(request, str(pk), {"queues": [str(queue_id)]})
        if status_code != HTTPStatus.OK:
            return error_page(request, description=data["errors"]["queues"][0],)
        return redirect(reverse_lazy("cases:cases") + "?queue_id=" + str(queue_id))


class ViewAdvice(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        case = get_case(request, case_id)
        activity, _ = get_activity(request, case_id)
        permissions = get_user_permissions(request)

        context = {
            "data": case,
            "activity": activity.get("activity"),
            "permissions": permissions,
            "edit_case_flags": cases.Case.EDIT_CASE_FLAGS,
        }
        return render(request, "case/advice/user.html", context)


class ChangeStatus(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        case = get_case(request, self.object_pk)
        self.case_type = case["case_type"]["type"]["key"]
        self.case_sub_type = case["case_type"]["sub_type"]["key"]
        permissible_statuses = get_permissible_statuses(request, self.case_type)
        self.data = case["application"] if "application" in case else case["query"]
        self.form = change_status_form(case, permissible_statuses)

    def get_action(self):
        if (
            self.case_type == CaseType.APPLICATION.value
            or self.case_sub_type == CaseType.HMRC.value
            or self.case_sub_type == CaseType.EXHIBITION.value
        ):
            return put_application_status
        elif self.case_sub_type == CaseType.END_USER_ADVISORY.value:
            return put_end_user_advisory_query
        elif self.case_sub_type == CaseType.GOODS.value:
            return put_goods_query_status

    def get_success_url(self):
        messages.success(self.request, cases.ChangeStatusPage.SUCCESS_MESSAGE)
        return reverse_lazy("cases:case", kwargs={"pk": self.object_pk})


class MoveCase(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.data = case
        self.form = move_case_form(request, case)
        self.action = put_case_queues

    def get_success_url(self):
        messages.success(self.request, cases.Manage.MoveCase.SUCCESS_MESSAGE)
        return reverse_lazy("cases:case", kwargs={"pk": self.object_pk})


class AdditionalContacts(TemplateView):
    def get(self, request, **kwargs):
        """
        List all documents belonging to a case
        """
        case_id = str(kwargs["pk"])
        case = get_case(request, case_id)
        additional_contacts = get_case_additional_contacts(request, case_id)

        context = {
            "case": case,
            "additional_contacts": additional_contacts,
        }
        return render(request, "case/views/additional-contacts.html", context)


class AddAnAdditionalContact(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = add_additional_contact_form(request, self.object_pk)
        self.action = post_case_additional_contacts
        self.success_message = cases.AdditionalContacts.SUCCESS_MESSAGE
        self.success_url = reverse("cases:additional_contacts", kwargs={"pk": self.object_pk})


class Documents(TemplateView):
    def get(self, request, **kwargs):
        """
        List all documents belonging to a case
        """
        case_id = str(kwargs["pk"])
        case = get_case(request, case_id)
        case_documents, _ = get_case_documents(request, case_id)

        context = {
            "title": cases.Manage.Documents.TITLE,
            "case": case,
            "case_documents": case_documents["documents"],
            "generated_document_key": GENERATED_DOCUMENT,
        }
        return render(request, "case/views/documents.html", context)


@method_decorator(csrf_exempt, "dispatch")
class AttachDocuments(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        get_case(request, case_id)

        form = attach_documents_form(reverse("cases:documents", kwargs={"pk": case_id}))

        return form_page(request, form, extra_data={"case_id": case_id})

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

        return redirect(reverse("cases:documents", kwargs={"pk": case_id}))


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


class CaseOfficer(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        return form_page(request, assign_case_officer_form(request, get_case_officer(request, case_id)[0]),)

    def post(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        user_id = request.POST.get("user")
        action = request.POST.get("_action")

        if action == "delete":
            response, status_code = delete_case_officer(request, case_id)
        else:
            response, status_code = put_case_officer(request, case_id, user_id)

        if status_code != HTTPStatus.NO_CONTENT:
            return form_page(
                request,
                assign_case_officer_form(request, get_case_officer(request, case_id)[0]),
                errors=response.json()["errors"],
            )

        return redirect(reverse_lazy("cases:case", kwargs={"pk": case_id}))


class UserWorkQueue(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = assign_user_and_work_queue(request)
        self.action = get_gov_user_from_form_selection

    @staticmethod
    def _get_form_data(request, case_pk, json):
        return json, HTTPStatus.OK

    def get_success_url(self):
        user_id = self.get_validated_data().get("user").get("id")
        return reverse_lazy("cases:assign_user_queue", kwargs={"pk": self.object_pk, "user_pk": user_id})


class UserTeamQueue(SingleFormView):
    def init(self, request, **kwargs):
        user_pk = str(kwargs["user_pk"])
        self.object_pk = kwargs["pk"]
        self.form = users_team_queues(request, str(kwargs["pk"]), user_pk)
        self.action = put_queue_single_case_assignment

    def get_success_url(self):
        return reverse_lazy("cases:case", kwargs={"pk": self.object_pk})
