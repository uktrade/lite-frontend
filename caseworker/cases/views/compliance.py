from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from caseworker.cases.forms.compliance import (
    visit_report_form,
    people_present_form,
    overview_form,
    inspection_form,
    compliance_with_licence_form,
    knowledge_of_people_form,
    knowledge_of_products_form,
)
from caseworker.cases.services import (
    post_create_compliance_visit,
    patch_compliance_visit_case,
    get_compliance_visit_case,
    post_compliance_person_present,
    get_case,
    get_compliance_people_present,
)
from lite_content.lite_internal_frontend.cases import ComplianceForms
from lite_forms.views import SingleFormView

from core.auth.views import LoginRequiredMixin


class CreateVisitReport(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        response = post_create_compliance_visit(request, case_id)

        new_case_id = response.json()["data"]["id"]

        return redirect(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": new_case_id, "tab": "details"})
        )


class PeoplePresent(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.context = {"case": get_case(request, self.object_pk)}
        self.data = {"people_present": get_compliance_people_present(request, self.object_pk)}
        self.form = people_present_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)
        self.success_message = ComplianceForms.PeoplePresent.SUCCESS
        self.action = post_compliance_person_present

    def on_submission(self, request, **kwargs):
        data = request.POST.copy()
        data["people_present"] = []

        for i in range(len(data.getlist("name[]"))):
            data["people_present"].append(
                {
                    "name": data.getlist("name[]")[i],
                    "job_title": data.getlist("job_title[]")[i],
                }
            )

        data["visit_case"] = str(kwargs["pk"])
        return data


class ComplianceVisitBaseForm(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.success_url = reverse("cases:case", kwargs=kwargs)
        self.action = patch_compliance_visit_case
        self.data = get_compliance_visit_case(request, kwargs["pk"])


class VisitReportDetails(LoginRequiredMixin, ComplianceVisitBaseForm):
    def init(self, request, **kwargs):
        super().init(request, **kwargs)
        self.form = visit_report_form(kwargs["queue_pk"], kwargs["pk"])

    def get_data(self):
        data = self.data
        field = "visit_date"
        if data.get(field, False):
            date_split = data[field].split("-")
            data[field + "_year"], data[field + "_month"], data[field + "_day"] = date_split
        return data


class Overview(LoginRequiredMixin, ComplianceVisitBaseForm):
    def init(self, request, **kwargs):
        super().init(request, **kwargs)
        self.form = overview_form(kwargs["queue_pk"], kwargs["pk"])


class Inspection(LoginRequiredMixin, ComplianceVisitBaseForm):
    def init(self, request, **kwargs):
        super().init(request, **kwargs)
        self.form = inspection_form(kwargs["queue_pk"], kwargs["pk"])


class ComplianceWithLicences(LoginRequiredMixin, ComplianceVisitBaseForm):
    def init(self, request, **kwargs):
        super().init(request, **kwargs)
        self.form = compliance_with_licence_form(kwargs["queue_pk"], kwargs["pk"])


class KnowledgePeople(LoginRequiredMixin, ComplianceVisitBaseForm):
    def init(self, request, **kwargs):
        super().init(request, **kwargs)
        self.form = knowledge_of_people_form(kwargs["queue_pk"], kwargs["pk"])


class KnowledgeProduct(LoginRequiredMixin, ComplianceVisitBaseForm):
    def init(self, request, **kwargs):
        super().init(request, **kwargs)
        self.form = knowledge_of_products_form(kwargs["queue_pk"], kwargs["pk"])
