import logging
from http import HTTPStatus

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import FormView, TemplateView

from core.auth.views import LoginRequiredMixin
from core.constants import (
    CaseStatusEnum,
    FirearmsActDocumentType,
    FirearmsActSections,
)
from core.file_handler import download_document_from_s3

from exporter.applications.helpers.date_fields import format_date
from exporter.applications.services import (
    add_document_data,
    edit_good_on_application_firearm_details_serial_numbers,
    fetch_and_delete_previous_application_documents,
    get_application,
    get_application_documents,
    get_application_ecju_queries,
    get_case_generated_documents,
    get_case_notes,
    get_status_properties,
    post_application_document,
    post_case_notes,
)
from exporter.applications.views.goods import is_firearm_certificate_needed
from exporter.core.helpers import (
    has_valid_rfd_certificate,
    str_to_bool,
)
from exporter.goods.forms import (
    FirearmsActConfirmationForm,
    FirearmsCalibreDetailsForm,
    FirearmsCaptureSerialNumbersForm,
    FirearmsNumberOfItemsForm,
    FirearmsReplicaForm,
    FirearmsYearOfManufactureDetailsForm,
    GroupTwoProductTypeForm,
    IdentificationMarkingsForm,
    ProductComponentForm,
    ProductMilitaryUseForm,
    ProductUsesInformationSecurityForm,
    SoftwareTechnologyDetailsForm,
    UpdateSerialNumbersForm,
    attach_documents_form,
    build_firearm_create_back,
    check_document_available_form,
    delete_good_form,
    document_grading_form,
    edit_good_detail_form,
    edit_grading_form,
    upload_firearms_act_certificate_form,
)
from exporter.goods.helpers import (
    COMPONENT_SELECTION_TO_DETAIL_FIELD_MAP,
    is_firearms_act_status_changed,
    return_to_good_summary,
    get_category_display_string,
)
from exporter.goods.services import (
    delete_good,
    delete_good_document,
    edit_good,
    edit_good_details,
    edit_good_firearm_details,
    edit_good_pv_grading,
    get_good,
    get_good_details,
    get_good_document,
    get_good_documents,
    get_good_on_application,
    get_goods,
    post_good_document_availability,
    post_good_document_sensitivity,
    post_good_documents,
)
from lite_content.lite_exporter_frontend import goods
from lite_content.lite_exporter_frontend.goods import AttachDocumentForm, CreateGoodForm
from lite_forms.components import BackLink, FiltersBar, TextInput
from lite_forms.generators import error_page, form_page
from lite_forms.views import SingleFormView

log = logging.getLogger(__name__)


class GoodCommonMixin:
    """Attributes common to the Goods views."""

    template_name = "core/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_form().title

        return context

    @property
    def application_id(self):
        if "good_pk" in self.kwargs:
            # coming from the application
            return str(self.kwargs["pk"])
        return None

    @property
    def object_id(self):
        if "good_pk" in self.kwargs:
            # coming from the application
            object_pk = str(self.kwargs["good_pk"])
        else:
            object_pk = str(self.kwargs["pk"])
        return object_pk

    @property
    def draft_id(self):
        return str(self.kwargs.get("draft_pk", ""))


