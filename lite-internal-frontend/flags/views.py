from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from cases.forms.flags import flags_form, set_case_flags_form
from cases.services import put_flag_assignments, get_good, get_goods_type, get_case, get_destination
from conf.constants import FlagLevels
from core.helpers import convert_dict_to_query_params
from flags.forms import add_flag_form, edit_flag_form
from flags.services import get_cases_flags, get_goods_flags, get_organisation_flags, get_destination_flags
from flags.services import get_flags, post_flags, get_flag, put_flag
from lite_content.lite_internal_frontend import strings
from lite_forms.components import Option
from lite_forms.generators import form_page
from organisations.services import get_organisation
from users.services import get_gov_user


class FlagsList(TemplateView):
    def get(self, request, **kwargs):
        data, _ = get_flags(request)
        user_data, _ = get_gov_user(request, str(request.user.lite_api_user_id))

        status = kwargs.get("status", "active")

        if status == "active":
            status = "no_deactivated"
            flags = []
            for flag in data["flags"]:
                if flag["status"] == "Deactivated":
                    status = "active"
                if flag["status"] == "Active":
                    flags.append(flag)
            data["flags"] = flags

        context = {
            "data": data,
            "status": status,
            "title": "Flags",
            "user_data": user_data,
        }
        return render(request, "flags/index.html", context)


class AddFlag(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, add_flag_form())

    def post(self, request, **kwargs):
        response, status_code = post_flags(request, request.POST)
        if status_code != 201:
            return form_page(request, add_flag_form(), data=request.POST, errors=response.get("errors"))

        return redirect(reverse_lazy("flags:flags"))


class EditFlag(TemplateView):
    def get(self, request, **kwargs):
        data, _ = get_flag(request, str(kwargs["pk"]))
        return form_page(request, edit_flag_form(), data=data["flag"])

    def post(self, request, **kwargs):
        response, status_code = put_flag(request, str(kwargs["pk"]), request.POST)
        if status_code != 200:
            return form_page(request, edit_flag_form(), data=request.POST, errors=response.get("errors"))

        return redirect(reverse_lazy("flags:flags"))


class ViewFlag(TemplateView):
    def get(self, request, **kwargs):
        data, _ = get_flag(request, str(kwargs["pk"]))

        context = {"data": data, "title": data["flag"]["name"]}
        return render(request, "flags/profile.html", context)


class ChangeFlagStatus(TemplateView):
    def get(self, request, **kwargs):
        status = kwargs["status"]
        description = ""

        if status != "deactivate" and status != "reactivate":
            raise Http404

        if status == "deactivate":
            description = strings.Flags.UpdateFlag.Status.DEACTIVATE_WARNING

        if status == "reactivate":
            description = strings.Flags.UpdateFlag.Status.REACTIVATE_WARNING

        context = {
            "title": "Are you sure you want to {} this flag?".format(status),
            "description": description,
            "user_id": str(kwargs["pk"]),
            "status": status,
        }
        return render(request, "flags/change_status.html", context)

    def post(self, request, **kwargs):
        status = kwargs["status"]

        if status != "deactivate" and status != "reactivate":
            raise Http404

        put_flag(request, str(kwargs["pk"]), json={"status": request.POST["status"]})

        return redirect(reverse_lazy("flags:flags"))


class AssignFlags(TemplateView):
    objects = None
    form = None
    selected_flags = None
    url = None
    level = None

    def dispatch(self, request, *args, **kwargs):
        self.objects = request.GET.getlist("items", request.GET.getlist("goods"))

        if not self.objects:
            raise Http404

        self.level = request.GET.get("level")

        kwargs = {"pk": self.objects[0]} if self.level == "organisations" else {"pk": str(kwargs["pk"])}
        origin = request.GET.get("origin", "case")

        if origin == "good":
            kwargs["good_pk"] = self.objects[0]

        # Retrieve the list of flags depending on type
        if self.level == FlagLevels.CASES:
            flags = get_cases_flags(request)
        elif self.level == FlagLevels.GOODS:
            flags = get_goods_flags(request)
        elif self.level == FlagLevels.ORGANISATIONS:
            flags = get_organisation_flags(request)
            origin = "organisation"
        elif self.level == FlagLevels.DESTINATIONS:
            flags = get_destination_flags(request)

        self.url = (
            reverse("organisations:organisation", kwargs=kwargs)
            if self.level == "organisations"
            else reverse("cases:" + origin, kwargs=kwargs)
        )

        # Perform pre-population of the flags if there is only one object to be flagged
        if len(self.objects) == 1:
            self._single_item_processing(request, flags)

        if origin == "review_goods":
            origin = "review good"
            parameters = {"goods": self.objects}
            objects_url_suffix = "?" + convert_dict_to_query_params(parameters)

            self.url += objects_url_suffix

        flags = [Option(flag["id"], flag["name"]) for flag in flags]

        self.form = flags_form(flags=flags, level=self.level, origin=origin, url=self.url)

        if self.level == FlagLevels.CASES:
            case = get_case(request, kwargs["pk"])
            self.form = set_case_flags_form(flags, case)

        return super(AssignFlags, self).dispatch(request, *args, **kwargs)

    def _single_item_processing(self, request, flags):
        object_flags = None
        if self.level == FlagLevels.GOODS:
            obj, status_code = get_good(request, self.objects[0])
            if status_code == 404:
                obj, _ = get_goods_type(request, self.objects[0])
        elif self.level == FlagLevels.CASES:
            obj = {"case": get_case(request, self.objects[0])}
        elif self.level == FlagLevels.ORGANISATIONS:
            obj, _ = get_organisation(request, self.objects[0])
            object_flags = obj.get("flags")
        elif self.level == FlagLevels.DESTINATIONS:
            obj = get_destination(request, self.objects[0])

        # Fetches existing flags on the object
        if self.level != "organisations":
            object_flags = obj.get(self.level[:-1]).get("flags")

        flags_list = []
        for flag in flags:
            for object_flag in object_flags:

                # If flag is both on the object and available to the user, show that it is already set
                if flag["id"] in object_flag["id"]:
                    flags_list.append(flag["id"])
                    break

        self.selected_flags = {"flags": flags_list}

    def get(self, request, **kwargs):
        return form_page(request, self.form, data=self.selected_flags)

    def post(self, request, **kwargs):
        data = {
            "level": self.level,
            "objects": self.objects,
            "flags": request.POST.getlist("flags"),
            "note": request.POST.get("note"),
        }

        response, _ = put_flag_assignments(request, data)

        if "errors" in response:
            return form_page(request, self.form, data=request.POST, errors=response["errors"])

        return redirect(self.url)
