from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView

from conf.constants import Permissions
from core.objects import Tab
from core.services import get_organisation
from lite_content.lite_exporter_frontend.organisation import Tabs
from lite_forms.helpers import conditional
from organisation.roles.services import get_user_permissions


class OrganisationView(TemplateView):
    organisation_id = None
    organisation = None
    additional_context = {}

    def get_additional_context(self):
        return self.additional_context

    def get(self, request, **kwargs):
        self.organisation_id = str(request.user.organisation)
        self.organisation = get_organisation(request, self.organisation_id)
        user_permissions = kwargs.get("permissions", get_user_permissions(request))
        can_administer_sites = Permissions.ADMINISTER_SITES in user_permissions
        can_administer_roles = Permissions.EXPORTER_ADMINISTER_ROLES in user_permissions

        context = {
            "organisation": self.organisation,
            "can_administer_sites": can_administer_sites,
            "can_administer_roles": can_administer_roles,
            "user_permissions": user_permissions,
            "tabs": [
                Tab("members", Tabs.MEMBERS, reverse_lazy("organisation:members:members")),
                conditional(can_administer_sites, Tab("sites", Tabs.SITES, reverse_lazy("organisation:sites:sites"))),
                conditional(can_administer_roles, Tab("roles", Tabs.ROLES, reverse_lazy("organisation:roles:roles"))),
                Tab("details", Tabs.DETAILS, reverse_lazy("organisation:details")),
            ],
        }
        context.update(self.get_additional_context())
        return render(request, f"organisation/{self.template_name}.html", context)


class RedirectToMembers(RedirectView):
    url = reverse_lazy("organisation:members:members")


class Details(OrganisationView):
    template_name = "details/index"