class Goods(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        name = request.GET.get("name", "").strip()
        description = request.GET.get("description", "").strip()
        part_number = request.GET.get("part_number", "").strip()
        control_list_entry = request.GET.get("control_list_entry", "").strip()

        filters = FiltersBar(
            [
                TextInput(title="name", name="name"),
                TextInput(title="description", name="description"),
                TextInput(title="control list entry", name="control_list_entry"),
                TextInput(title="part number", name="part_number"),
            ]
        )

        params = {
            "page": int(request.GET.get("page", 1)),
            "name": name,
            "description": description,
            "part_number": part_number,
            "control_list_entry": control_list_entry,
        }

        context = {
            "goods": get_goods(request, **params),
            "name": name,
            "description": description,
            "part_number": part_number,
            "control_list_entry": control_list_entry,
            "filters": filters,
        }
        return render(request, "goods/goods.html", context)


class GoodsDetailEmpty(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        is_preexisting_with_id = ""
        if request.GET.get("is_preexisting") and request.GET.get("application_id"):
            application_id = request.GET.get("application_id")
            is_preexisting_with_id = f"?is_preexisting=true&application_id={application_id}"
        return redirect(
            reverse_lazy("goods:good_detail", kwargs={"pk": kwargs["pk"], "type": "case-notes"})
            + is_preexisting_with_id
        )


class GoodsDetail(LoginRequiredMixin, TemplateView):
    good_id = None
    good = None
    view_type = None

    def dispatch(self, request, *args, **kwargs):
        self.good_id = str(kwargs["pk"])
        self.good = get_good(request, self.good_id, full_detail=True)[0]
        self.view_type = kwargs["type"]

        if self.view_type not in ["application", "case-notes", "ecju-queries", "ecju-generated-documents"]:
            return Http404

        return super(GoodsDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        documents = get_good_documents(request, str(self.good_id))

        # check for query params is_preexisting
        from_preexisting_url = None
        application_id = None
        if request.GET.get("is_preexisting") == "true":
            from_preexisting_url = True
            application_id = request.GET.get("application_id")

        context = {
            "good": self.good,
            "documents": documents,
            "type": self.view_type,
            "error": kwargs.get("error"),
            "text": kwargs.get("text", ""),
            "FEATURE_FLAG_ONLY_ALLOW_SIEL": settings.FEATURE_FLAG_ONLY_ALLOW_SIEL,
            "from_preexisting_url": from_preexisting_url,
            "application_id": application_id,
        }

        if self.good["query"]:
            context["case_id"] = self.good["query"]["id"]
            status_props, _ = get_status_properties(request, self.good["case_status"]["key"])
            context["status_is_read_only"] = status_props["is_read_only"]
            context["status_is_terminal"] = status_props["is_terminal"]

            if self.view_type == "ecju-generated-documents":
                generated_documents, _ = get_case_generated_documents(request, self.good["query"]["id"])
                context["generated_documents"] = generated_documents["results"]

        if self.view_type == "application":
            context["draft_pk"] = str(kwargs.get("draft_pk", ""))

        if self.view_type == "case-notes":
            if self.good.get("case_id"):
                case_notes = get_case_notes(request, self.good["case_id"])["case_notes"]
                context["notes"] = filter(lambda note: note["is_visible_to_exporter"], case_notes)

        if self.view_type == "ecju-queries":
            context["open_queries"], context["closed_queries"] = get_application_ecju_queries(
                request, self.good["case_id"]
            )

        return render(request, "goods/good.html", context)

    def post(self, request, **kwargs):
        if self.view_type != "case-notes":
            return Http404

        good_id = kwargs["pk"]
        data, _ = get_good(request, str(good_id), full_detail=True)

        response, _ = post_case_notes(request, data["case_id"], request.POST)

        if "errors" in response:
            return self.get(request, error=response["errors"]["text"][0], text=request.POST.get("text"), **kwargs)

        return redirect(reverse_lazy("goods:good_detail", kwargs={"pk": good_id, "type": "case-notes"}))


class GoodSoftwareTechnologyView(LoginRequiredMixin, GoodCommonMixin, FormView):
    form_class = SoftwareTechnologyDetailsForm

    @cached_property
    def good_details(self):
        return get_good_details(self.request, self.object_id)[0]

    def get_category_type(self):
        category_type = self.good_details.get("item_category")

        if category_type == "group2_firearms":
            category_type = self.good_details["firearm_details"]["type"]["key"]

        return category_type

    def get_form_title(self):
        return CreateGoodForm.TechnologySoftware.TITLE + get_category_display_string(self.get_category_type())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs["product_type"] = self.get_category_type()

        return kwargs

    def get_initial(self):
        data = self.good_details

        return {
            "software_or_technology_details": data["software_or_technology_details"],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = self.get_form_title()
        return context

    def form_valid(self, form):
        edit_good_details(self.request, self.object_id, form.cleaned_data)

        return super().form_valid(form)

    def get_success_url(self):
        if self.draft_id:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_id, "type": "application", "draft_pk": self.draft_id},
            )
        elif self.application_id and self.object_id:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_id)
        elif self.object_id:
            return reverse("goods:good", kwargs={"pk": self.object_id})


class GoodMilitaryUseView(LoginRequiredMixin, GoodCommonMixin, FormView):
    form_class = ProductMilitaryUseForm

    def get_initial(self):
        data = get_good_details(self.request, self.object_id)[0]

        return {
            "is_military_use": data["is_military_use"],
            "modified_military_use_details": data["modified_military_use_details"],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = self.form_class.title
        return context

    def form_valid(self, form):
        edit_good_firearm_details(self.request, self.object_id, form.cleaned_data)

        return super().form_valid(form)

    def get_success_url(self):
        good = get_good(self.request, self.object_id, full_detail=True)[0]
        is_software_technology = good.get("item_category")["key"] in ["group3_software", "group3_technology"]
        # Next question information security if good is software/hardware

        if is_software_technology:
            if good.get("uses_information_security") is None:
                if "good_pk" in self.kwargs:
                    return reverse(
                        "applications:good_information_security",
                        kwargs={"pk": self.application_id, "good_pk": self.object_id},
                    )
                elif self.draft_id:
                    return reverse(
                        "goods:good_detail_application",
                        kwargs={"pk": self.object_id, "type": "application", "draft_pk": self.draft_id},
                    )
                else:
                    return reverse("goods:good_information_security", kwargs={"pk": self.object_id})

        if self.draft_id:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_id, "type": "application", "draft_pk": self.draft_id},
            )
        elif self.application_id and self.object_id:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_id)
        elif self.object_id:
            return reverse("goods:good", kwargs={"pk": self.object_id})


