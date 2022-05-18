from collections import OrderedDict

from django.conf import settings
from formtools.wizard.views import SessionWizardView

from caseworker.cases.forms.review_goods import review_goods_form, ExportControlCharacteristicsForm
from caseworker.cases.helpers.advice import get_param_goods, flatten_goods_data
from caseworker.cases.services import (
    get_case,
    post_review_good,
    post_review_goods,
    get_good_on_application,
    get_good_on_application_documents,
)
from caseworker.search.services import get_application_search_results
from caseworker.search.forms import SearchForm
from caseworker.core.constants import Permission
from caseworker.core.helpers import has_permission
from caseworker.core.services import get_control_list_entries
from caseworker.search.services import get_product_like_this
from core.auth.views import LoginRequiredMixin
from lite_forms.views import SingleFormView

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView
from django.utils.functional import cached_property


class ReviewGoods(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        case_url = reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"]})
        if not has_permission(request, Permission.REVIEW_GOODS):
            return redirect(case_url)
        self.object_pk = kwargs["pk"]

        case = get_case(request, self.object_pk)
        param_goods = get_param_goods(request, case)
        control_list_entries = get_control_list_entries(request, convert_to_options=True)

        self.data = flatten_goods_data(param_goods)
        self.form = review_goods_form(control_list_entries=control_list_entries, back_url=case_url)
        self.context = {"case": case, "goods": param_goods}
        self.action = post_review_goods
        self.success_url = case_url


class AbstractReviewGoodWizardView(SessionWizardView):
    form_class = ExportControlCharacteristicsForm
    # required by view
    form_list = [form_class]
    CACHE_KEY_CONTROL_LIST_ENTRIES = "control_list_entries"

    @cached_property
    def case(self):
        return get_case(self.request, self.kwargs["pk"])

    @property
    def object_pks(self):
        # when user accesses the firs step, it will contain "goods" in the querystring, and will be
        # cached in storage. Then later on POSTs and second page the good pks can be retrieved from storage
        return self.request.GET.getlist(self.object_name) or self.storage.extra_data.get(self.object_name)

    @property
    def object_pk(self):
        return self.object_pks[self.steps.index]

    @property
    def control_list_entries(self):
        if self.CACHE_KEY_CONTROL_LIST_ENTRIES not in self.storage.extra_data:
            data = get_control_list_entries(self.request, convert_to_options=True)
            control_list_entries = [(item.value, item.key) for item in data]
            self.storage.extra_data[self.CACHE_KEY_CONTROL_LIST_ENTRIES] = control_list_entries
        return self.storage.extra_data[self.CACHE_KEY_CONTROL_LIST_ENTRIES]

    def get(self, *args, **kwargs):
        # hack to make the form_list as long as the number of selected goods
        if self.object_name in self.request.GET:
            self.storage.extra_data[self.object_name] = self.request.GET.getlist(self.object_name)
        self.form_list = self.get_form_list()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.form_list = self.get_form_list()
        return super().post(*args, **kwargs)

    def get_form_list(self):
        return OrderedDict((pk, self.form_class) for pk in self.object_pks)

    def get_form_kwargs(self, step):  # noqa pylint incorrectly flagging this
        form_kwargs = super().get_form_kwargs(step)
        form_kwargs["control_list_entries_choices"] = self.control_list_entries
        return form_kwargs

    def get_context_data(self, **kwargs):
        form = kwargs["form"]
        if form.is_bound and not form.is_valid():
            errors = {bound_field.id_for_label: bound_field.errors for bound_field in form}
        else:
            errors = {}
        return super().get_context_data(
            case=self.case, object=self.object, errors=errors, related_products=self.related_products, **kwargs
        )

    def process_step(self, form):
        if self.case["case_type"]["reference"]["key"] != "siel":
            raise ValueError("Only SIEL licences are supported")
        data = {**form.cleaned_data, "current_object": self.object["id"], "objects": [self.object["good"]["id"]]}
        del data["does_not_have_control_list_entries"]
        post_review_good(self.request, case_id=self.kwargs["pk"], data=data)
        return super().process_step(form)

    def done(self, form_list, **kwargs):
        url = reverse("cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})
        return redirect(url)

    @property
    def related_products(self):
        return get_product_like_this(self.request, pk=self.object["id"])


class ReviewStandardApplicationGoodWizardView(AbstractReviewGoodWizardView):
    object_name = "goods"
    template_name = "case/review-good-standard.html"

    @property
    def object(self):
        return next(item for item in self.case.goods if item["id"] == self.object_pk)

    def get_form_initial(self, step):
        current_step_object = next(item for item in self.case.goods if item["id"] == step)

        # if the good was reviewed at application level then use that as source of truth, otherwise use the export
        # control characteristics from the canonical good level
        if self.object["is_good_controlled"] is None:
            source = current_step_object["good"]
        else:
            source = current_step_object
        is_good_controlled = source["is_good_controlled"]
        initial = {
            "is_good_controlled": is_good_controlled["key"] if is_good_controlled else None,
            "does_not_have_control_list_entries": not source["control_list_entries"],
            "control_list_entries": [item["rating"] for item in source["control_list_entries"]],
            "report_summary": current_step_object["report_summary"],
            "comment": source["comment"],
            "end_use_control": self.object["end_use_control"],
            "is_precedent": self.object.get("is_precedent", False),
        }
        initial.update(super().get_form_initial(step))
        return initial

    def get_context_data(self, **kwargs):
        # if the good was reviewed at application level then use that as source of truth, otherwise use the export
        # control characteristics from the canonical good level
        documents = {
            item["document_type"].replace("-", "_"): item
            for item in self.case["data"]["organisation"].get("documents", [])
        }

        if self.object["is_good_controlled"] is not None:
            control_list_entries = self.object["control_list_entries"]
        else:
            control_list_entries = self.object["good"]["control_list_entries"]
        return super().get_context_data(
            object_control_list_entries=control_list_entries, organisation_documents=documents, **kwargs
        )


class ReviewOpenApplicationGoodWizardView(AbstractReviewGoodWizardView):
    object_name = "goods_types"
    template_name = "case/review-good-open.html"

    @property
    def object(self):
        return next(item for item in self.case.goods if item["id"] == self.object_pk)

    def get_form_initial(self, step):
        # unlike ReviewGoodOnApplicationWizardView, goods_type has no distinction of "good" and "good on application"
        initial = {
            "is_good_controlled": self.object["is_good_controlled"],
            "does_not_have_control_list_entries": not self.object["control_list_entries"],
            "control_list_entries": [item["rating"] for item in self.object["control_list_entries"]],
            "report_summary": self.object["report_summary"],
            "comment": self.object["comment"],
            "end_use_control": self.object["end_use_control"],
        }
        initial.update(super().get_form_initial(step))
        return initial

    def get_context_data(self, **kwargs):
        return super().get_context_data(object_control_list_entries=self.object["control_list_entries"], **kwargs)


class GoodDetails(LoginRequiredMixin, FormView):
    form_class = SearchForm

    def get_template_names(self):
        product_1_template = "case/product-on-case.html"

        if not settings.FEATURE_FLAG_PRODUCT_2_0:
            return product_1_template

        firearm_details = self.object.get("firearm_details")
        if not firearm_details:
            return product_1_template

        if firearm_details["type"]["key"] != "firearms":
            return product_1_template

        return "case/product-on-case-product2-0.html"

    @cached_property
    def object(self):
        return get_good_on_application(self.request, pk=self.kwargs["good_pk"])

    @cached_property
    def other_cases(self):
        form = self.get_form()
        search_string = self.get_initial()["search_string"]
        if search_string:
            return get_application_search_results(self.request, query_params=form.extract_filters(search_string))
        return []

    def get_initial(self):
        search_string = ""
        part_number = self.object["good"]["part_number"]
        if part_number:
            search_string += f'part:"{part_number}"'
        control_list_entries = self.object["control_list_entries"] or self.object["good"]["control_list_entries"]
        for item in control_list_entries:
            search_string += f' clc_rating:"{item["rating"]}"'
        return {"search_string": search_string.strip()}

    def get_context_data(self, **kwargs):
        form = self.get_form()

        case = get_case(self.request, self.kwargs["pk"])

        good_on_application_documents = get_good_on_application_documents(
            self.request,
            self.object["application"],
            self.object["good"]["id"],
        )
        good_on_application_documents = {
            item["document_type"].replace("-", "_"): item for item in good_on_application_documents["documents"]
        }

        organisation_documents = {
            item["document_type"].replace("-", "_"): item for item in case.organisation["documents"]
        }

        rfd_certificate = organisation_documents.get("rfd_certificate")
        is_user_rfd = bool(rfd_certificate) and not rfd_certificate["is_expired"]

        return super().get_context_data(
            good_on_application=self.object,
            good_on_application_documents=good_on_application_documents,
            case=case,
            other_cases=self.other_cases,
            # for pagination
            data={"total_pages": self.other_cases["count"] // form.page_size} if self.other_cases else {},
            organisation_documents=organisation_documents,
            is_user_rfd=is_user_rfd,
            **kwargs,
        )
