from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from core.builtins.custom_tags import str_date
from core.services import get_countries, get_denial_reasons
from flags.enums import FlagStatus
from flags.services import get_flags
from lite_content.lite_internal_frontend.picklists import (
    ReactivatePicklistItem,
    DeactivatePicklistItem,
    EditPicklistItemForm,
)
from lite_forms.components import FiltersBar, TextInput, HiddenField
from lite_forms.generators import confirm_form
from lite_forms.views import SingleFormView
from picklists.enums import PicklistCategories
from picklists.forms import (
    add_picklist_item_form,
    add_letter_paragraph_form,
    edit_picklist_item_form,
    edit_letter_paragraph_form,
)
from picklists.services import (
    get_picklist_item,
    get_picklists_list,
    set_picklist_item_status,
    post_picklist_item,
    put_picklist_item,
)
from teams.services import get_team
from users.services import get_gov_user


class Picklists(TemplateView):
    def get(self, request, **kwargs):
        """
        Return a list of picklists and show all the relevant items
        """
        picklist_type = request.GET.get("type", PicklistCategories.proviso.key)  # Ensure that the page has a type
        user, _ = get_gov_user(request)
        team, _ = get_team(request, user["user"]["team"]["id"])
        picklist_items = get_picklists_list(
            request, type=picklist_type, page=request.GET.get("page", 1), name=request.GET.get("name")
        )

        active_picklist_items = [x for x in picklist_items["results"] if x["status"]["key"] == "active"]
        deactivated_picklist_items = [x for x in picklist_items["results"] if x["status"]["key"] != "active"]

        filters = FiltersBar([HiddenField(name="type", value=picklist_type), TextInput(name="name", title="name")])

        context = {
            "team": team["team"],
            "active_picklist_items": active_picklist_items,
            "deactivated_picklist_items": deactivated_picklist_items,
            "data": picklist_items,
            "type": picklist_type,
            "filters": filters,
            "name": request.GET.get("name"),
            "picklist_categories": PicklistCategories.all(),
        }
        return render(request, "teams/picklists.html", context)


class PicklistsJson(TemplateView):
    def get(self, request, **kwargs):
        """
        Return JSON representation of picklists for use in picklist pickers
        """
        picklist_items = get_picklists_list(
            request,
            type=request.GET.get("type", PicklistCategories.proviso.key),
            page=request.GET.get("page", 1),
            name=request.GET.get("name"),
            show_deactivated=False,
        )
        # Convert the dates to friendly format to cut down on JavaScript code
        for item in picklist_items["results"]:
            item["updated_at"] = str_date(item["updated_at"])
        return JsonResponse(data=picklist_items)


class ViewPicklistItem(TemplateView):
    def get(self, request, **kwargs):
        picklist_item = get_picklist_item(request, str(kwargs["pk"]))

        context = {
            "title": picklist_item["name"],
            "picklist_item": picklist_item,
            "activity": picklist_item["activity"],
        }
        return render(request, "teams/picklist-item.html", context)


class AddPicklistItem(SingleFormView):
    def init(self, request, **kwargs):
        self.action = post_picklist_item
        countries, _ = get_countries(request)
        flags = get_flags(request, status=FlagStatus.ACTIVE.value)
        denial_reasons = get_denial_reasons(request, False)

        self.context = {**countries, "flags": flags, "denial_reasons": denial_reasons}
        self.success_url = reverse_lazy("picklists:picklists") + "?type=" + self.request.GET.get("type")

    def get_form(self):
        if self.request.GET.get("type") == "letter_paragraph":
            return add_letter_paragraph_form(self.request.GET.get("type"))
        else:
            return add_picklist_item_form(self.request.GET.get("type"))


class EditPicklistItem(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.object = get_picklist_item(request, self.object_pk)
        self.data = self.object
        self.action = put_picklist_item
        self.success_url = reverse_lazy("picklists:picklist_item", kwargs={"pk": self.object_pk})
        self.success_message = EditPicklistItemForm.SUCCESS_MESSAGE
        countries, _ = get_countries(request)
        flags = get_flags(request, status=FlagStatus.ACTIVE.value)
        denial_reasons = get_denial_reasons(request)

        self.context = {**countries, "flags": flags, "denial_reasons": denial_reasons}

    def get_form(self):
        if self.object["type"]["key"] == "letter_paragraph":
            return edit_letter_paragraph_form(self.object)
        else:
            return edit_picklist_item_form(self.object)


class ChangeStatusView(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.object = get_picklist_item(request, self.object_pk)
        self.action = set_picklist_item_status
        self.success_url = reverse("picklists:picklist_item", kwargs={"pk": self.object_pk})
        self.strings = ReactivatePicklistItem if self.kwargs["status"] == "reactivate" else DeactivatePicklistItem
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