class GoodComponentView(LoginRequiredMixin, GoodCommonMixin, FormView):
    form_class = ProductComponentForm

    def get_initial(self):
        data = get_good_details(self.request, self.object_id)[0]

        if data.get("is_component") and data.get("component_details"):
            detail_field = COMPONENT_SELECTION_TO_DETAIL_FIELD_MAP[data["is_component"]]
            return {"is_component": data["is_component"], detail_field: data["component_details"]}

        return {"is_component": data.get("is_component")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = self.form_class.title
        return context

    def form_valid(self, form):
        edit_good_details(self.request, self.object_id, form.cleaned_data)

        return super().form_valid(form)

    def get_success_url(self):
        if self.draft_id:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_id, "type": "application", "draft_pk": self.draft_id},
            )
        elif self.application_id and self.object_id:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_id)
        elif self.object_id:
            return reverse("goods:good", kwargs={"pk": self.object_id})


class GoodInformationSecurityView(LoginRequiredMixin, GoodCommonMixin, FormView):
    form_class = ProductUsesInformationSecurityForm

    def get_initial(self):
        data = get_good_details(self.request, self.object_id)[0]

        return {
            "uses_information_security": data["uses_information_security"],
            "information_security_details": data["information_security_details"],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = self.form_class.title
        return context

    def form_valid(self, form):
        edit_good_details(self.request, self.object_id, form.cleaned_data)

        return super().form_valid(form)

    def get_success_url(self):
        if self.draft_id:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_id, "type": "application", "draft_pk": self.draft_id},
            )
        elif self.application_id and self.object_id:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_id)
        elif self.object_id:
            return reverse("goods:good", kwargs={"pk": self.object_id})


