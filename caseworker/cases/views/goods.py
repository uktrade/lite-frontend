from core.constants import OrganisationDocumentType

from caseworker.cases.helpers.summaries import get_good_on_application_summary
from caseworker.cases.services import (
    get_case,
    get_good_on_application,
    get_good_on_application_documents,
)
from caseworker.cases.forms.goods import GoodDetailsForm
from caseworker.search.services import get_application_search_results
from core.auth.views import LoginRequiredMixin

from django.views.generic import FormView
from django.utils.functional import cached_property


class GoodDetails(LoginRequiredMixin, FormView):
    form_class = GoodDetailsForm
    template_name = "case/product-on-case.html"

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
            other_cases=self.other_cases,
            # for pagination
            data={"total_pages": self.other_cases["count"] // form.page_size} if self.other_cases else {},
            organisation_documents={key.replace("-", "_"): value for key, value in organisation_documents.items()},
            is_user_rfd=is_user_rfd,
            **kwargs,
        )
