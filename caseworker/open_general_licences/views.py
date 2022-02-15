import copy

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from core.builtins.custom_tags import friendly_boolean
from caseworker.core.helpers import generate_activity_filters
from caseworker.core.services import get_countries, get_control_list_entries
from lite_content.lite_internal_frontend import open_general_licences as open_general_licences_strings, generic
from lite_forms.components import FiltersBar, Select, TextInput, AutocompleteInput, BackLink, HiddenField
from lite_forms.generators import confirm_form
from lite_forms.views import SummaryListFormView, SingleFormView
from caseworker.open_general_licences import constants
from caseworker.open_general_licences.enums import OpenGeneralExportLicences
from caseworker.open_general_licences.forms import open_general_licence_forms
from caseworker.open_general_licences.services import (
    get_open_general_licences,
    post_open_general_licences,
    get_open_general_licence,
    patch_open_general_licence,
    set_open_general_licence_status,
    get_ogl_activity,
)

from core.auth.views import LoginRequiredMixin


class ListView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        open_general_licences = get_open_general_licences(request, **request.GET)
        control_list_entries = get_control_list_entries(request, True)
        countries = get_countries(request, True)

        filters = FiltersBar(
            [
                HiddenField("status", request.GET.get("status", "active")),
                TextInput(name="name", title="name"),
                Select(name="case_type", title="type", options=OpenGeneralExportLicences.as_options()),
                AutocompleteInput(name="control_list_entry", title="control list entry", options=control_list_entries),
                AutocompleteInput(name="country", title="country", options=countries),
            ]
        )

        context = {
            "filters": filters,
            "tab": request.GET.get("status", "active"),
            "open_general_licences": open_general_licences,
        }
        return render(request, "open-general-licences/index.html", context)


class DetailView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        activity_and_filters = get_ogl_activity(request, kwargs["pk"], activity_filters=request.GET)
        context = {
            "open_general_licence": get_open_general_licence(request, kwargs["pk"]),
            "activity": activity_and_filters["activity"],
            "filters": generate_activity_filters(activity_and_filters["filters"], open_general_licences_strings.Detail),
            "DETAILS": constants.DETAILS,
            "CONTROL_LIST_ENTRIES": constants.CONTROL_LIST_ENTRIES,
            "COUNTRIES": constants.COUNTRIES,
        }
        return render(request, "open-general-licences/open-general-licence.html", context)


class CreateView(LoginRequiredMixin, SummaryListFormView):
    def init(self, request, **kwargs):
        licence = OpenGeneralExportLicences.get_by_id(
            request.POST.get("case_type", OpenGeneralExportLicences.open_general_export_licence.id)
        )
        self.forms = open_general_licence_forms(
            request,
            licence,
            open_general_licences_strings.Create,
        )
        self.action = post_open_general_licences
        self.summary_list_title = open_general_licences_strings.Create.SUMMARY_TITLE + licence.name
        self.summary_list_button = open_general_licences_strings.Create.SUBMIT_BUTTON
        self.summary_list_notice_title = None
        self.summary_list_notice_text = None
        self.hide_titles = True
        self.hide_components = ["case_type"]
        self.success_message = open_general_licences_strings.Create.SUCCESS_MESSAGE
        self.success_url = reverse("open_general_licences:open_general_licences")

    def prettify_data(self, data):
        countries, _ = get_countries(self.request)
        countries = [
            country["name"] for country in countries["countries"] if country["id"] in data.get("countries", [])
        ]

        data["registration_required"] = friendly_boolean(data["registration_required"])
        data["control_list_entries[]"] = ", ".join(data.get("control_list_entries", []))
        data["countries[]"] = ", ".join(countries)
        return data


class UpdateView(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.object = get_open_general_licence(request, self.object_pk)
        self.data = self.object
        self.action = patch_open_general_licence
        self.success_message = open_general_licences_strings.Edit.SUCCESS_MESSAGE
        self.success_url = reverse("open_general_licences:open_general_licence", kwargs={"pk": self.object_pk})

    def get_form(self):
        forms = open_general_licence_forms(
            self.request,
            OpenGeneralExportLicences.get_by_id(self.object["case_type"]["id"]),
            open_general_licences_strings.Edit,
        ).forms

        if self.kwargs["edit"] == constants.DETAILS:
            form = forms[1]
        elif self.kwargs["edit"] == constants.CONTROL_LIST_ENTRIES:
            form = forms[2]
        elif self.kwargs["edit"] == constants.COUNTRIES:
            form = forms[3]
        else:
            raise Http404

        form = copy.deepcopy(form)
        form.caption = self.object["case_type"]["reference"]["value"] + " (" + self.object["name"] + ")"
        form.buttons[0].value = generic.SAVE_AND_RETURN
        form.back_link = BackLink(
            url=reverse("open_general_licences:open_general_licence", kwargs={"pk": self.kwargs["pk"]})
        )
        return form


class ChangeStatusView(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.object = get_open_general_licence(request, self.object_pk)
        self.action = set_open_general_licence_status
        self.success_url = reverse("open_general_licences:open_general_licence", kwargs={"pk": self.object_pk})
        self.strings = (
            open_general_licences_strings.Reactivate
            if self.kwargs["status"] == "reactivate"
            else open_general_licences_strings.Deactivate
        )
        if request.POST.get("response") == "yes":
            self.success_message = self.strings.SUCCESS_MESSAGE

    def get_form(self):
        return confirm_form(
            title=self.strings.TITLE.format(self.object["name"]),
            description=self.strings.DESCRIPTION,
            back_link_text=self.strings.BACK_LINK.format(self.object["name"]),
            back_url=self.success_url,
            yes_label=self.strings.YES,
            no_label=self.strings.NO,
            side_by_side=True,
            submit_button_text=self.strings.SUBMIT_BUTTON,
            confirmation_name="response",
        )

    def on_submission(self, request, **kwargs):
        if kwargs["status"] == "reactivate":
            if request.POST.get("response") == "yes":
                return {"status": "active"}
            elif request.POST.get("response") == "no":
                return {"status": "deactivated"}
        elif kwargs["status"] == "deactivate":
            if request.POST.get("response") == "yes":
                return {"status": "deactivated"}
            elif request.POST.get("response") == "no":
                return {"status": "active"}
        return {}
