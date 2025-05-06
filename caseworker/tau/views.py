import copy
import os

from http import HTTPStatus
from urllib.parse import urlencode

from django.contrib import messages
from django.forms import formset_factory
from django.shortcuts import redirect
from django.views.generic import FormView, View, TemplateView
from django.utils.functional import cached_property
from django.urls import reverse

from crispy_forms_gds.helper import FormHelper

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from caseworker.advice.services import move_case_forward
from caseworker.cases.services import get_case
from caseworker.cases.views.main import CaseTabsMixin
from caseworker.core.constants import ALL_CASES_QUEUE_ID
from caseworker.core.services import get_control_list_entries
from caseworker.core.helpers import get_organisation_documents
from caseworker.regimes.enums import Regimes
from caseworker.regimes.services import get_regime_entries, get_regime_entries_all
from caseworker.users.services import get_gov_user
from extra_views import FormSetView

from caseworker.tau.forms import (
    BaseTAUPreviousAssessmentFormSet,
    TAUAssessmentForm,
    TAUEditAssessmentChoiceForm,
    TAUEditAssessmentChoiceFormSet,
    TAUPreviousAssessmentForm,
    TAUMultipleEditForm,
    TAUMultipleEditFormSet,
)
from caseworker.tau.services import (
    get_first_precedents,
    get_good_precedents,
    get_latest_precedents,
    group_gonas_by_good,
    put_bulk_assessment,
)
from caseworker.tau.utils import get_cle_suggestions_json, get_tau_tab_url_name
from caseworker.cases.helpers.case import CaseworkerMixin
from caseworker.queues.services import get_queue

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
    def queue(self):
        return get_queue(self.request, self.queue_id)

    @cached_property
    def case(self):
        case = get_case(self.request, self.case_id)
        for i, good in enumerate(case.goods):
            good["line_number"] = i + 1
        return case

    @cached_property
    def organisation_documents(self):
        """This property will collect the org documents that we need to access
        in the template e.g. section 5 certificate etc."""
        return get_organisation_documents(
            self.case,
            self.queue_id,
        )

    @cached_property
    def goods(self):
        goods = []
        all_precedents = get_good_precedents(self.request, self.case.id)["results"]
        # assign default queues if precedents do not have any
        for precedent in all_precedents:
            precedent["queue"] = precedent.get("queue") or ALL_CASES_QUEUE_ID
        good_precedents = group_gonas_by_good(all_precedents)
        oldest_precedents = get_first_precedents(self.case, good_precedents)
        latest_precedents = get_latest_precedents(self.case, good_precedents)

        for item in self.case.goods:
            item_id = item["id"]
            # Populate precedents
            item["precedents"] = oldest_precedents.get(item_id, [])
            item["latest_precedent"] = latest_precedents.get(item_id, None)
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
        control_list_entries = get_control_list_entries(self.request, include_non_selectable_for_assessment=False)
        return [(item["rating"], item["rating"]) for item in control_list_entries]

    @expect_status(
        HTTPStatus.OK,
        "Error loading regime entries for assessment",
        "Unexpected error loading assessment details",
    )
    def get_regime_entries(self, regime_type):
        return get_regime_entries(self.request, regime_type)

    @cached_property
    def all_regime_entries(self):
        regime_entries, _ = get_regime_entries_all(self.request)
        return [(entry["pk"], entry["name"]) for entry in regime_entries]

    def get_regime_choices(self, regime_type):
        entries, _ = self.get_regime_entries(regime_type)
        return [(entry["pk"], entry["name"]) for entry in entries]

    @cached_property
    def wassenaar_entries(self):
        return self.get_regime_choices(Regimes.WASSENAAR)

    @cached_property
    def mtcr_entries(self):
        return self.get_regime_choices(Regimes.MTCR)

    @cached_property
    def nsg_entries(self):
        return self.get_regime_choices(Regimes.NSG)

    @cached_property
    def cwc_entries(self):
        return self.get_regime_choices(Regimes.CWC)

    @cached_property
    def ag_entries(self):
        return self.get_regime_choices(Regimes.AG)

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
                "tabs": self.get_tabs(),
                "current_tab": get_tau_tab_url_name(),
            }
        )

        return context


def get_regime_entries_payload_data(form_cleaned_data):
    regimes = form_cleaned_data.get("regimes")

    entries = []
    for key, entry_field in [
        (Regimes.MTCR, "mtcr_entries"),
        (Regimes.WASSENAAR, "wassenaar_entries"),
        (Regimes.NSG, "nsg_entries"),
        (Regimes.CWC, "cwc_entries"),
        (Regimes.AG, "ag_entries"),
    ]:
        if key not in regimes:
            continue

        values = form_cleaned_data[entry_field]
        if not isinstance(values, list):
            values = [values]

        entries += values

    return entries