class EditGood(LoginRequiredMixin, SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        self.data = get_good(request, self.object_pk)[0]
        self.form = edit_good_detail_form(request, self.object_pk)
        self.action = edit_good

    def get_data(self):
        self.data["control_list_entries"] = [
            {"key": clc["rating"], "value": clc["rating"]} for clc in self.data["control_list_entries"]
        ]
        self.data["is_good_controlled"] = self.data["is_good_controlled"].get("key")
        return self.data

    def get_success_url(self):
        # Return to the application add good summary if adding good from the application
        if "good_pk" in self.kwargs:
            return reverse_lazy(
                "applications:add_good_summary", kwargs={"pk": self.application_id, "good_pk": self.object_pk}
            )
        elif self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        else:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class EditGrading(LoginRequiredMixin, SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        self.data = get_good(request, self.object_pk)[0]
        self.form = edit_grading_form(request, self.object_pk)
        self.action = edit_good_pv_grading

    def get_data(self):
        data = self.data
        if data.get("pv_grading_details", False):
            for k, v in data["pv_grading_details"].items():
                data[k] = v
            date_of_issue = data["date_of_issue"].split("-")
            data["date_of_issueday"] = date_of_issue[2]
            data["date_of_issuemonth"] = date_of_issue[1]
            data["date_of_issueyear"] = date_of_issue[0]

        return data

    def get_success_url(self):
        if "good_pk" in self.kwargs:
            return reverse_lazy(
                "applications:add_good_summary", kwargs={"pk": self.application_id, "good_pk": self.object_pk}
            )
        good = get_good(self.request, self.object_pk, full_detail=True)[0]

        if self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        elif not good.get("documents") and not good.get("is_document_available"):
            return reverse_lazy("goods:add_document", kwargs={"pk": self.object_pk})
        else:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class EditFirearmProductTypeView(LoginRequiredMixin, GoodCommonMixin, FormView):
    form_class = GroupTwoProductTypeForm

    def get_initial(self):
        data = get_good_details(self.request, self.object_id)[0]["firearm_details"]

        return {"type": data["type"]["key"]}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = self.form_class.title
        return context

    def form_valid(self, form):
        edit_good_firearm_details(self.request, self.object_id, form.cleaned_data)

        return super().form_valid(form)

    def get_success_url(self):
        firearm_type = self.request.POST.get("type")

        if firearm_type:
            if "good_pk" in self.kwargs:
                return reverse("applications:edit_good", kwargs={"pk": self.application_id, "good_pk": self.object_id})
            else:
                return reverse("goods:edit", kwargs={"pk": self.object_id})
        elif self.draft_id:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_id, "type": "application", "draft_pk": self.draft_id},
            )
        # Edit
        else:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_id)


class EditYearOfManufactureView(LoginRequiredMixin, GoodCommonMixin, FormView):
    form_class = FirearmsYearOfManufactureDetailsForm

    def get_initial(self):
        data = get_good_details(self.request, self.object_id)[0]["firearm_details"]

        return {
            "year_of_manufacture": data["year_of_manufacture"],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = self.form_class.title
        return context

    def form_valid(self, form):
        edit_good_firearm_details(self.request, self.object_id, form.cleaned_data)

        return super().form_valid(form)

    def get_success_url(self):
        if self.draft_id:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_id, "type": "application", "draft_pk": self.object_id},
            )
        elif self.application_id and self.object_id:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_id)
        elif self.object_id:
            return reverse("goods:good", kwargs={"pk": self.object_id})


class EditFirearmReplicaView(LoginRequiredMixin, GoodCommonMixin, FormView):
    form_class = FirearmsReplicaForm

    @cached_property
    def firearm_details(self):
        return get_good_details(self.request, self.object_id)[0]["firearm_details"]

    def get_initial(self):
        data = self.firearm_details

        return {
            "is_replica": data["is_replica"],
            "replica_description": data["replica_description"],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = self.form_class.title
        return context

    def form_valid(self, form):
        edit_good_firearm_details(
            self.request, self.object_id, {"type": self.firearm_details["type"]["key"], **form.cleaned_data}
        )

        return super().form_valid(form)

    def get_success_url(self):
        if self.draft_id:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_id, "type": "application", "draft_pk": self.draft_id},
            )
        elif self.application_id and self.object_id:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_id)
        elif self.object_id:
            return reverse("goods:good", kwargs={"pk": self.object_id})


class EditCalibreView(LoginRequiredMixin, GoodCommonMixin, FormView):
    form_class = FirearmsCalibreDetailsForm

    def get_initial(self):
        data = get_good_details(self.request, self.object_id)[0]["firearm_details"]

        return {
            "calibre": data["calibre"],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = self.form_class.title
        return context

    def form_valid(self, form):
        edit_good_firearm_details(self.request, self.object_id, form.cleaned_data)

        return super().form_valid(form)

    def get_success_url(self):
        if self.draft_id:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_id, "type": "application", "draft_pk": self.draft_id},
            )
        elif self.application_id and self.object_id:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_id)
        elif self.object_id:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_id})


