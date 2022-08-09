from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin
from core.summaries.utils import (
    pick_fields,
    remove_fields,
)

from exporter.applications.services import get_application_documents
from exporter.applications.summaries.firearm import (
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

from .mixins import Product2FlagMixin
from exporter.applications.views.goods.common.mixins import ApplicationMixin, GoodMixin, GoodOnApplicationMixin


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
    template_name = "applications/goods/firearms/product-on-application-summary.html"

    @cached_property
    def is_user_rfd(self):
        return has_valid_organisation_rfd_certificate(self.application)

    @cached_property
    def organisation_documents(self):
        return get_organisation_documents(self.application)

    def get_product_summary(self):
        product_summary = firearm_product_summary(
            self.good,
            self.is_user_rfd,
            self.organisation_documents,
        )
        return product_summary

    def get_good_on_application_documents(self):
        application_documents, _ = get_application_documents(
            self.request,
            self.application["id"],
            self.good["id"],
            include_unsafe=True,
        )
        application_documents = application_documents["documents"]

        good_on_application_documents = {
            document["document_type"]: document
            for document in application_documents
            if document["good_on_application"] == self.good_on_application["id"]
        }

        return good_on_application_documents

    def get_product_on_application_summary(self):
        product_on_application_summary = firearm_product_on_application_summary(
            self.good_on_application,
            self.get_good_on_application_documents(),
        )
        product_on_application_summary = add_product_on_application_summary_edit_links(
            product_on_application_summary,
            PRODUCT_ON_APPLICATION_SUMMARY_EDIT_LINKS,
            self.application,
            self.good_on_application,
            self.summary_type,
        )
        return product_on_application_summary

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return {
            **context,
            "application": self.application,
            "good": self.good,
            "good_on_application": self.good_on_application,
            "product_summary": self.get_product_summary(),
            "product_on_application_summary": self.get_product_on_application_summary(),
        }


class FirearmProductOnApplicationSummary(BaseProductOnApplicationSummary):
    summary_type = "product-on-application-summary"


class FirearmAttachProductOnApplicationSummary(BaseProductOnApplicationSummary):
    summary_type = "attach-product-on-application-summary"

    def has_added_firearm_category(self):
        return bool(self.request.GET.get("added_firearm_category"))

    def has_confirmed_rfd_validity(self):
        return bool(self.request.GET.get("confirmed_rfd_validity"))

    def get_product_summary(self):
        product_summary = super().get_product_summary()

        if self.has_added_firearm_category():
            self.firearm_category_field = pick_fields(
                product_summary,
                ["firearm-category"],
            )[0]
            product_summary = remove_fields(product_summary, ["firearm-category"])

        return product_summary

    def get_product_on_application_summary(self):
        product_on_application_summary = super().get_product_on_application_summary()

        if self.has_confirmed_rfd_validity():
            product_on_application_summary = (
                (
                    "confirm-rfd-validity",
                    "Yes",
                    "Is your registered firearms dealer certificate still valid?",
                    None,
                ),
            ) + product_on_application_summary

        if self.has_added_firearm_category():
            firearm_category_field = self.firearm_category_field + (None,)
            product_on_application_summary = (firearm_category_field,) + product_on_application_summary

        return product_on_application_summary
