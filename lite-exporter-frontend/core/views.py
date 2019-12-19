from json import JSONDecodeError

from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from conf.constants import Permissions
from core.builtins.custom_tags import get_string
from core.forms import select_your_organisation_form
from core.helpers import Section, Tile, generate_notification_string
from core.services import get_notifications, get_organisation
from lite_content.lite_exporter_frontend import strings
from lite_forms.generators import form_page
from users.services import get_user


class Hub(TemplateView):
    def get(self, request, **kwargs):
        try:
            user = get_user(request)
            user_permissions = user["role"]["permissions"]
        except (JSONDecodeError, TypeError):
            return redirect("auth:login")

        if Permissions.ADMINISTER_USERS in user_permissions:
            manage_organisation_section_link = reverse_lazy("users:users")
            title = strings.core.HubPage.USERS
        elif Permissions.ADMINISTER_SITES in user_permissions:
            manage_organisation_section_link = reverse_lazy("sites:sites")
            title = strings.core.HubPage.SITES
        elif Permissions.EXPORTER_ADMINISTER_ROLES in user_permissions:
            manage_organisation_section_link = reverse_lazy("roles:roles")
            title = strings.core.HubPage.ROLES
        else:
            manage_organisation_section_link = None

        notifications = get_notifications(request, unviewed=True)
        organisation = get_organisation(request, str(request.user.organisation))

        if organisation.get("type").get("key") == "hmrc":
            sections = [
                Section("", [Tile("Make a Customs enquiry", "", reverse_lazy("hmrc:raise_a_query")),]),
                Section(
                    "Manage",
                    [
                        Tile(get_string("applications.title"), "", reverse_lazy("applications:applications")),
                        Tile(
                            get_string("drafts.title"),
                            "",
                            reverse_lazy("applications:applications") + "?submitted=False",
                        ),
                    ],
                ),
            ]
        else:
            sections = [
                Section(
                    "",
                    [Tile(get_string("licences.apply_for_a_licence"), "", reverse_lazy("apply_for_a_licence:start")),],
                ),
                Section(
                    "Manage",
                    [
                        Tile(
                            get_string("applications.title"),
                            generate_notification_string(notifications, "base_application"),
                            reverse_lazy("applications:applications"),
                        ),
                        Tile(
                            "Goods",
                            generate_notification_string(notifications, "control_list_classification_query"),
                            reverse_lazy("goods:goods"),
                        ),
                        Tile(
                            "End User Advisories",
                            generate_notification_string(notifications, "end_user_advisory_query"),
                            reverse_lazy("end_users:end_users"),
                        ),
                    ],
                ),
            ]

            if organisation.get("type").get("key") == "individual":
                sections[1].tiles.append(Tile("Manage my sites", "", reverse_lazy("sites:sites")))
            elif manage_organisation_section_link:
                number_permissions = 0
                for permission in user_permissions:
                    if permission in Permissions.MANAGE_ORGANISATION_PERMISSIONS:
                        number_permissions += 1
                if number_permissions > 1:
                    title = strings.core.HubPage.ORGANISATION
                sections[1].tiles.append(Tile(title, "", manage_organisation_section_link))

        context = {
            "organisation": organisation,
            "sections": sections,
            "application_deleted": request.GET.get("application_deleted"),
            "user_data": user,
            "notifications": notifications,
        }

        return render(request, "core/hub.html", context)


class PickOrganisation(TemplateView):
    form = None
    organisations = None

    def dispatch(self, request, *args, **kwargs):
        user = get_user(request)
        self.organisations = user["organisations"]
        self.form = select_your_organisation_form(self.organisations)

        if len(self.organisations) == 1:
            raise Http404()

        return super(PickOrganisation, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        data = {"organisation": str(request.user.organisation)}
        return form_page(request, self.form, data=data, extra_data={"user_in_limbo": data["organisation"] == "None"})

    def post(self, request, **kwargs):
        # If no data is given, error
        if not request.POST.get("organisation"):
            return form_page(request, self.form, errors={"organisation": ["Select an organisation to use"]})

        request.user.organisation = request.POST["organisation"]
        organisation = get_organisation(request, request.user.organisation)
        request.user.organisation_name = organisation["name"]
        request.user.save()

        return redirect("/")
