from http import HTTPStatus

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from ecju_queries.forms import respond_to_query_form, ecju_query_respond_confirmation_form
from ecju_queries.services import get_ecju_query, put_ecju_query
from goods.services import get_good
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import HiddenField
from lite_forms.generators import form_page, error_page


class RespondToQuery(TemplateView):
    object_type = None
    case_id = None
    ecju_query_id = None
    ecju_query = None
    extra_id = None
    back_link = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs["case_pk"])
        self.object_type = kwargs["object_type"]
        self.ecju_query_id = str(kwargs["query_pk"])
        self.ecju_query = get_ecju_query(request, self.case_id, self.ecju_query_id)

        if self.object_type == "good":
            self.extra_id = kwargs["extra_pk"]
            good, _ = get_good(request, self.extra_id, full_detail=True)
            self.case_id = good["case_id"]
            self.ecju_query = get_ecju_query(request, self.case_id, self.ecju_query_id)

        if self.object_type == "application":
            self.back_link = reverse_lazy(
                "applications:application", kwargs={"pk": self.case_id, "type": "ecju-queries"}
            )
        elif self.object_type == "good":
            self.back_link = reverse_lazy("goods:good_detail", kwargs={"pk": self.extra_id, "type": "ecju-queries"})
        elif self.object_type == "end-user-advisory":
            self.back_link = reverse_lazy(
                "end_users:end_user_detail", kwargs={"pk": self.case_id, "type": "ecju-queries"}
            )
        elif self.object_type == "compliance-site":
            self.back_link = reverse_lazy(
                "compliance:compliance_site_details", kwargs={"pk": self.case_id, "tab": "ecju-queries"}
            )
        elif self.object_type == "compliance-visit":
            self.extra_id = kwargs["extra_pk"]
            self.back_link = reverse_lazy(
                "compliance:compliance_visit_details",
                kwargs={"site_case_id": self.extra_id, "pk": self.case_id, "tab": "ecju-queries"},
            )

        if self.ecju_query["response"]:
            return redirect(self.back_link)

        return super(RespondToQuery, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Will get a text area form for the user to respond to the ecju_query
        """
        return form_page(request, respond_to_query_form(self.back_link, self.ecju_query))

    def post(self, request, **kwargs):
        """
        will determine what form the user is on:
        if the user is on the input form will then will determine if data is valid, and move user to confirmation form
        else will allow the user to confirm they wish to respond and post data if accepted.
        """
        form_name = request.POST.get("form_name")

        if form_name == "respond_to_query":
            # Post the form data to API for validation only
            data = {"response": request.POST.get("response"), "validate_only": True}
            response, status_code = put_ecju_query(request, self.case_id, self.ecju_query_id, data)

            if status_code != HTTPStatus.OK:
                errors = response.get("errors")
                errors = {error: message for error, message in errors.items()}
                form = respond_to_query_form(self.back_link, self.ecju_query)
                data = {"response": request.POST.get("response")}
                return form_page(request, form, data=data, errors=errors)
            else:
                form = ecju_query_respond_confirmation_form(self.request.path_info)
                form.questions.append(HiddenField("response", request.POST.get("response")))
                return form_page(request, form)
        elif form_name == "ecju_query_response_confirmation":
            if request.POST.get("confirm_response") == "yes":
                data, status_code = put_ecju_query(request, self.case_id, self.ecju_query_id, request.POST)

                if "errors" in data:
                    return form_page(
                        request,
                        respond_to_query_form(self.back_link, self.ecju_query),
                        data=request.POST,
                        errors=data["errors"],
                    )

                return redirect(self.back_link)
            elif request.POST.get("confirm_response") == "no":
                return form_page(request, respond_to_query_form(self.back_link, self.ecju_query), data=request.POST)
            else:
                error = {"required": ["This field is required"]}
                form = ecju_query_respond_confirmation_form(self.request.path_info)
                form.questions.append(HiddenField("response", request.POST.get("response")))
                return form_page(request, form, errors=error)
        else:
            # Submitted data does not contain an expected form field - return an error
            return error_page(request, strings.applications.AttachDocumentPage.UPLOAD_GENERIC_ERROR)
