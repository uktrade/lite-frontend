from http import HTTPStatus

from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler

from exporter.applications.services import (
    get_application_ecju_queries,
    get_case_notes,
    post_case_notes,
    add_document_data,
    download_document_from_s3,
    get_status_properties,
    get_case_generated_documents,
    post_application_document,
    get_application_documents,
    fetch_and_delete_previous_application_documents,
)
from exporter.core.constants import FIREARM_AMMUNITION_COMPONENT_TYPES
from exporter.goods.forms import (
    attach_documents_form,
    delete_good_form,
    document_grading_form,
    raise_a_goods_query,
    add_good_form_group,
    edit_good_detail_form,
    edit_grading_form,
    product_military_use_form,
    product_component_form,
    product_uses_information_security,
    software_technology_details_form,
    group_two_product_type_form,
    firearm_calibre_details_form,
    firearms_act_confirmation_form,
    upload_firearms_act_certificate_form,
    build_firearm_create_back,
    identification_markings_form,
    firearms_sporting_shotgun_form,
    firearm_year_of_manufacture_details_form,
    firearm_replica_form,
)
from exporter.goods.helpers import (
    COMPONENT_SELECTION_TO_DETAIL_FIELD_MAP,
    return_to_good_summary,
    is_firearms_act_status_changed,
)
from exporter.goods.services import (
    get_goods,
    post_goods,
    get_good,
    edit_good,
    delete_good,
    get_good_documents,
    get_good_document,
    post_good_documents,
    delete_good_document,
    raise_goods_query,
    post_good_document_sensitivity,
    validate_good,
    edit_good_pv_grading,
    edit_good_details,
    get_good_details,
    edit_good_firearm_details,
)
from lite_content.lite_exporter_frontend import goods
from lite_content.lite_exporter_frontend.goods import AttachDocumentForm
from lite_forms.components import BackLink, FiltersBar, TextInput
from lite_forms.generators import error_page, form_page
from lite_forms.views import SingleFormView, MultiFormView

