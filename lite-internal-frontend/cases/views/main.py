from http import HTTPStatus
from django.http import StreamingHttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler, s3_client

from cases.constants import CaseType
from cases.forms.attach_documents import attach_documents_form
from cases.forms.move_case import move_case_form
from cases.helpers import get_updated_cases_banner_queue_id
from cases.services import (
    get_case,
    post_case_notes,
    put_application_status,
    get_activity,
    put_case,
    put_end_user_advisory_query,
    _get_total_goods_value,
    put_clc_query_status,
    get_case_officer,
    put_case_officer,
    delete_case_officer,
)
from cases.services import post_case_documents, get_case_documents, get_document
from conf import settings
from conf.constants import DEFAULT_QUEUE_ID, GENERATED_DOCUMENT
from conf.settings import AWS_STORAGE_BUCKET_NAME
from core.helpers import convert_dict_to_query_params
from core.services import get_status_properties, get_user_permissions, get_permissible_statuses
from lite_content.lite_internal_frontend import cases
from lite_forms.generators import error_page, form_page
from lite_forms.views import SingleFormView
from queues.services import get_cases_search_data
from users.services import get_gov_users


class Cases(TemplateView):
    def get(self, request, **kwargs):
        """
        Show a list of cases pertaining to that queue
        """
        case_type = request.GET.get("case_type")
        status = request.GET.get("status")
        sort = request.GET.get("sort")
        queue_id = request.GET.get("queue_id")

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

        data = get_cases_search_data(request, convert_dict_to_query_params(params))

        updated_cases_banner_queue_id = get_updated_cases_banner_queue_id(queue_id, data["results"]["queues"])

        context = {
            "title": data["results"]["queue"]["name"],
            "data": data,
            "queue": data["results"]["queue"],
            "page": params.pop("page"),
            "params": params,
            "params_str": convert_dict_to_query_params(params),
            "updated_cases_banner_queue_id": updated_cases_banner_queue_id,
        }

        return render(request, "cases/index.html", context)

    def post(self, request, **kwargs):
        """ Assign users depending on what cases were selected. """
        queue_id = request.GET.get("queue_id", DEFAULT_QUEUE_ID)
        return redirect(
            reverse("queues:case_assignments", kwargs={"pk": queue_id})
            + "?cases="
            + ",".join(request.POST.getlist("cases"))
        )


class ViewCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        case = get_case(request, case_id)
        case_type = case["type"]["key"]

        if "application" in case:
            status_props, _ = get_status_properties(request, case["application"]["status"]["key"])
        else:
            status_props, _ = get_status_properties(request, case["query"]["status"]["key"])

        context = {
            "activity": get_activity(request, case_id),
            "case": case,
            "permissions": get_user_permissions(request),
            "permissible_statuses": get_permissible_statuses(request, case_type),
            "status_is_read_only": status_props["is_read_only"],
            "status_is_terminal": status_props["is_terminal"],
        }

        if case_type == CaseType.END_USER_ADVISORY_QUERY.value:
            return render(request, "case/queries/end_user_advisory.html", context)
        elif case_type == CaseType.CLC_QUERY.value:
            context["good"] = case["query"]["good"]
            context["verified"] = case["query"]["good"]["status"]["key"] == "verified"
            return render(request, "case/queries/clc-query-case.html", context)
        elif case_type == CaseType.APPLICATION.value:
            context["total_goods_value"] = _get_total_goods_value(case)

            application_type = case["application"]["application_type"]["key"]
            if application_type == CaseType.OPEN_LICENCE.value:
                return render(request, "case/applications/open-licence-case.html", context)
            elif application_type == CaseType.STANDARD_LICENCE.value:
                return render(request, "case/applications/standard-licence-case.html", context)
            else:
                raise Exception("Invalid application_type: {}".format(case["application"]["application_type"]["key"]))
        elif case_type == CaseType.HMRC_QUERY.value:
            context["total_goods_value"] = _get_total_goods_value(case)
            return render(request, "case/queries/hmrc-case.html", context)
        else:
            raise Exception("Invalid case_type: {}".format(case_type))

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


class ManageCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        case = get_case(request, case_id)
        case_type = case["type"]["key"]
        permissible_statuses = get_permissible_statuses(request, case_type)

        if case_type == CaseType.APPLICATION.value:
            title = cases.ChangeStatusPage.TITLE_APPLICATION
        elif case_type == CaseType.HMRC_QUERY.value:
            title = cases.ChangeStatusPage.TITLE_APPLICATION
        elif case_type == CaseType.END_USER_ADVISORY_QUERY.value:
            title = cases.ChangeStatusPage.TITLE_EUA
        elif case_type == CaseType.CLC_QUERY.value:
            title = cases.ChangeStatusPage.TITLE_CLC
        else:
            raise Exception("Invalid case_type: {}".format(case_type))

        context = {"case": case, "title": title, "statuses": permissible_statuses}
        return render(request, "case/views/change-status.html", context)

    def post(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        case = get_case(request, case_id)

        if case["type"]["key"] == CaseType.APPLICATION.value or case["type"]["key"] == CaseType.HMRC_QUERY.value:
            application_id = case.get("application").get("id")
            put_application_status(request, application_id, request.POST)
        elif case["type"]["key"] == CaseType.END_USER_ADVISORY_QUERY.value:
            query_id = case.get("query").get("id")
            put_end_user_advisory_query(request, query_id, request.POST)
        elif case["type"]["key"] == CaseType.CLC_QUERY.value:
            query_id = case.get("query").get("id")
            put_clc_query_status(request, query_id, request.POST)
        else:
            raise Http404

        return redirect(reverse("cases:case", kwargs={"pk": case_id}))


class MoveCase(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.data = case
        self.form = move_case_form(request, case)
        self.action = put_case
        self.success_url = reverse_lazy("cases:case", kwargs={"pk": self.object_pk})


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
        case = get_case(request, case_id)
        params = {"name": request.GET.get("name", ""), "activated": True}
        gov_users, _ = get_gov_users(request, params)

        context = {
            "case_officer": get_case_officer(request, case_id)[0],
            "users": gov_users,
            "case": case,
            "name": params["name"],
        }
        return render(request, "case/views/set-case-officer.html", context)

    def post(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        user_id = request.POST.get("user")
        action = request.POST.get("_action")

        if action == "assign":
            if not user_id:
                case = get_case(request, case_id)
                params = {"name": request.GET.get("name", ""), "activated": True}
                gov_users, _ = get_gov_users(request, params)

                context = {
                    "error": cases.CaseOfficerPage.Error.NO_SELECTION,
                    "case_officer": get_case_officer(request, case_id)[0],
                    "users": gov_users,
                    "case": case,
                    "name": request.GET.get("name", ""),
                }
                return render(request, "case/views/set-case-officer.html", context)

            _, status_code = put_case_officer(request, case_id, user_id)

        elif action == "unassign":
            _, status_code = delete_case_officer(request, case_id)

        if status_code != HTTPStatus.NO_CONTENT:
            self.response_error(request, case_id)

        return redirect(reverse_lazy("cases:case", kwargs={"pk": case_id}))

    def response_error(self, request, case_id):
        case = get_case(request, case_id)
        params = {"name": request.GET.get("name", ""), "activated": True}
        gov_users, _ = get_gov_users(request, params)

        context = {
            "show_error": True,
            "case_officer": get_case_officer(request, case_id)[0],
            "users": gov_users,
            "case": case,
            "name": params["name"],
        }
        return render(request, "case/views/set-case-officer.html", context)
