from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView

from exporter.applications.services import (
    get_case_notes,
    get_application_ecju_queries,
    post_case_notes,
    get_case_generated_documents,
)
from core.helpers import convert_parameters_to_query_params
from exporter.end_users.forms import (
    apply_for_an_end_user_advisory_form,
    copy_end_user_advisory_form,
    end_user_advisory_success_page,
)
from exporter.end_users.services import get_end_user_advisories, post_end_user_advisories, get_end_user_advisory
from lite_forms.components import HiddenField, FiltersBar, TextInput
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form

from core.auth.views import LoginRequiredMixin


class EndUsersList(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        params = convert_parameters_to_query_params(
            {"page": request.GET.get("page", 1), "name": request.GET.get("name")}
        )
        end_users = get_end_user_advisories(request, params)

        filters = FiltersBar(
            [
                TextInput(title="name", name="name"),
            ]
        )

        context = {
            "filters": filters,
            "end_users": end_users,
        }
        return render(request, "end-users/end-users.html", context)


class CopyAdvisory(LoginRequiredMixin, TemplateView):

    forms = None
    data = None

    def dispatch(self, request, *args, **kwargs):
        query, _ = get_end_user_advisory(request, str(kwargs["pk"]))

        self.data = {
            "end_user.name": query["end_user"]["name"],
            "end_user.website": query["end_user"]["website"],
            "end_user.address": query["end_user"]["address"],
            "end_user.country": query["end_user"]["country"]["id"],
            "end_user.type": query["end_user"]["type"],
            "reasoning": query.get("reasoning", ""),
            "note": query.get("note", ""),
            "copy_of": query["id"],
            "contact_email": query["contact_email"],
            "contact_telephone": query["contact_telephone"],
        }

        individual, commercial = False, False

        sub_type = query["end_user"]["sub_type"]["key"]
        if sub_type != "individual":
            self.data["contact_name"] = query["contact_name"]
            self.data["contact_job_title"] = query["contact_job_title"]
        else:
            individual = True

        if sub_type == "commercial":
            commercial = True
            self.data["nature_of_business"] = query["nature_of_business"]

        self.forms = copy_end_user_advisory_form(request, individual, commercial)

        # Add the existing end user type as a hidden field to preserve its data
        self.forms.forms[0].questions.append(HiddenField("end_user.sub_type", query["end_user"]["sub_type"]["key"]))

        return super(CopyAdvisory, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0], data=self.data)

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.forms, post_end_user_advisories, inject_data=self.data)

        if response:
            return response

        return end_user_advisory_success_page(request, str(data["end_user_advisory"]["reference_code"]))


class ApplyForAnAdvisory(LoginRequiredMixin, TemplateView):
    forms = None

    def dispatch(self, request, *args, **kwargs):
        individual = request.POST.get("end_user.sub_type") == "individual"
        commercial = request.POST.get("end_user.sub_type") == "commercial"
        self.forms = apply_for_an_end_user_advisory_form(request, individual, commercial)

        return super(ApplyForAnAdvisory, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0])

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.forms, post_end_user_advisories)
        if response:
            return response

        return end_user_advisory_success_page(request, str(data["end_user_advisory"]["reference_code"]))


class EndUserDetailEmpty(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("end_users:end_user_detail", kwargs={"pk": self.kwargs["pk"], "type": "case-notes"})


class EndUserDetail(LoginRequiredMixin, TemplateView):
    end_user_advisory_id = None
    end_user_advisory = None
    view_type = None
    case_id = None

    def dispatch(self, request, *args, **kwargs):
        self.end_user_advisory_id = str(kwargs["pk"])
        self.end_user_advisory, self.case_id = get_end_user_advisory(request, self.end_user_advisory_id)
        self.view_type = kwargs["type"]

        if self.view_type not in ["case-notes", "ecju-queries", "ecju-generated-documents"]:
            return Http404

        return super(EndUserDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        context = {
            "case_id": self.case_id,
            "end_user_advisory": self.end_user_advisory,
            "type": self.view_type,
            "error": kwargs.get("error"),
            "text": kwargs.get("text", ""),
        }

        if self.view_type == "case-notes":
            case_notes = get_case_notes(request, self.case_id)["case_notes"]
            context["notes"] = case_notes

        if self.view_type == "ecju-queries":
            context["open_queries"], context["closed_queries"] = get_application_ecju_queries(request, self.case_id)

        if self.view_type == "ecju-generated-documents":
            generated_documents, _ = get_case_generated_documents(request, self.case_id)
            context["generated_documents"] = generated_documents["results"]

        return render(request, "end-users/end-user.html", context)

    def post(self, request, **kwargs):
        if self.view_type != "case-notes":
            return Http404

        response, _ = post_case_notes(request, self.case_id, request.POST)

        if "errors" in response:
            return self.get(request, error=response["errors"]["text"][0], text=request.POST.get("text"), **kwargs)

        return redirect(
            reverse_lazy("end_users:end_user_detail", kwargs={"pk": self.end_user_advisory_id, "type": "case-notes"})
        )