from core.auth.views import LoginRequiredMixin


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
        return redirect(reverse("goods:good_detail", kwargs={"pk": kwargs["pk"], "type": "case-notes"}))


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

        context = {
            "good": self.good,
            "documents": documents,
            "type": self.view_type,
            "error": kwargs.get("error"),
            "text": kwargs.get("text", ""),
            "FEATURE_FLAG_ONLY_ALLOW_SIEL": settings.FEATURE_FLAG_ONLY_ALLOW_SIEL,
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


class AddGood(LoginRequiredMixin, MultiFormView):
    def init(self, request, **kwargs):
        self.forms = add_good_form_group(request)
        self.action = validate_good

    def on_submission(self, request, **kwargs):
        copied_request = request.POST.copy()
        is_pv_graded = copied_request.get("is_pv_graded", "").lower() == "yes"
        is_software_technology = copied_request.get("item_category") in ["group3_software", "group3_technology"]
        is_firearm = copied_request.get("type") == "firearms"
        is_firearms_core = copied_request.get("type") in FIREARM_AMMUNITION_COMPONENT_TYPES
        is_firearms_accessory = copied_request.get("type") == "firearms_accessory"
        is_firearms_software_tech = copied_request.get("type") in [
            "software_related_to_firearms",
            "technology_related_to_firearms",
        ]
        self.forms = add_good_form_group(
            request,
            is_pv_graded,
            is_software_technology,
            is_firearm,
            is_firearms_core,
            is_firearms_accessory,
            is_firearms_software_tech,
            base_form_back_link=reverse("goods:goods"),
        )

        # we require the form index of the last form in the group, not the total number
        number_of_forms = len(self.forms.get_forms()) - 1

        if int(self.request.POST.get("form_pk")) == number_of_forms:
            self.action = post_goods

    def get_success_url(self):
        return reverse_lazy("goods:add_document", kwargs={"pk": self.get_validated_data()["good"]["id"]})


class GoodSoftwareTechnology(LoginRequiredMixin, SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        self.data = get_good_details(request, self.object_pk)[0]
        category_type = self.data.get("item_category")
        if category_type == "group2_firearms":
            category_type = self.data["firearm_details"]["type"]["key"]
        self.form = software_technology_details_form(request, category_type)
        self.action = edit_good_details

    def get_data(self):
        return {
            "software_or_technology_details": self.data.get("software_or_technology_details"),
        }

    def get_success_url(self):
        if self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        elif self.application_id and self.object_pk:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_pk)
        elif self.object_pk:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class GoodMilitaryUse(LoginRequiredMixin, SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        self.data = get_good_details(request, self.object_pk)[0]
        self.form = product_military_use_form(request)
        self.action = edit_good_details

    def get_data(self):
        new_data = {
            "is_military_use": self.data.get("is_military_use"),
            "modified_military_use_details": self.data.get("modified_military_use_details"),
        }
        return new_data

    def get_success_url(self):
        good = get_good(self.request, self.object_pk, full_detail=True)[0]
        is_software_technology = good.get("item_category")["key"] in ["group3_software", "group3_technology"]
        # Next question information security if good is software/hardware
        if is_software_technology:
            if good.get("uses_information_security") is None:
                if "good_pk" in self.kwargs:
                    return reverse_lazy(
                        "applications:good_information_security",
                        kwargs={"pk": self.application_id, "good_pk": self.object_pk},
                    )
                elif self.draft_pk:
                    return reverse(
                        "goods:good_detail_application",
                        kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
                    )
                else:
                    return reverse_lazy("goods:good_information_security", kwargs={"pk": self.object_pk})

        if self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        elif self.application_id and self.object_pk:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_pk)
        elif self.object_pk:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class GoodComponent(LoginRequiredMixin, SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        self.data = get_good_details(request, self.object_pk)[0]
        self.form = product_component_form(request)
        self.action = edit_good_details

    def get_data(self):
        if self.data.get("is_component") and self.data.get("component_details"):
            detail_field = COMPONENT_SELECTION_TO_DETAIL_FIELD_MAP[self.data["is_component"]]
            self.data[detail_field] = self.data["component_details"]
            return {"is_component": self.data.get("is_component"), detail_field: self.data.get(detail_field)}
        return {"is_component": self.data.get("is_component")}

    def get_success_url(self):
        if self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        elif self.application_id and self.object_pk:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_pk)
        elif self.object_pk:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class GoodInformationSecurity(LoginRequiredMixin, SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        self.data = get_good_details(request, self.object_pk)[0]
        self.form = product_uses_information_security(request)
        self.action = edit_good_details

    def get_data(self):
        new_data = {
            "uses_information_security": self.data.get("uses_information_security"),
            "information_security_details": self.data.get("information_security_details"),
        }
        return new_data

    def get_success_url(self):
        if self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        elif self.application_id and self.object_pk:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_pk)
        elif self.object_pk:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class RaiseGoodsQuery(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        good, _ = get_good(request, self.object_pk)

        raise_a_clc_query = good["is_good_controlled"] is None
        raise_a_pv_query = "grading_required" == good["is_pv_graded"]["key"]

        self.form = raise_a_goods_query(self.object_pk, raise_a_clc_query, raise_a_pv_query)
        self.action = raise_goods_query

        if self.draft_pk:
            self.success_url = reverse_lazy(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        else:
            self.success_url = reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


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

        raise_a_clc_query = good["is_good_controlled"] is None
        raise_a_pv_query = "grading_required" == good["is_pv_graded"]["key"]

        if self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        elif not good.get("documents") and not good.get("missing_document_reason"):
            return reverse_lazy("goods:add_document", kwargs={"pk": self.object_pk})
        elif raise_a_clc_query or raise_a_pv_query:
            return reverse_lazy("goods:raise_goods_query", kwargs={"pk": self.object_pk})
        else:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class EditFirearmProductType(LoginRequiredMixin, SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        self.data = get_good_details(request, self.object_pk)[0]["firearm_details"]
        self.form = group_two_product_type_form()
        self.action = edit_good_firearm_details

    def get_success_url(self):
        firearm_type = self.request.POST.get("type")
        if firearm_type:
            capture_sporting_shotgun = firearm_type in FIREARM_AMMUNITION_COMPONENT_TYPES
            if "good_pk" in self.kwargs:
                url = "applications:sporting-shotgun" if capture_sporting_shotgun else "applications:edit_good"
                return reverse_lazy(url, kwargs={"pk": self.application_id, "good_pk": self.object_pk})
            else:
                url = "goods:sporting-shotgun" if capture_sporting_shotgun else "goods:edit"
                return reverse_lazy(url, kwargs={"pk": self.object_pk})
        elif self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        # Edit
        else:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_pk)


class EditFirearmSportingShotgunStatus(LoginRequiredMixin, SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        self.data = get_good_details(request, self.object_pk)[0]["firearm_details"]
        self.form = firearms_sporting_shotgun_form(self.data["type"]["key"])
        self.action = edit_good_firearm_details

    def get_success_url(self):
        if self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        # coming from product summary screen when adding a new product to an application
        elif self.application_id and self.object_pk:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_pk)
        elif self.object_pk:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class EditYearOfManufacture(LoginRequiredMixin, SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        self.data = get_good_details(request, self.object_pk)[0]["firearm_details"]
        self.form = firearm_year_of_manufacture_details_form()
        self.action = edit_good_firearm_details

    def get_success_url(self):
        if self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        elif self.application_id and self.object_pk:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_pk)
        elif self.object_pk:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class EditFirearmReplica(LoginRequiredMixin, SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        self.data = get_good_details(request, self.object_pk)[0]["firearm_details"]
        self.form = firearm_replica_form(self.data["type"]["key"])
        self.action = edit_good_firearm_details

    def get_success_url(self):
        if self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        elif self.application_id and self.object_pk:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_pk)
        elif self.object_pk:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class EditCalibre(LoginRequiredMixin, SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        self.data = get_good_details(request, self.object_pk)[0]["firearm_details"]
        self.form = firearm_calibre_details_form()
        self.action = edit_good_firearm_details

    def get_success_url(self):
        if self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        elif self.application_id and self.object_pk:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_pk)
        elif self.object_pk:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class EditFirearmActDetails(LoginRequiredMixin, SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        self.data = get_good_details(request, self.object_pk)[0]["firearm_details"]
        self.form = firearms_act_confirmation_form()
        self.action = edit_good_firearm_details

    def get_data(self):
        if self.data:
            return {
                "is_covered_by_firearm_act_section_one_two_or_five": self.data.get(
                    "is_covered_by_firearm_act_section_one_two_or_five"
                ),
                "firearms_act_section": self.data.get("firearms_act_section"),
            }

    def get_success_url(self):
        updated_data = self.get_validated_data()["good"]["firearm_details"]
        covered_by_firearms_act = updated_data.get("is_covered_by_firearm_act_section_one_two_or_five") == "Yes"
        section_selected = updated_data.get("firearms_act_section")
        show_upload_form = covered_by_firearms_act and section_selected

        if self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        elif self.application_id and self.object_pk:
            # If the new status is that the product is not covered by firearms act or section change
            # then delete the previous certificate
            if is_firearms_act_status_changed(self.data, updated_data):
                fetch_and_delete_previous_application_documents(self.request, self.application_id, self.object_pk)

            if show_upload_form:
                return reverse(
                    "applications:firearms_act_certificate",
                    kwargs={"pk": self.application_id, "good_pk": self.object_pk},
                )
            else:
                return return_to_good_summary(self.kwargs, self.application_id, self.object_pk)
        elif self.object_pk:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


@method_decorator(csrf_exempt, "dispatch")
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
        if self.data["firearms_act_section"] == "firearms_act_section1":
            self.selected_section = "Section 1"
        elif self.data["firearms_act_section"] == "firearms_act_section2":
            self.selected_section = "Section 2"

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

    @csrf_exempt
    def post(self, request, **kwargs):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))
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


class EditIdentificationMarkings(LoginRequiredMixin, SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.draft_pk = str(kwargs.get("draft_pk", ""))
        self.data = get_good_details(request, self.object_pk)[0]["firearm_details"]
        self.form = identification_markings_form()
        self.action = edit_good_firearm_details

    def get_success_url(self):
        if self.draft_pk:
            return reverse(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        elif self.application_id and self.object_pk:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_pk)
        elif self.object_pk:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class DeleteGood(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        data, _ = get_good(request, str(kwargs["pk"]))
        return form_page(request, delete_good_form(data))

    def post(self, request, **kwargs):
        delete_good(request, str(kwargs["pk"]))
        return redirect(reverse_lazy("goods:goods"))


class CheckDocumentGrading(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.draft_pk = kwargs.get("draft_pk")
        back_url = reverse_lazy("goods:good", kwargs={"pk": self.object_pk})
        if self.draft_pk:
            back_url = reverse_lazy(
                "goods:good_detail_application",
                kwargs={"pk": self.object_pk, "type": "application", "draft_pk": self.draft_pk},
            )
        self.form = document_grading_form(request, self.object_pk, back_url)
        self.action = post_good_document_sensitivity

    def get_success_url(self):
        kwargs = {"pk": self.object_pk}
        if self.draft_pk:
            kwargs["draft_pk"] = self.draft_pk

        if self.request.POST.get("has_document_to_upload") == "no":
            good = self.get_validated_data()["good"]
            raise_a_clc_query = good["is_good_controlled"] is None
            raise_a_pv_query = "grading_required" == good["is_pv_graded"]["key"]

            if self.draft_pk:
                if not (raise_a_clc_query or raise_a_pv_query):
                    kwargs["type"] = "application"
                    url = "goods:good_detail_application"
                else:
                    url = "goods:raise_goods_query_add_application"
            else:
                if not (raise_a_clc_query or raise_a_pv_query):
                    url = "goods:good"
                else:
                    url = "goods:raise_goods_query"
        else:
            if self.draft_pk:
                url = "goods:attach_documents_add_application"
            else:
                url = "goods:attach_documents"

        return reverse_lazy(url, kwargs=kwargs)


@method_decorator(csrf_exempt, "dispatch")
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
                    AttachDocumentForm.BACK_FORM_LINK, reverse("goods:add_document", kwargs={"pk": good_id})
                )
        form = attach_documents_form(back_link)
        return form_page(request, form, extra_data=extra_data)

    @csrf_exempt
    def post(self, request, **kwargs):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        good_id = str(kwargs["pk"])
        draft_pk = str(kwargs.get("draft_pk", ""))
        good, _ = get_good(request, good_id)

        data, error = add_document_data(request)

        if error:
            return error_page(request, error)

        data, status_code = post_good_documents(request, good_id, data)
        if status_code != HTTPStatus.CREATED:
            return error_page(request, data["errors"]["file"])

        raise_a_clc_query = good["is_good_controlled"] is None
        raise_a_pv_query = "grading_required" == good["is_pv_graded"]["key"]

        if draft_pk:
            if not (raise_a_clc_query or raise_a_pv_query):
                return redirect(
                    reverse(
                        "goods:good_detail_application",
                        kwargs={"pk": good_id, "type": "application", "draft_pk": draft_pk},
                    )
                )
            else:
                return redirect(
                    reverse("goods:raise_goods_query_add_application", kwargs={"pk": good_id, "draft_pk": draft_pk})
                )
        else:
            if not (raise_a_clc_query or raise_a_pv_query):
                return redirect(reverse("goods:good", kwargs={"pk": good_id}))
            else:
                return redirect(reverse("goods:raise_goods_query", kwargs={"pk": good_id}))


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
