import os

from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import FormView, View, TemplateView
from django.utils.functional import cached_property
from django.urls import reverse

from core.auth.views import LoginRequiredMixin

from caseworker.advice.services import move_case_forward
from caseworker.cases.helpers.summaries import get_good_on_application_summary
from caseworker.cases.services import get_case
from caseworker.cases.views.main import CaseTabsMixin
from caseworker.core.services import get_control_list_entries
from caseworker.cases.services import post_review_good
from caseworker.users.services import get_gov_user

from .forms import TAUAssessmentForm, TAUEditForm
from .services import get_first_precedents
from .utils import get_cle_suggestions_json


TAU_ALIAS = "TAU"


class TAUMixin(CaseTabsMixin):
    """Mixin containing some useful functions used in TAU views."""

    @cached_property
    def case_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def queue_id(self):
        return str(self.kwargs["queue_pk"])

    @cached_property
    def case(self):
        case = get_case(self.request, self.case_id)
        for (i, good) in enumerate(case.goods):
            good["line_number"] = i + 1
        return case

    @cached_property
    def organisation_documents(self):
        """This property will collect the org documents that we need to access
        in the template e.g. section 5 certificate etc."""
        documents = {}
        for item in self.case.organisation["documents"]:
            key = item["document_type"].replace("-", "_")
            documents[key] = item
            item["document"]["url"] = reverse(
                "cases:document",
                kwargs={"queue_pk": self.queue_id, "pk": self.case.id, "file_pk": item["document"]["id"]},
            )
        return documents

    @cached_property
    def goods(self):
        goods = []
        precedents = get_first_precedents(self.request, self.case)
        for item in self.case.goods:
            item_id = item["id"]
            # Populate precedents
            item["precedents"] = precedents.get(item_id, [])
            # Populate document urls
            for document in item["good"]["documents"]:
                _, fext = os.path.splitext(document["name"])
                document["type"] = fext[1:].upper()
                document["url"] = reverse(
                    "cases:document", kwargs={"queue_pk": self.queue_id, "pk": self.case.id, "file_pk": document["id"]}
                )

            # It duplicates these documents in each good but this is unavoidable now
            # because of the way we are rendering each good.
            # Once that is updated then we can remove this.
            item["organisation_documents"] = self.organisation_documents

            goods.append(item)

        return goods

    @cached_property
    def control_list_entries(self):
        control_list_entries = get_control_list_entries(self.request, convert_to_options=True)
        return [(item.value, item.key) for item in control_list_entries]

    def is_assessed(self, good):
        """Returns True if a good has been assessed"""
        return (good["is_good_controlled"] is not None) or (good["control_list_entries"] != [])

    @property
    def assessed_goods(self):
        return [item for item in self.goods if self.is_assessed(item)]

    @property
    def unassessed_goods(self):
        return [item for item in self.goods if not self.is_assessed(item)]

    @property
    def good_id(self):
        return str(self.kwargs["good_id"])

    @property
    def caseworker_id(self):
        return str(self.request.session["lite_api_user_id"])

    @property
    def caseworker(self):
        data, _ = get_gov_user(self.request, self.caseworker_id)
        return data["user"]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update(
            {
                "tabs": self.get_standard_application_tabs(),
                "current_tab": "cases:tau:home",
            }
        )

        return context


class TAUHome(LoginRequiredMixin, TAUMixin, FormView):
    """This renders a placeholder home page for TAU 2.0."""

    template_name = "tau/home.html"
    form_class = TAUAssessmentForm

    def get_success_url(self):
        return self.request.path

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()

        form_kwargs["request"] = self.request
        form_kwargs["control_list_entries_choices"] = self.control_list_entries
        form_kwargs["goods"] = {item["id"]: item for item in self.unassessed_goods}
        form_kwargs["queue_pk"] = self.queue_id
        form_kwargs["application_pk"] = self.case["id"]
        form_kwargs["organisation_documents"] = self.organisation_documents

        rfd_certificate = self.organisation_documents.get("rfd_certificate")
        is_user_rfd = bool(rfd_certificate) and not rfd_certificate["is_expired"]
        form_kwargs["is_user_rfd"] = is_user_rfd

        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            "case": self.case,
            "queue_id": self.queue_id,
            "assessed_goods": self.assessed_goods,
            "unassessed_goods": self.unassessed_goods,
            "cle_suggestions_json": get_cle_suggestions_json(self.unassessed_goods),
            "organisation_documents": self.organisation_documents,
            "is_tau": self.caseworker["team"]["alias"] == TAU_ALIAS,
        }

    def get_goods(self, good_ids):
        good_ids_set = set(good_ids)
        for good in self.goods:
            if good["id"] in good_ids_set:
                yield good

    def form_valid(self, form):
        data = form.cleaned_data
        # API does not accept `does_not_have_control_list_entries` but it does require `is_good_controlled`.
        # `is_good_controlled`.has an explicit checkbox called "Is a licence required?" in
        # ExportControlCharacteristicsForm. Going forwards, we want to deduce this like so -
        is_good_controlled = not data.pop("does_not_have_control_list_entries")
        good_ids = data.pop("goods")

        for good in self.get_goods(good_ids):
            payload = {
                **form.cleaned_data,
                "current_object": good["id"],
                "objects": [good["good"]["id"]],
                "is_good_controlled": is_good_controlled,
            }

            post_review_good(self.request, case_id=self.kwargs["pk"], data=payload)

        return super().form_valid(form)


