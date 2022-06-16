from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from exporter.applications.services import get_application_documents
from exporter.applications.summaries import (
    add_product_summary_edit_links,
    add_product_on_application_summary_edit_links,
    firearm_product_summary,
    firearm_product_on_application_summary,
    PRODUCT_SUMMARY_EDIT_LINKS,
    PRODUCT_ON_APPLICATION_SUMMARY_EDIT_LINKS,
)
from exporter.core.helpers import (
    get_organisation_documents,
    has_valid_rfd_certificate as has_valid_organisation_rfd_certificate,
)
from exporter.goods.services import get_good_documents

from .mixins import (
    ApplicationMixin,
    GoodMixin,
    GoodOnApplicationMixin,
    Product2FlagMixin,
)


class FirearmProductSummary(
    LoginRequiredMixin,
    Product2FlagMixin,
    ApplicationMixin,
    GoodMixin,
    TemplateView,
):
    template_name = "applications/goods/firearms/product-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["application_id"] = self.application["id"]
        context["good"] = self.good

        is_user_rfd = has_valid_organisation_rfd_certificate(self.application)
        organisation_documents = get_organisation_documents(self.application)
        summary = firearm_product_summary(
            self.good,
            is_user_rfd,
            organisation_documents,
        )
        summary = add_product_summary_edit_links(
            summary,
            PRODUCT_SUMMARY_EDIT_LINKS,
            self.application,
            self.good,
        )
        context["summary"] = summary

        return context


class BaseProductOnApplicationSummary(
    LoginRequiredMixin,
    Product2FlagMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    TemplateView,
):
    @cached_property
    def is_user_rfd(self):
        return has_valid_organisation_rfd_certificate(self.application)

    @cached_property
    def organisation_documents(self):
        return get_organisation_documents(self.application)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        documents = get_good_documents(self.request, self.good["id"])

        application_documents, _ = get_application_documents(
            self.request,
            self.application["id"],
            self.good["id"],
            include_unsafe=True,
        )
        application_documents = application_documents["documents"]

        good_on_application_documents = {
            document["document_type"].replace("-", "_"): document
            for document in application_documents
            if document["good_on_application"] == self.good_on_application["id"]
        }

        summary_good_on_application_documents = {
            document["document_type"]: document
            for document in application_documents
            if document["good_on_application"] == self.good_on_application["id"]
        }

        product_summary = firearm_product_summary(
            self.good,
            self.is_user_rfd,
            self.organisation_documents,
        )

        product_on_application_summary = firearm_product_on_application_summary(
            self.good_on_application,
            summary_good_on_application_documents,
        )
        product_on_application_summary = add_product_on_application_summary_edit_links(
            product_on_application_summary,
            PRODUCT_ON_APPLICATION_SUMMARY_EDIT_LINKS,
            self.application,
            self.good_on_application,
            self.summary_type,
        )

        return {
            **context,
            "application": self.application,
            "documents": documents,
            "good": self.good,
            "good_on_application": self.good_on_application,
            "good_on_application_documents": good_on_application_documents,
            "product_summary": product_summary,
            "product_on_application_summary": product_on_application_summary,
        }


class FirearmProductOnApplicationSummary(BaseProductOnApplicationSummary):
    summary_type = "product-on-application-summary"
    template_name = "applications/goods/firearms/product-on-application-summary.html"


class FirearmAttachProductOnApplicationSummary(BaseProductOnApplicationSummary):
    summary_type = "attach-product-on-application-summary"
    template_name = "applications/goods/firearms/attach-product-on-application-summary.html"

    def has_added_firearm_category(self):
        return bool(self.request.GET.get("added_firearm_category"))

    def has_confirmed_rfd_validity(self):
        return bool(self.request.GET.get("confirmed_rfd_validity"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["added_firearm_category"] = self.has_added_firearm_category()
        context["confirmed_rfd_validity"] = self.has_confirmed_rfd_validity()

        return context
