from core.constants import OrganisationDocumentType

from caseworker.cases.helpers.summaries import get_good_on_application_summary
from caseworker.cases.services import (
    get_case,
    get_good_on_application,
    get_good_on_application_documents,
)
from core.auth.views import LoginRequiredMixin

from django.views.generic import TemplateView
from django.utils.functional import cached_property


class GoodDetails(LoginRequiredMixin, TemplateView):
    template_name = "case/product-on-case.html"

    @cached_property
    def object(self):
        return get_good_on_application(self.request, pk=self.kwargs["good_pk"])

    def get_context_data(self, **kwargs):
        case = get_case(self.request, self.kwargs["pk"])

        good_on_application_documents = get_good_on_application_documents(
            self.request,
            self.object["application"],
            self.object["good"]["id"],
        )
        good_on_application_documents = {
            item["document_type"]: item
            for item in good_on_application_documents["documents"]
            if item.get("document_type")
        }

        organisation_documents = {item["document_type"]: item for item in case.organisation["documents"]}

        rfd_certificate = organisation_documents.get(OrganisationDocumentType.RFD_CERTIFICATE)
        is_user_rfd = bool(rfd_certificate) and not rfd_certificate["is_expired"]

        product_summary = get_good_on_application_summary(
            self.request,
            self.object,
            self.kwargs["queue_pk"],
            self.object["application"],
            is_user_rfd,
            organisation_documents,
        )

        return super().get_context_data(
            good_on_application=self.object,
            good_on_application_documents={
                key.replace("-", "_"): value for key, value in good_on_application_documents.items()
            },
            product_summary=product_summary,
            case=case,
            # for pagination
            organisation_documents={key.replace("-", "_"): value for key, value in organisation_documents.items()},
            is_user_rfd=is_user_rfd,
            **kwargs,
        )
