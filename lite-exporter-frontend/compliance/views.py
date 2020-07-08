from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.services import (
    get_case_notes,
    post_case_notes,
    get_application_ecju_queries,
    get_case_generated_documents,
)
from compliance.forms import open_licence_return_form_group
from compliance.services import (
    post_open_licence_return,
    get_open_licence_returns,
    get_open_licence_return_download,
    get_compliance_list,
    get_compliance_detail,
    get_case_visit_reports,
    get_case_visit_report,
)
from lite_content.lite_exporter_frontend.compliance import OpenReturnsForm
from lite_forms.generators import success_page
from lite_forms.views import MultiFormView


class ComplianceSiteList(TemplateView):
    def get(self, request, *args, **kwargs):
        data = get_compliance_list(request)
        return render(request, "compliance/compliance/list.html", {"compliance": data})


class ComplianceSiteDetails(TemplateView):
    def get(self, request, pk, tab, **kwargs):
        data = get_compliance_detail(request, pk)
        data["tab"] = tab
        if tab == "case-notes":
            data["notes"] = get_case_notes(request, str(pk))["case_notes"]
        elif tab == "ecju-queries":
            data["open_queries"], data["closed_queries"] = get_application_ecju_queries(request, str(pk))
        elif tab == "generated-documents":
            generated_documents, _ = get_case_generated_documents(request, str(pk))
            data["generated_documents"] = generated_documents["results"]
        elif tab == "visit-reports":
            data["visit_reports"] = get_case_visit_reports(request, str(pk))

        if kwargs.get("errors"):
            data["errors"] = kwargs["errors"]
            data["text"] = kwargs["text"]

        return render(request, "compliance/compliance/site-case.html", data)

    def post(self, request, pk, tab):
        if tab != "case-notes":
            return Http404

        response, _ = post_case_notes(request, str(pk), request.POST)

        if "errors" in response:
            return self.get(request, pk, tab, errors=response["errors"]["text"][0], text=request.POST.get("text"))

        return redirect(reverse_lazy("compliance:compliance_site_details", kwargs={"pk": pk, "tab": tab}))


class ComplianceVisitDetails(TemplateView):
    def get(self, request, site_case_id, pk, tab, **kwargs):
        data = get_case_visit_report(request, pk)
        data["tab"] = tab
        data["site_case_id"] = site_case_id
        if tab == "ecju-queries":
            data["open_queries"], data["closed_queries"] = get_application_ecju_queries(request, str(pk))
        elif tab == "generated-documents":
            generated_documents, _ = get_case_generated_documents(request, str(pk))
            data["generated_documents"] = generated_documents["results"]

        return render(request, "compliance/compliance/visit-case.html", data)


class AnnualReturnsList(TemplateView):
    def get(self, request, *args, **kwargs):
        data = get_open_licence_returns(request)
        return render(request, "compliance/open-licence-returns/list.html", {"open_licence_returns": data})


class AnnualReturnsDownload(TemplateView):
    def get(self, request, pk):
        return get_open_licence_return_download(request, pk)


class AddAnnualReturn(MultiFormView):
    def init(self, request, **kwargs):
        self.additional_context = {
            "columns": [
                OpenReturnsForm.Upload.ExampleTable.LICENCE_COLUMN,
                OpenReturnsForm.Upload.ExampleTable.DESTINATION_COLUMN,
                OpenReturnsForm.Upload.ExampleTable.END_USER_COLUMN,
                OpenReturnsForm.Upload.ExampleTable.USAGE_COLUMN,
                OpenReturnsForm.Upload.ExampleTable.PERIOD_COLUMN,
            ],
            "rows": [
                [
                    OpenReturnsForm.Upload.ExampleTable.LICENCE_EXAMPLE,
                    OpenReturnsForm.Upload.ExampleTable.DESTINATION_EXAMPLE,
                    OpenReturnsForm.Upload.ExampleTable.END_USER_EXAMPLE_COLUMN,
                    OpenReturnsForm.Upload.ExampleTable.USAGE_EXAMPLE,
                    OpenReturnsForm.Upload.ExampleTable.PERIOD_EXAMPLE,
                ]
            ],
        }
        self.forms = open_licence_return_form_group()
        self.action = post_open_licence_return

    def get_success_url(self):
        return reverse_lazy(
            "compliance:add_open_licence_return_success",
            kwargs={"pk": self.get_validated_data()["open_licence_returns"]},
        )


class AddAnnualReturnSuccess(TemplateView):
    def get(self, request, **kwargs):
        return success_page(
            request=request,
            title=OpenReturnsForm.Success.TITLE,
            secondary_title=OpenReturnsForm.Success.SECONDARY_TITLE,
            description=OpenReturnsForm.Success.DESCRIPTION,
            what_happens_next="",
            links={
                OpenReturnsForm.Success.OPEN_LICENCE_RETURNS_LINK: reverse_lazy("compliance:open_licence_returns_list"),
                OpenReturnsForm.Success.HOME_LINK: reverse_lazy("core:home"),
            },
        )
