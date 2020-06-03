from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.builtins.custom_tags import str_date
from core.services import get_countries, get_denial_reasons
from flags.enums import FlagStatus
from flags.services import get_flags
from lite_forms.components import FiltersBar, TextInput, HiddenField
from lite_forms.generators import form_page
from lite_forms.views import SingleFormView
from picklists.enums import PicklistCategories
from picklists.forms import (
    add_picklist_item_form,
    deactivate_picklist_item,
    reactivate_picklist_item,
    add_letter_paragraph_form,
    edit_picklist_item_form,
    edit_letter_paragraph_form,
)
from picklists.services import get_picklist_item, put_picklist_item, get_picklists_list
from picklists.validators import validate_and_post_picklist_item, validate_and_put_picklist_item
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
        self.action = validate_and_post_picklist_item
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
        self.action = validate_and_put_picklist_item
        self.success_url = reverse_lazy("picklists:picklist_item", kwargs={"pk": self.object_pk})
        countries, _ = get_countries(request)
        flags = get_flags(request, status=FlagStatus.ACTIVE.value)
        denial_reasons = get_denial_reasons(request)

        self.context = {**countries, "flags": flags, "denial_reasons": denial_reasons}

    def get_form(self):
        if self.object["type"]["key"] == "letter_paragraph":
            return edit_letter_paragraph_form(self.object)
        else:
            return edit_picklist_item_form(self.object)


class DeactivatePicklistItem(TemplateView):
    picklist_item_id = None
    picklist_item = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.picklist_item_id = str(kwargs["pk"])
        self.picklist_item = get_picklist_item(request, self.picklist_item_id)
        self.form = deactivate_picklist_item(self.picklist_item)

        return super(DeactivatePicklistItem, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        if self.picklist_item["status"]["key"] == "deactivated":
            raise Http404

        return form_page(request, self.form)

    def post(self, request, **kwargs):
        data = {"status": "deactivated"}

        put_picklist_item(request, self.picklist_item_id, data)
        return redirect(reverse_lazy("picklists:picklist_item", kwargs={"pk": self.picklist_item["id"]}))


class ReactivatePicklistItem(TemplateView):
    picklist_item_id = None
    picklist_item = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.picklist_item_id = str(kwargs["pk"])
        self.picklist_item = get_picklist_item(request, self.picklist_item_id)
        self.form = reactivate_picklist_item(self.picklist_item)

        return super(ReactivatePicklistItem, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        if self.picklist_item["status"]["key"] != "deactivated":
            raise Http404

        return form_page(request, self.form)

    def post(self, request, **kwargs):
        data = {"status": "active"}

        put_picklist_item(request, self.picklist_item_id, data)
        return redirect(reverse_lazy("picklists:picklist_item", kwargs={"pk": self.picklist_item["id"]}))