class EditFirearmActDetailsView(LoginRequiredMixin, GoodCommonMixin, FormView):
    form_class = FirearmsActConfirmationForm

    @cached_property
    def application(self):
        return get_application(self.request, self.kwargs["pk"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["is_rfd"] = has_valid_rfd_certificate(self.application)
        return kwargs

    def get_initial(self):
        data = get_good_details(self.request, self.object_id)[0]["firearm_details"]

        return {
            "is_covered_by_firearm_act_section_one_two_or_five": data[
                "is_covered_by_firearm_act_section_one_two_or_five"
            ],
            "firearms_act_section": data["firearms_act_section"],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = (
            self.form_class.Layout.RFD_FORM_TITLE
            if has_valid_rfd_certificate(self.application)
            else self.form_class.Layout.NON_RFD_FORM_TITLE
        )
        return context

    def form_valid(self, form):
        if "firearms_act_section" not in form.cleaned_data:
            form.cleaned_data["firearms_act_section"] = ""

        edit_good_firearm_details(self.request, self.object_id, form.cleaned_data)

        show_upload_form = str_to_bool(
            form.cleaned_data["is_covered_by_firearm_act_section_one_two_or_five"]
        ) and is_firearm_certificate_needed(
            application=self.application, selected_section=form.cleaned_data["firearms_act_section"]
        )

        if self.draft_id:
            success_url = reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_id, "type": "application", "draft_pk": self.draft_id},
            )
        elif self.application_id and self.object_id:
            # If the new status is that the product is not covered by firearms act or section change
            # then delete the previous certificate
            if is_firearms_act_status_changed(form.data, form.cleaned_data):
                fetch_and_delete_previous_application_documents(self.request, self.application_id, self.object_id)

            if show_upload_form:
                success_url = reverse(
                    "applications:firearms_act_certificate",
                    kwargs={"pk": self.application_id, "good_pk": self.object_id},
                )
            else:
                success_url = return_to_good_summary(self.kwargs, self.application_id, self.object_id)
        else:
            success_url = reverse("goods:good", kwargs={"pk": self.object_id})

        return HttpResponseRedirect(success_url)


class EditFirearmActCertificateDetails(LoginRequiredMixin, SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
            self.back_link = build_firearm_create_back(
                reverse("applications:add_good_summary", kwargs={"pk": self.application_id, "good_pk": self.object_pk})
            )
        else:
            self.back_link = None
            self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        self.data = get_good_details(request, self.object_pk)[0]["firearm_details"]

        self.selected_section = "section"
        if self.data["firearms_act_section"] == FirearmsActSections.SECTION_1:
            self.selected_section = "Section 1"
        elif self.data["firearms_act_section"] == FirearmsActSections.SECTION_2:
            self.selected_section = "Section 2"
        elif self.data["firearms_act_section"] == FirearmsActSections.SECTION_5:
            self.selected_section = "Section 5"

        self.certificate_filename = ""
        if not self.data["section_certificate_missing"]:
            documents, _ = get_application_documents(request, self.application_id, self.object_pk)
            if documents["documents"]:
                self.certificate_filename = documents["documents"][0]["name"]

        self.firearms_data_id = f"edit_{request.session['lite_api_user_id']}_{self.application_id}_{self.object_pk}"
        self.form = upload_firearms_act_certificate_form(
            self.selected_section, self.certificate_filename, self.back_link
        )
        self.action = edit_good_firearm_details

    def get_data(self):
        if self.data:
            expiry_date = self.data.get("section_certificate_date_of_expiry")
            day = month = year = ""
            if expiry_date:
                year, month, day = expiry_date.split("-")
            return {
                "section_certificate_number": self.data.get("section_certificate_number"),
                "section_certificate_date_of_expiryday": day,
                "section_certificate_date_of_expirymonth": month,
                "section_certificate_date_of_expiryyear": year,
                "section_certificate_missing": self.data.get("section_certificate_missing"),
                "section_certificate_missing_reason": self.data.get("section_certificate_missing_reason"),
            }

    def post(self, request, **kwargs):
        self.init(request, **kwargs)
        doc_data = {}
        new_file_selected = False
        file_upload_key = f"{self.firearms_data_id}_file"

        json = {k: v for k, v in request.POST.items()}
        certificate_available = json.get("section_certificate_missing", False) is False

        doc_data, _ = add_document_data(request)
        if doc_data:
            self.request.session[file_upload_key] = doc_data
            self.certificate_filename = doc_data["name"]
            new_file_selected = True
        else:
            file_info = self.request.session.get(file_upload_key)
            if file_info:
                doc_data = file_info
                new_file_selected = True
                self.certificate_filename = file_info["name"]

        # if certificate_available and error and self.certificate_filename == "":
        if certificate_available and self.certificate_filename == "":
            form = upload_firearms_act_certificate_form(
                self.selected_section, self.certificate_filename, self.back_link
            )
            return form_page(request, form, data=json, errors={"file": ["Select certificate file to upload"]})

        validated_data, _ = edit_good_firearm_details(request, kwargs["good_pk"], json)
        if "errors" in validated_data:
            form = upload_firearms_act_certificate_form(
                self.selected_section, self.certificate_filename, self.back_link
            )
            return form_page(request, form, data=json, errors=validated_data["errors"])

        if certificate_available and new_file_selected:
            fetch_and_delete_previous_application_documents(request, kwargs["pk"], kwargs["good_pk"])

            document_types = {
                "Section 1": FirearmsActDocumentType.SECTION_1,
                "Section 2": FirearmsActDocumentType.SECTION_2,
                "Section 5": FirearmsActDocumentType.SECTION_5,
            }

            doc_data["document_on_organisation"] = {
                "expiry_date": format_date(request.POST, "section_certificate_date_of_expiry"),
                "reference_code": request.POST["section_certificate_number"],
                "document_type": document_types[self.selected_section],
            }

            data, status_code = post_application_document(request, kwargs["pk"], kwargs["good_pk"], doc_data)
            if status_code != HTTPStatus.CREATED:
                return error_page(request, data["errors"]["file"])

        if not certificate_available and self.certificate_filename:
            fetch_and_delete_previous_application_documents(request, kwargs["pk"], kwargs["good_pk"])

        if file_upload_key in request.session.keys():
            del self.request.session[file_upload_key]
            self.request.session.modified = True

        return redirect(
            reverse("applications:add_good_summary", kwargs={"pk": kwargs["pk"], "good_pk": kwargs["good_pk"]})
        )

    def get_success_url(self):
        if self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        elif self.application_id and self.object_pk:
            return reverse(
                "applications:add_good_summary", kwargs={"pk": self.application_id, "good_pk": self.object_pk}
            )
        elif self.object_pk:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class EditNumberOfItemsView(LoginRequiredMixin, GoodCommonMixin, FormView):
    form_class = FirearmsNumberOfItemsForm

    def get_initial(self):
        data = get_good_details(self.request, self.object_id)[0]["firearm_details"]

        return {"number_of_items": data["number_of_items"]}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = self.form_class.title
        return context

    def form_valid(self, form):
        edit_good_firearm_details(self.request, self.object_id, form.cleaned_data)

        return super().form_valid(form)

    def get_success_url(self):
        if self.draft_id:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_id, "type": "application", "draft_pk": self.draft_id},
            )
        elif self.application_id and self.object_id:
            return reverse(
                "applications:identification_markings", kwargs={"pk": self.application_id, "good_pk": self.object_id}
            )
        elif self.object_id:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_id})


