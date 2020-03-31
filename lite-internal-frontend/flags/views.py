from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from cases.forms.flags import flags_form, set_case_flags_form
from cases.services import put_flag_assignments, get_good, get_goods_type, get_case, get_destination
from conf.constants import FlagLevels, Permission
from core.helpers import convert_dict_to_query_params, get_params_if_exist
from core.services import get_user_permissions
from flags.forms import (
    add_flag_form,
    edit_flag_form,
    create_flagging_rules_formGroup,
    select_condition_and_flag,
    _levels,
    deactivate_or_activate_flagging_rule_form,
)
from flags.services import (
    get_cases_flags,
    get_goods_flags,
    get_organisation_flags,
    get_destination_flags,
    get_flagging_rules,
    put_flagging_rule,
    get_flagging_rule,
    post_flagging_rules,
)
from flags.services import get_flags, post_flags, get_flag, put_flag
from lite_content.lite_internal_frontend import strings, flags
from lite_content.lite_internal_frontend.flags import UpdateFlag
from lite_forms.components import Option, FiltersBar, Select, Checkboxes
from lite_forms.generators import form_page
from lite_forms.views import MultiFormView, SingleFormView
from organisations.services import get_organisation
from queues.services import get_queue
from users.services import get_gov_user


class FlagsList(TemplateView):
    def get(self, request, **kwargs):
        data, _ = get_flags(request)
        user_data, _ = get_gov_user(request, str(request.user.lite_api_user_id))

        status = request.GET.get("status", "active")

        if status == "active":
            status = "no_deactivated"
            flags_data = []
            for flag in data["flags"]:
                if flag["status"] == "Deactivated":
                    status = "active"
                if flag["status"] == "Active":
                    flags_data.append(flag)
            data["flags"] = flags_data

        filters = FiltersBar(
            [
                Checkboxes(
                    name="status",
                    options=[Option("deactivated", flags.FlagsList.INCLUDE_DEACTIVATED)],
                    classes=["govuk-checkboxes--small"],
                ),
            ]
        )

        context = {
            "data": data,
            "status": status,
            "user_data": user_data,
            "filters": filters,
        }
        return render(request, "flags/index.html", context)


class AddFlag(SingleFormView):
    def init(self, request, **kwargs):
        self.form = add_flag_form()
        self.action = post_flags

    def get_success_url(self):
        messages.success(self.request, flags.FlagsList.SUCCESS_MESSAGE)
        return reverse("flags:flags")


class EditFlag(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        flag, _ = get_flag(request, self.object_pk)
        self.form = edit_flag_form()
        self.data = flag["flag"]
        self.action = put_flag
        self.success_url = reverse("flags:flags")


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
            description = UpdateFlag.Status.DEACTIVATE_WARNING

        if status == "reactivate":
            description = UpdateFlag.Status.REACTIVATE_WARNING

        context = {
            "title": "Are you sure you want to {} this flag?".format(status),
            "description": description,
            "user_id": str(kwargs["pk"]),
            "status": status,
        }
        return render(request, "flags/change-status.html", context)

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

        pks = {"pk": self.objects[0]} if self.level == "organisations" else {"pk": str(kwargs["pk"])}
        origin = request.GET.get("origin", "case")

        if origin == "good":
            pks["good_pk"] = self.objects[0]

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
            reverse("organisations:organisation", kwargs=pks)
            if self.level == "organisations"
            else reverse("cases:" + origin, kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"]})
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
            self.form = set_case_flags_form(get_queue(request, kwargs["queue_pk"]), flags, case)

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
            obj = get_organisation(request, self.objects[0])
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


class ManageFlagRules(TemplateView):
    def get(self, request, **kwargs):
        if Permission.MANAGE_FLAGGING_RULES.value not in get_user_permissions(request):
            return redirect(reverse_lazy("cases:cases"))

        params = {"page": int(request.GET.get("page", 1))}
        params = get_params_if_exist(request, ["only_my_team", "level", "include_deactivated"], params)

        data, _ = get_flagging_rules(request, convert_dict_to_query_params(params))

        filters = FiltersBar(
            [
                Select(name="level", title=strings.FlaggingRules.List.Filter.Type, options=_levels),
                Checkboxes(
                    name="only_my_team",
                    options=[Option("true", strings.FlaggingRules.List.Filter.MY_TEAM_ONLY)],
                    classes=["govuk-checkboxes--small", "govuk-!-margin-top-6"],
                ),
                Checkboxes(
                    name="include_deactivated",
                    options=[Option("true", strings.FlaggingRules.List.Filter.INCLUDE_DEACTIVATED)],
                    classes=["govuk-checkboxes--small", "govuk-!-margin-top-6"],
                ),
            ]
        )

        context = {
            "data": data,
            "page": params.pop("page"),
            "team": get_gov_user(request)[0]["user"]["team"]["id"],
            "filters": filters,
            "params_str": convert_dict_to_query_params(params),
        }
        return render(request, "flags/flagging-rules-list.html", context)


class CreateFlagRules(MultiFormView):
    def init(self, request, **kwargs):
        if Permission.MANAGE_FLAGGING_RULES.value not in get_user_permissions(request):
            return redirect(reverse_lazy("cases:cases"))

        type = request.POST.get("level", None)
        self.forms = create_flagging_rules_formGroup(request=self.request, type=type)
        self.action = post_flagging_rules
        self.success_url = reverse_lazy("flags:flagging_rules")


class EditFlaggingRules(SingleFormView):
    def init(self, request, **kwargs):
        if Permission.MANAGE_FLAGGING_RULES.value not in get_user_permissions(request):
            return redirect(reverse_lazy("cases:cases"))

        self.object_pk = kwargs["pk"]
        self.data = get_flagging_rule(request, self.object_pk)[0]["flag"]
        self.form = select_condition_and_flag(request, type=self.data["level"])
        self.action = put_flagging_rule
        self.success_url = reverse_lazy("flags:flagging_rules")


class ChangeFlaggingRuleStatus(SingleFormView):
    success_url = reverse_lazy("flags:flagging_rules")

    def init(self, request, **kwargs):
        if Permission.MANAGE_FLAGGING_RULES.value not in get_user_permissions(request):
            return redirect(reverse_lazy("cases:cases"))

        status = kwargs["status"]
        self.object_pk = kwargs["pk"]

        if status != "Deactivated" and status != "Active":
            raise Http404

        if status == "Deactivated":
            title = strings.FlaggingRules.Status.DEACTIVATE_HEADING
            description = strings.FlaggingRules.Status.DEACTIVATE_WARNING
            confirm_text = strings.FlaggingRules.Status.DEACTIVATE_CONFIRM

        if status == "Active":
            title = strings.FlaggingRules.Status.REACTIVATE_HEADING
            description = strings.FlaggingRules.Status.REACTIVATE_WARNING
            confirm_text = strings.FlaggingRules.Status.REACTIVATE_CONFIRM

        self.form = deactivate_or_activate_flagging_rule_form(
            title=title, description=description, confirm_text=confirm_text, status=status
        )
        self.action = put_flagging_rule

    def post(self, request, **kwargs):
        self.init(request, **kwargs)
        if not request.POST.get("confirm"):
            return form_page(
                request,
                self.get_form(),
                data=self.get_data(),
                errors={"confirm": [strings.FlaggingRules.Status.NO_SELECTION_ERROR]},
                extra_data=self.context,
            )
        elif request.POST.get("confirm") == "no":
            return redirect(self.success_url)

        return super(ChangeFlaggingRuleStatus, self).post(request, **kwargs)