class TAUEdit(LoginRequiredMixin, TAUMixin, FormView):
    """This renders a form for editing product assessment for TAU 2.0."""

    template_name = "tau/edit.html"
    form_class = TAUEditForm

    def get_success_url(self):
        return reverse("cases:tau:home", kwargs={"queue_pk": self.queue_id, "pk": self.case_id})

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["control_list_entries_choices"] = self.control_list_entries

        good = self.get_good()
        form_kwargs["data"] = self.request.POST or {
            "control_list_entries": [cle["rating"] for cle in good["control_list_entries"]],
            "does_not_have_control_list_entries": good["control_list_entries"] == [],
            "is_wassenaar": "WASSENAAR" in {flag["name"] for flag in good["flags"]},
            "report_summary": good["report_summary"],
            "comment": good["comment"],
        }
        return form_kwargs

    def get_good(self):
        for good in self.goods:
            if good["id"] == self.good_id:
                return good
        raise Http404

    def get_good_on_application_summary(self, good):
        organisation_documents = {
            document["document_type"]: document for document in self.organisation_documents.values()
        }
        rfd_certificate = organisation_documents.get("rfd-certificate")
        is_user_rfd = bool(rfd_certificate) and not rfd_certificate["is_expired"]

        summary = get_good_on_application_summary(
            self.request,
            good,
            self.queue_id,
            self.case["id"],
            is_user_rfd,
            organisation_documents,
        )

        return summary

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        good = self.get_good()
        summary = self.get_good_on_application_summary(good)
        return {
            **context,
            "case": self.case,
            "queue_id": self.queue_id,
            "good": good,
            "summary": summary,
            "organisation_documents": self.organisation_documents,
            "cle_suggestions_json": get_cle_suggestions_json([good]),
        }

    def form_valid(self, form):
        data = form.cleaned_data
        # API does not accept `does_not_have_control_list_entries` but it does require `is_good_controlled`.
        # `is_good_controlled`.has an explicit checkbox called "Is a licence required?" in
        # ExportControlCharacteristicsForm. Going forwards, we want to deduce this like so -
        is_good_controlled = not data.pop("does_not_have_control_list_entries")
        good = self.get_good()

        payload = {
            **form.cleaned_data,
            "current_object": self.good_id,
            "objects": [good["good"]["id"]],
            "is_good_controlled": is_good_controlled,
        }

        post_review_good(self.request, case_id=self.kwargs["pk"], data=payload)
        return super().form_valid(form)


class TAUMoveCaseForward(LoginRequiredMixin, TAUMixin, View):
    """This is a transient view that move the case forward for TAU 2.0
    and redirects to the queue view"""

    def post(self, request, queue_pk, pk):
        queue_pk = str(queue_pk)
        case_pk = str(pk)
        move_case_forward(request, case_pk, queue_pk)
        queue_url = reverse("queues:cases", kwargs={"queue_pk": queue_pk})
        return redirect(queue_url)


class TAUClearAssessments(LoginRequiredMixin, TAUMixin, TemplateView):
    """Clears the assessments for all the goods on the current case."""

    template_name = "tau/clear_assessments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            "case": self.case,
            "queue_id": self.queue_id,
            "assessed_goods": self.assessed_goods,
        }

    def post(self, request, queue_pk, pk):
        for good in self.assessed_goods:
            payload = {
                "control_list_entries": [],
                "is_good_controlled": None,
                "is_wassenaar": False,
                "report_summary": None,
                "comment": None,
                "current_object": good["id"],
                "objects": [good["good"]["id"]],
            }
            post_review_good(self.request, case_id=pk, data=payload)
        return redirect(reverse("cases:tau:home", kwargs={"queue_pk": self.queue_id, "pk": self.case_id}))
