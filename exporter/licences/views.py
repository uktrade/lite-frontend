from http import HTTPStatus

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from exporter.core.objects import Tab
from exporter.core.services import get_open_general_licences, get_control_list_entries, get_countries
from exporter.licences import filters
from exporter.licences.helpers import (
    get_potential_ogl_control_list_entries,
    get_potential_ogl_countries,
    get_potential_ogl_sites,
)
from exporter.licences.services import get_licences, get_licence, get_nlr_letters
from lite_content.lite_exporter_frontend.licences import LicencesList, LicencePage

from lite_forms.generators import error_page

from core.auth.views import LoginRequiredMixin


tabs = [
    Tab(id="licences", name=LicencesList.Tabs.LICENCE, url=reverse_lazy("licences:list-open-and-standard-licences")),
    Tab(
        id="open_general_licences",
        name=LicencesList.Tabs.OGLS,
        url=reverse_lazy("licences:list-open-general-licences"),
    ),
    Tab(
        id="no_licence_required",
        name=LicencesList.Tabs.NLR,
        url=reverse_lazy("licences:list-no-licence-required"),
    ),
    Tab(
        id="clearances",
        name=LicencesList.Tabs.CLEARANCE,
        url=reverse_lazy("licences:list-clearances"),
    ),
]


class AbstractListView(LoginRequiredMixin, TemplateView):
    @property
    def params(self):
        params = self.request.GET.copy()
        params.pop("licence_type", None)
        return params

    def get(self, *args, **kwargs):
        self.page = int(self.request.GET.get("page", 1))
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            selected_tab=self.object_name,
            reference=self.request.GET.get("reference", ""),
            name=self.request.GET.get("name", ""),
            row_limit=3,
            tabs=tabs,
            FEATURE_FLAG_ONLY_ALLOW_SIEL=settings.FEATURE_FLAG_ONLY_ALLOW_SIEL,
            **kwargs,
        )

    @property
    def control_list(self):
        return get_control_list_entries(self.request, convert_to_options=True)

    @property
    def countries(self):
        return get_countries(self.request, convert_to_options=True)


class ListOpenAndStandardLicences(AbstractListView):
    template_name = "licences/licences.html"
    object_name = "licences"

    def get_context_data(self, **kwargs):
        filter_bar = filters.get_licences_filters(
            licence_type=self.object_name, control_list_entries=self.control_list, countries=self.countries
        )
        licences = get_licences(self.request, licence_type="licence")
        return super().get_context_data(data=licences, filters=filter_bar, **kwargs)


class ListClearances(AbstractListView):
    template_name = "licences/clearances.html"
    object_name = "clearances"

    def get_context_data(self, **kwargs):
        filter_bar = filters.get_licences_filters(
            licence_type=self.object_name, control_list_entries=self.control_list, countries=self.countries
        )
        clearances = get_licences(self.request, licence_type="clearance", **self.params)
        return super().get_context_data(data=clearances, filters=filter_bar, **kwargs)


class ListNoLicenceRequired(AbstractListView):
    template_name = "licences/nlrs.html"
    object_name = "no_licence_required"

    def get_context_data(self, **kwargs):
        letters = get_nlr_letters(self.request, **self.params)
        filter_bar = filters.get_no_licence_required_filters(
            licence_type=self.object_name, control_list_entries=self.control_list, countries=self.countries
        )
        return super().get_context_data(data=letters, filters=filter_bar, **kwargs)


class ListOpenGeneralLicences(AbstractListView):
    template_name = "licences/open-general-licences.html"
    object_name = "open_general_licences"

    def get_context_data(self, **kwargs):
        licences = get_open_general_licences(self.request, registered=True, **self.params)
        filter_bar = filters.get_open_general_licences_filters(
            licence_type=self.object_name,
            control_list_entries=get_potential_ogl_control_list_entries(licences),
            countries=get_potential_ogl_countries(licences),
            sites=get_potential_ogl_sites(licences),
        )
        return super().get_context_data(data=licences, filters=filter_bar, **kwargs)


class Licence(LoginRequiredMixin, TemplateView):
    def get(self, request, pk):
        licence, status_code = get_licence(request, pk)
        if status_code == HTTPStatus.NOT_FOUND:
            return Http404
        elif status_code != HTTPStatus.OK:
            return error_page(request, LicencePage.ERROR)
        return render(request, "licences/licence.html", {"licence": licence})