class EditIdentificationMarkingsView(LoginRequiredMixin, GoodCommonMixin, FormView):
    form_class = IdentificationMarkingsForm

    def get_initial(self):
        data = get_good_details(self.request, self.object_id)[0]["firearm_details"]

        return {
            "serial_numbers_available": data["serial_numbers_available"],
            "no_identification_markings_details": data["no_identification_markings_details"],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = self.form_class.title
        return context

    def form_valid(self, form):
        edit_good_firearm_details(self.request, self.object_id, form.cleaned_data)

        if self.draft_id:
            success_url = reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_id, "type": "application", "draft_pk": self.draft_id},
            )
        elif self.application_id and self.object_id:
            serial_numbers_available = form.cleaned_data["serial_numbers_available"]
            if serial_numbers_available == "AVAILABLE":
                success_url = reverse(
                    "applications:serial_numbers", kwargs={"pk": self.application_id, "good_pk": self.object_id}
                )
            else:
                success_url = return_to_good_summary(self.kwargs, self.application_id, self.object_id)
        else:
            success_url = reverse("goods:good", kwargs={"pk": self.object_id})

        return HttpResponseRedirect(success_url)


class EditSerialNumbersView(LoginRequiredMixin, GoodCommonMixin, FormView):
    form_class = FirearmsCaptureSerialNumbersForm

    @cached_property
    def firearm_details(self):
        return get_good_details(self.request, self.object_id)[0]["firearm_details"]

    def get_initial(self):
        return {"serial_numbers": self.firearm_details["serial_numbers"]}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["number_of_items"] = self.firearm_details["number_of_items"]

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = self.form_class.title
        return context

    def form_valid(self, form):
        edit_good_firearm_details(
            self.request,
            self.object_id,
            {"number_of_items": self.firearm_details["number_of_items"], **form.cleaned_data},
        )

        return super().form_valid(form)

    def get_success_url(self):
        if self.draft_id:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_id, "type": "application", "draft_pk": self.draft_id},
            )
        elif self.application_id and self.object_id:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_id)
        elif self.object_id:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_id})


