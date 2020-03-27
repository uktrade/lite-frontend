from json import JSONDecodeError

from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from auth.services import authenticate_exporter_user
from conf.constants import Permissions, NotificationType, NEWLINE
from core.forms import (
    select_your_organisation_form,
    register_a_commercial_organisation_group,
    register_triage,
    register_an_individual_group,
)
from core.helpers import Section, Tile, generate_notification_string
from core.services import (
    get_notifications,
    get_organisation,
    get_country,
    register_commercial_organisation,
    register_private_individual,
)
from core.validators import validate_register_organisation_triage
from lite_content.lite_exporter_frontend import strings, generic
from lite_forms.components import BackLink
from lite_forms.generators import form_page, success_page
from lite_forms.helpers import conditional
from lite_forms.views import SummaryListFormView, MultiFormView
from organisation.members.services import get_user


class Home(TemplateView):
    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return render(request, "core/start.html")

        try:
            user = get_user(request)
            user_permissions = user["role"]["permissions"]
        except (JSONDecodeError, TypeError, KeyError):
            return redirect("auth:login")

        if Permissions.ADMINISTER_USERS in user_permissions:
            manage_organisation_section_link = reverse_lazy("organisation:organisation")
            title = strings.core.HubPage.ORGANISATION
        else:
            manage_organisation_section_link = None

        organisation = get_organisation(request, str(request.user.organisation))
        notifications, _ = get_notifications(request)

        if organisation.get("type").get("key") == "hmrc":
            sections = [
                Section("", [Tile(strings.hub.Tiles.CUSTOMS_ENQUIRY, "", reverse_lazy("hmrc:raise_a_query")),]),
                Section(
                    strings.hub.Header.MANAGE,
                    [
                        Tile(strings.hub.Tiles.APPLICATIONS, "", reverse_lazy("applications:applications"),),
                        Tile(
                            strings.hub.Tiles.DRAFTS,
                            "",
                            reverse_lazy("applications:applications") + "?submitted=False",
                        ),
                    ],
                ),
            ]
        else:
            sections = [
                Section(
                    "", [Tile(strings.hub.Tiles.APPLY_FOR_LICENCE, "", reverse_lazy("apply_for_a_licence:start"))],
                ),
                Section(
                    strings.hub.Header.MANAGE,
                    [
                        Tile(
                            strings.hub.Tiles.APPLICATIONS,
                            generate_notification_string(notifications, case_types=[NotificationType.APPLICATION]),
                            reverse_lazy("applications:applications"),
                        ),
                        Tile(
                            strings.hub.Tiles.GOODS,
                            generate_notification_string(notifications, case_types=[NotificationType.GOODS]),
                            reverse_lazy("goods:goods"),
                        ),
                        Tile(
                            strings.hub.Tiles.END_USER_ADVISORIES,
                            generate_notification_string(notifications, case_types=[NotificationType.EUA]),
                            reverse_lazy("end_users:end_users"),
                        ),
                    ],
                ),
            ]

            if organisation.get("type").get("key") == "individual":
                sections[1].tiles.append(Tile(strings.hub.Tiles.SITES, "", reverse_lazy("organisation:sites:sites")))
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
        organisation = get_organisation(request, request.POST["organisation"])

        if "errors" in organisation:
            return redirect(reverse_lazy("core:register_an_organisation_confirm") + "?show_back_link=True")

        request.user.organisation_name = organisation["name"]
        request.user.save()

        return redirect("/")


class RegisterAnOrganisationTriage(MultiFormView):
    class Locations:
        UNITED_KINGDOM = "united_kingdom"
        ABROAD = "abroad"

    def init(self, request, **kwargs):
        self.forms = register_triage()
        self.action = validate_register_organisation_triage
        self.additional_context = {"user_in_limbo": True}

        try:
            organisation = get_user(request)["organisations"][0]
            if organisation:
                raise Http404
        except JSONDecodeError:
            pass

        if not request.user.is_authenticated:
            raise Http404

    def get_success_url(self):
        return reverse(
            "core:register_an_organisation",
            kwargs={"type": self.get_validated_data()["type"], "location": self.get_validated_data()["location"]},
        )


class RegisterAnOrganisation(SummaryListFormView):
    def init(self, request, **kwargs):
        _type = self.kwargs["type"]
        location = self.kwargs["location"]

        self.forms = (
            register_a_commercial_organisation_group(location)
            if _type == "commercial"
            else register_an_individual_group(location)
        )
        self.action = register_commercial_organisation if _type == "commercial" else register_private_individual
        self.hide_components = ["site.address.address_line_2"]
        self.additional_context = {"user_in_limbo": True}

        try:
            organisation = get_user(request)["organisations"][0]
            if organisation:
                raise Http404
        except JSONDecodeError:
            pass

        if not request.user.is_authenticated:
            raise Http404

    def prettify_data(self, data):
        if "site.address.country" in data and data["site.address.country"]:
            data["site.address.country"] = get_country(self.request, data["site.address.country"])["name"]
        if "site.foreign_address.country" in data and data["site.foreign_address.country"]:
            data["site.foreign_address.country"] = get_country(self.request, data["site.foreign_address.country"])[
                "name"
            ]
        if "site.address.address_line_2" in data and data["site.address.address_line_2"]:
            data["site.address.address_line_1"] = (
                data["site.address.address_line_1"] + NEWLINE + data["site.address.address_line_2"]
            )
        return data

    def get_success_url(self):
        # Update the signed in user's details so they can make validated API calls
        response, _ = authenticate_exporter_user(
            {
                "email": self.request.user.email,
                "user_profile": {"first_name": self.request.user.first_name, "last_name": self.request.user.last_name},
            }
        )
        self.request.user.user_token = response["token"]
        self.request.user.lite_api_user_id = response["lite_api_user_id"]
        self.request.user.save()
        return reverse("core:register_an_organisation_confirm") + "?animate=True"


class RegisterAnOrganisationConfirmation(TemplateView):
    def get(self, request, *args, **kwargs):
        organisation = get_user(request)["organisations"][0]
        organisation_name = organisation["name"]
        organisation_status = organisation["status"]["key"]

        if organisation_status != "in_review":
            raise Http404

        return success_page(
            request=request,
            title=f"You've successfully registered: {organisation_name}",
            secondary_title="We're currently processing your application.",
            description="",
            what_happens_next=[
                "Export Control Joint Unit (ECJU) is processing your request for an export control account. "
                "We'll send you an email when we've made a final decision."
            ],
            links={},
            back_link=conditional(
                request.GET.get("show_back_link", False), BackLink(generic.BACK, reverse_lazy("core:pick_organisation"))
            ),
            animated=True,
            additional_context={"user_in_limbo": True},
        )
