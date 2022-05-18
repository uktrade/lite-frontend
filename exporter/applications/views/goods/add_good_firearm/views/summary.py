from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from exporter.applications.services import (
    get_application,
    get_application_documents,
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
        documents = get_good_documents(self.request, self.good["id"])
        application = get_application(self.request, self.application["id"])
        is_user_rfd = has_valid_organisation_rfd_certificate(application)
        organisation_documents = {k.replace("-", "_"): v for k, v in get_organisation_documents(application).items()}

        return {
            **context,
            "is_user_rfd": is_user_rfd,
            "application_id": self.application["id"],
            "good": self.good,
            "documents": documents,
            "organisation_documents": organisation_documents,
        }


class BaseProductOnApplicationSummary(
    LoginRequiredMixin,
    Product2FlagMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    TemplateView,
):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_user_rfd = has_valid_organisation_rfd_certificate(self.application)

        documents = get_good_documents(self.request, self.good["id"])
        organisation_documents = {
            k.replace("-", "_"): v for k, v in get_organisation_documents(self.application).items()
        }

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

        return {
            **context,
            "application": self.application,
            "documents": documents,
            "good": self.good,
            "good_on_application": self.good_on_application,
            "good_on_application_documents": good_on_application_documents,
            "is_user_rfd": is_user_rfd,
            "organisation_documents": organisation_documents,
        }


class FirearmProductOnApplicationSummary(BaseProductOnApplicationSummary):
    template_name = "applications/goods/firearms/product-on-application-summary.html"


class FirearmAttachProductOnApplicationSummary(BaseProductOnApplicationSummary):
    template_name = "applications/goods/firearms/attach-product-on-application-summary.html"

    def has_added_firearm_category(self):
        return bool(self.request.GET.get("added_firearm_category"))

    def has_confirmed_rfd_validity(self):
        return bool(self.request.GET.get("confirmed_rfd_validity"))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["added_firearm_category"] = self.has_added_firearm_category()
        ctx["confirmed_rfd_validity"] = self.has_confirmed_rfd_validity()

        return ctx