class DeleteGood(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        data, _ = get_good(request, str(kwargs["pk"]))
        return form_page(request, delete_good_form(data))

    def post(self, request, **kwargs):
        delete_good(request, str(kwargs["pk"]))
        return redirect(reverse_lazy("goods:goods"))


class CheckDocumentAvailable(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.draft_pk = kwargs.get("draft_pk")
        back_url = reverse_lazy("goods:good", kwargs={"pk": self.object_pk})
        if self.draft_pk:
            back_url = reverse_lazy(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        self.form = check_document_available_form(back_url)
        self.action = post_good_document_availability

    def get_success_url(self):
        kwargs = {"pk": self.object_pk}
        if self.draft_pk:
            kwargs["draft_pk"] = self.draft_pk

        if self.request.POST.get("is_document_available") == "no":
            url = "goods:good"
        else:
            url = "goods:check_document_sensitivity"

        return reverse_lazy(url, kwargs=kwargs)


class CheckDocumentGrading(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        return_to_good_page = request.GET.get("goodpage", "no")
        self.object_pk = kwargs["pk"]
        self.draft_pk = kwargs.get("draft_pk")
        if return_to_good_page == "yes":
            back_url = reverse_lazy("goods:good", kwargs={"pk": self.object_pk})
        else:
            back_url = reverse_lazy("goods:check_document_availability", kwargs={"pk": self.object_pk})
        if self.draft_pk:
            back_url = reverse_lazy(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        self.form = document_grading_form(back_url)
        self.action = post_good_document_sensitivity

    def get_success_url(self):
        kwargs = {"pk": self.object_pk}
        if self.draft_pk:
            kwargs["draft_pk"] = self.draft_pk

        if self.request.POST.get("is_document_sensitive") == "yes":
            if self.draft_pk:
                kwargs["type"] = "application"
                url = "goods:good_detail_application"
            else:
                url = "goods:good"
        else:
            if self.draft_pk:
                url = "goods:attach_documents_add_application"
            else:
                url = "goods:attach_documents"

        return reverse_lazy(url, kwargs=kwargs)


class AttachDocuments(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        return_to_good_page = request.GET.get("goodpage", "no")
        good_id = str(kwargs["pk"])
        extra_data = {"good_id": good_id}
        draft_pk = str(kwargs.get("draft_pk", ""))
        if draft_pk:
            extra_data["draft_pk"] = draft_pk
        if return_to_good_page == "yes":
            if draft_pk:
                back_link = BackLink(
                    AttachDocumentForm.BACK_GOOD_LINK,
                    reverse(
                        "goods:good_detail_application",
                        kwargs={"pk": good_id, "type": "application", "draft_pk": draft_pk},
                    ),
                )
            else:
                back_link = BackLink(AttachDocumentForm.BACK_GOOD_LINK, reverse("goods:good", kwargs={"pk": good_id}))
        else:
            if draft_pk:
                back_link = BackLink(
                    AttachDocumentForm.BACK_FORM_LINK,
                    reverse("goods:add_document_add_application", kwargs={"pk": good_id, "draft_pk": draft_pk}),
                )
            else:
                back_link = BackLink(
                    AttachDocumentForm.BACK_FORM_LINK,
                    reverse("goods:check_document_sensitivity", kwargs={"pk": good_id}),
                )
        form = attach_documents_form(back_link)
        return form_page(request, form, extra_data=extra_data)

    def post(self, request, **kwargs):
        draft_pk = str(kwargs.get("draft_pk", ""))
        good_id = str(kwargs["pk"])
        back_link = BackLink(
            AttachDocumentForm.BACK_FORM_LINK,
            reverse("goods:check_document_sensitivity", kwargs={"pk": good_id}),
        )

        data, error = add_document_data(request)
        if error:
            form = attach_documents_form(back_link)
            return form_page(request, form, errors={"file": ["Select a document"]})

        data, status_code = post_good_documents(request, good_id, data)
        if status_code != HTTPStatus.CREATED:
            return error_page(request, data["errors"]["file"])

        if draft_pk:
            return redirect(
                reverse(
                    "goods:good_detail_application",
                    kwargs={"pk": good_id, "type": "application", "draft_pk": draft_pk},
                )
            )
        else:
            return redirect(reverse("goods:good", kwargs={"pk": good_id}))


class Document(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs["pk"])
        file_pk = str(kwargs["file_pk"])

        document = get_good_document(request, good_id, file_pk)
        return download_document_from_s3(document["s3_key"], document["name"])


class DeleteDocument(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs["pk"])
        draft_pk = str(kwargs.get("draft_pk", ""))
        file_pk = str(kwargs["file_pk"])

        document = get_good_document(request, good_id, file_pk)

        context = {
            "title": goods.DeleteGoodDocumentPage.TITLE,
            "good_id": good_id,
            "draft_pk": draft_pk,
            "document": document,
        }
        return render(request, "goods/delete-document.html", context)

    def post(self, request, **kwargs):
        good_id = str(kwargs["pk"])
        draft_pk = str(kwargs.get("draft_pk", ""))
        file_pk = str(kwargs["file_pk"])

        # Delete the file on the API
        delete_good_document(request, good_id, file_pk)

        if draft_pk:
            return redirect(
                reverse(
                    "goods:good_detail_application", kwargs={"pk": good_id, "type": "application", "draft_pk": draft_pk}
                )
            )
        else:
            return redirect(reverse("goods:good", kwargs={"pk": good_id}))


class UpdateSerialNumbersView(LoginRequiredMixin, FormView):
    form_class = UpdateSerialNumbersForm
    template_name = "core/form.html"

    @cached_property
    def application(self):
        return get_application(self.request, self.kwargs["pk"])

    @cached_property
    def firearm_details(self):
        return self.good_on_application["firearm_details"]

    @cached_property
    def good_on_application(self):
        return get_good_on_application(self.request, self.kwargs["good_on_application_pk"])

    @cached_property
    def good(self):
        return self.good_on_application["good"]

    def dispatch(self, *args, **kwargs):
        if self.application["status"]["key"] not in [
            CaseStatusEnum.SUBMITTED,
            CaseStatusEnum.FINALISED,
        ]:
            raise PermissionDenied()

        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs["number_of_items"] = self.firearm_details["number_of_items"]
        kwargs["product_name"] = self.good["name"]

        return kwargs

    def get_initial(self):
        initial = super().get_initial()

        initial["serial_numbers"] = self.firearm_details["serial_numbers"]

        return initial

    def get_success_url(self):
        return reverse("applications:application", kwargs={"pk": self.application["id"]})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["back_link_url"] = self.get_success_url()
        ctx["title"] = self.get_form().title
        ctx["form_title"] = self.get_form().title

        return ctx

    def generate_serial_numbers_data(self, cleaned_data):
        def sort_key(key):
            return int(key.replace("serial_number_input_", ""))

        keys = [key for key in cleaned_data.keys() if key.startswith("serial_number_input_")]
        sorted_keys = sorted(keys, key=sort_key)
        data = [cleaned_data[k] for k in sorted_keys]

        return data

    def form_valid(self, form):
        serial_numbers = self.generate_serial_numbers_data(form.cleaned_data)

        api_resp_data, status_code = edit_good_on_application_firearm_details_serial_numbers(
            self.request,
            self.application["id"],
            self.good_on_application["id"],
            {"serial_numbers": serial_numbers},
        )

        if status_code != HTTPStatus.OK:
            log.error(
                "Error updating serial numbers - response was: %s - %s",
                status_code,
                api_resp_data,
                exc_info=True,
            )
            return error_page(self.request, "Unexpected error updating serial numbers")

        return super().form_valid(form)