def get_assessment_payload(data, good_on_application_ids):
    # API does not accept `does_not_have_control_list_entries` but it does require `is_good_controlled`.
    # `is_good_controlled`.has an explicit checkbox called "Is a licence required?" in
    # ExportControlCharacteristicsForm. Going forwards, we want to deduce this like so -
    is_good_controlled = not data.pop("does_not_have_control_list_entries")
    assessment = {
        "is_good_controlled": is_good_controlled,
        "regime_entries": get_regime_entries_payload_data(data),
        "control_list_entries": data["control_list_entries"],
        "report_summary_prefix": data["report_summary_prefix"],
        "report_summary_subject": data["report_summary_subject"],
        "is_ncsc_military_information_security": data["is_ncsc_military_information_security"],
        "comment": data["comment"],
    }
    payload = []
    for good_on_application_id in good_on_application_ids:
        assessment_item = copy.deepcopy(assessment)
        assessment_item["id"] = good_on_application_id
        payload.append(assessment_item)

    return payload


class TAUHome(LoginRequiredMixin, TAUMixin, CaseworkerMixin, FormView):
    """This renders a placeholder home page for TAU 2.0."""

    template_name = "tau/home.html"
    form_class = TAUAssessmentForm

    def get_success_url(self):
        return self.request.path

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()

        form_kwargs["request"] = self.request
        form_kwargs["control_list_entries_choices"] = self.control_list_entries
        form_kwargs["wassenaar_entries"] = self.wassenaar_entries
        form_kwargs["mtcr_entries"] = self.mtcr_entries
        form_kwargs["nsg_entries"] = self.nsg_entries
        form_kwargs["cwc_entries"] = self.cwc_entries
        form_kwargs["ag_entries"] = self.ag_entries
        form_kwargs["goods"] = {item["id"]: item for item in self.unassessed_goods}
        form_kwargs["queue_pk"] = self.queue_id
        form_kwargs["application_pk"] = self.case["id"]
        form_kwargs["organisation_documents"] = self.organisation_documents

        rfd_certificate = self.organisation_documents.get("rfd_certificate")
        is_user_rfd = bool(rfd_certificate) and not rfd_certificate["is_expired"]
        form_kwargs["is_user_rfd"] = is_user_rfd

        return form_kwargs

    def get_edit_choice_formset(self, goods_on_applications):
        if not goods_on_applications:
            return None
        AssessmentEditChoiceFormSet = formset_factory(
            TAUEditAssessmentChoiceForm,
            extra=0,
            formset=TAUEditAssessmentChoiceFormSet,
        )
        return AssessmentEditChoiceFormSet(  # pylint: disable=unexpected-keyword-arg
            initial=[{"good_on_application_id": goa["id"]} for goa in goods_on_applications],
            goods_on_applications=goods_on_applications,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formset_helper = FormHelper()
        formset_helper.template = "tau/edit_assessed_products_formset.html"
        context["formset"] = self.get_edit_choice_formset(self.assessed_goods)
        context["formset_helper"] = formset_helper

        return {
            **context,
            "case": self.case,
            "queue_id": self.queue_id,
            "assessed_goods": self.assessed_goods,
            "unassessed_goods": self.unassessed_goods,
            "unassessed_goods_with_precedents": any(
                [bool(good_on_application.get("latest_precedent")) for good_on_application in self.unassessed_goods]
            ),
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
        data = {**form.cleaned_data}

        good_on_application_ids = [good["id"] for good in self.get_goods(data.pop("goods"))]
        payload = get_assessment_payload(data, good_on_application_ids)
        put_bulk_assessment(self.request, self.kwargs["pk"], payload)

        return super().form_valid(form)


class TAUChooseAssessmentEdit(LoginRequiredMixin, TAUMixin, CaseworkerMixin, FormSetView):
    """
    View for posting assessment edit choices to from TAUHome.  Does not provide a
    GET as this should just support POST and redirect to the multiple assessment edit
    page.
    """

    form_class = TAUEditAssessmentChoiceForm
    factory_kwargs = {"extra": 0, "formset": TAUEditAssessmentChoiceFormSet}
    # Required as we inherit from a mixin which requires this
    template_name = "tau/previous_assessments.html"

    def get(self, *args, **kwargs):
        raise NotImplementedError()

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        kwargs["goods_on_applications"] = self.assessed_goods
        return kwargs

    def formset_valid(self, formset):
        line_numbers = []
        for form in formset:
            if form.cleaned_data["selected"]:
                line_numbers.append(form.good_on_application["line_number"])
        params = urlencode({"line_numbers": line_numbers}, doseq=True)
        return redirect(
            reverse("cases:tau:multiple_edit", kwargs={"queue_pk": self.queue_id, "pk": self.case_id}) + f"?{params}"
        )


class TAUPreviousAssessments(LoginRequiredMixin, TAUMixin, CaseworkerMixin, FormSetView):
    template_name = "tau/previous_assessments.html"
    form_class = TAUPreviousAssessmentForm
    factory_kwargs = {"extra": 0, "formset": BaseTAUPreviousAssessmentFormSet}

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        kwargs["goods_on_applications"] = self.unassessed_goods
        return kwargs

    def get_initial(self):
        initial = []

        for good_on_application in self.unassessed_goods:
            good = {}

            good["good_on_application_id"] = good_on_application["id"]

            if good_on_application.get("latest_precedent"):
                good["latest_precedent_id"] = good_on_application["latest_precedent"]["id"]

            initial.append(good)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        formset_helper = FormHelper()
        formset_helper.template = "tau/previous_assessment_formset.html"

        context.update(
            {
                "case": self.case,
                "queue_id": self.queue_id,
                "formset_helper": formset_helper,
                "unassessed_goods": self.unassessed_goods,
                "ALL_CASES_QUEUE_ID": ALL_CASES_QUEUE_ID,
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        if not [good for good in self.unassessed_goods if good["latest_precedent"]]:
            return redirect("cases:tau:home", queue_pk=self.queue_id, pk=self.case_id)

        return super().get(request, *args, **kwargs)

    @expect_status(
        HTTPStatus.OK,
        "Error assessing good with previous assessments",
        "Unexpected error assessing good with previous assessments",
    )
    def assess_with_previous_assessments(self, previous_assessments):
        payload = []
        for good_on_application_id, previous_assessment in previous_assessments.items():
            payload.append(
                {
                    "id": good_on_application_id,
                    "is_good_controlled": previous_assessment["is_good_controlled"],
                    "control_list_entries": previous_assessment["control_list_entries"],
                    "regime_entries": [entry["pk"] for entry in previous_assessment["regime_entries"]],
                    "report_summary_prefix": (
                        previous_assessment["report_summary_prefix"]["id"]
                        if previous_assessment["report_summary_prefix"]
                        else None
                    ),
                    "report_summary_subject": (
                        previous_assessment["report_summary_subject"]["id"]
                        if previous_assessment["report_summary_subject"]
                        else None
                    ),
                    "report_summary": (
                        previous_assessment["report_summary"] if previous_assessment["report_summary"] else None
                    ),
                    "comment": previous_assessment["comment"],
                    "is_ncsc_military_information_security": previous_assessment[
                        "is_ncsc_military_information_security"
                    ],
                }
            )
        return put_bulk_assessment(self.request, self.kwargs["pk"], payload)

    def formset_valid(self, formset):
        # Build a datastructure of previous assessments for each good on application
        # that the user has approved the previous assessment
        previous_assessments = {}
        for form in formset.forms:
            if not form.cleaned_data.get("use_latest_precedent"):
                continue

            application_id = str(form.cleaned_data["good_on_application_id"])
            previous_assessments[application_id] = form.good_on_application["latest_precedent"]
            previous_assessments[application_id]["comment"] = form.cleaned_data.get("comment", "")

        redirect_response = redirect("cases:tau:home", queue_pk=self.queue_id, pk=self.case_id)
        if not previous_assessments:
            return redirect_response

        # Assess these good on applications with the values from the approved previous assessments
        self.assess_with_previous_assessments(previous_assessments)
        messages.success(self.request, f"Assessed {len(previous_assessments)} products using previous assessments.")

        return redirect_response


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
        good_on_application_ids = [good_on_application["id"] for good_on_application in self.assessed_goods]
        clear_assessment = {
            "is_good_controlled": None,
            "regime_entries": [],
            "control_list_entries": [],
            "report_summary": None,
            "report_summary_prefix": None,
            "report_summary_subject": None,
            "is_ncsc_military_information_security": None,
            "comment": None,
        }
        payload = []
        for good_on_application_id in good_on_application_ids:
            assessment_item = copy.deepcopy(clear_assessment)
            assessment_item["id"] = good_on_application_id
            payload.append(assessment_item)
        put_bulk_assessment(self.request, self.kwargs["pk"], payload)

        latest_precedent_exists = any("latest_precedent" in good and good["latest_precedent"] for good in self.goods)

        if latest_precedent_exists:
            return redirect(
                reverse("cases:tau:previous_assessments", kwargs={"queue_pk": self.queue_id, "pk": self.case_id})
            )

        return redirect(reverse("cases:tau:home", kwargs={"queue_pk": self.queue_id, "pk": self.case_id}))


class TAUMultipleEdit(LoginRequiredMixin, TAUMixin, CaseworkerMixin, FormSetView):
    template_name = "tau/multiple_edit.html"
    form_class = TAUMultipleEditForm
    factory_kwargs = {"extra": 0, "formset": TAUMultipleEditFormSet}

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        kwargs["goods_on_applications"] = self.products_to_edit
        kwargs["form_kwargs"] = {
            "control_list_entries_choices": self.control_list_entries,
            "regime_choices": self.all_regime_entries,
        }
        return kwargs

    @cached_property
    def products_to_edit(self):
        # We use line_number as the identifier for our product selection instead of good on application ID.
        # If we used ID instead, it's quite possible that we would run in to URL character limit
        # problems when a user selects a large number of products to edit.
        if not self.request.GET.get("line_numbers"):
            return self.assessed_goods
        products_to_edit = []
        products_by_line_number = {product["line_number"]: product for product in self.assessed_goods}

        valid_line_numbers = []
        for line_number in self.request.GET.getlist("line_numbers"):
            try:
                valid_line_numbers.append(int(line_number))
            except ValueError:
                # Skip invalid line number values rather than raising an exception further
                continue
        ascending_line_numbers = sorted(valid_line_numbers)

        for line_number in ascending_line_numbers:
            product = products_by_line_number.get(line_number)
            if product:
                products_to_edit.append(product)
        return products_to_edit

    def get_initial(self):
        all_initial_data = []

        for good_on_application in self.products_to_edit:
            initial_form_data = {}
            initial_form_data["good_on_application"] = good_on_application
            initial_form_data["id"] = good_on_application["id"]
            raw_is_good_controlled = good_on_application["is_good_controlled"]["key"]
            initial_form_data["licence_required"] = raw_is_good_controlled == "True"
            initial_form_data["refer_to_ncsc"] = good_on_application["is_ncsc_military_information_security"]
            initial_form_data["comment"] = good_on_application["comment"]
            initial_form_data["control_list_entries"] = [
                cle["rating"] for cle in good_on_application["control_list_entries"]
            ]
            initial_form_data["regimes"] = [regime["pk"] for regime in good_on_application["regime_entries"]]
            if good_on_application.get("report_summary_prefix"):
                initial_form_data["report_summary_prefix"] = (
                    good_on_application["report_summary_prefix"] and good_on_application["report_summary_prefix"]["id"]
                )
                initial_form_data["report_summary_prefix_name"] = (
                    good_on_application["report_summary_prefix"]
                    and good_on_application["report_summary_prefix"]["name"]
                )
            if good_on_application.get("report_summary_subject"):
                initial_form_data["report_summary_subject"] = (
                    good_on_application["report_summary_subject"]
                    and good_on_application["report_summary_subject"]["id"]
                )
                initial_form_data["report_summary_subject_name"] = (
                    good_on_application["report_summary_subject"]
                    and good_on_application["report_summary_subject"]["name"]
                )

            all_initial_data.append(initial_form_data)

        return all_initial_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        formset_helper = FormHelper()
        formset_helper.template = "tau/multiple_edit_formset.html"

        context.update(
            {
                "case": self.case,
                "queue_id": self.queue_id,
                "formset_helper": formset_helper,
            }
        )
        return context

    @expect_status(
        HTTPStatus.OK,
        "Error editing assessments",
        "Unexpected error editing assessments",
    )
    def put_assessment_edits(self, payload):
        return put_bulk_assessment(self.request, self.kwargs["pk"], payload)

    def formset_valid(self, formset):
        assessment_edits = []
        for form in formset.forms:
            assessment_edits.append(
                {
                    "id": str(form.cleaned_data["id"]),
                    "is_good_controlled": form.cleaned_data["licence_required"],
                    "control_list_entries": form.cleaned_data["control_list_entries"],
                    "regime_entries": form.cleaned_data["regimes"],
                    "report_summary_prefix": form.cleaned_data["report_summary_prefix"],
                    "report_summary_subject": form.cleaned_data["report_summary_subject"],
                    "comment": form.cleaned_data["comment"],
                    "is_ncsc_military_information_security": form.cleaned_data["refer_to_ncsc"],
                }
            )

        # Assess these good on applications with the values from the approved previous assessments
        self.put_assessment_edits(assessment_edits)
        success_message = (
            f"You have edited {len(assessment_edits)} product assessments on Case {self.case['reference_code']}"
        )
        if len(assessment_edits) == 1:
            success_message = f"You have edited 1 product assessment on Case {self.case['reference_code']}"
        messages.success(self.request, success_message)

        return redirect("cases:tau:home", queue_pk=self.queue_id, pk=self.case_id)
