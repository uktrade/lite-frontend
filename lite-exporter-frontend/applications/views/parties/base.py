from http import HTTPStatus

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.parties import party_create_new_or_copy_existing_form
from applications.services import get_application, get_existing_parties, copy_party
from lite_content.lite_exporter_frontend.applications import AddPartyForm, CopyExistingPartyPage
from lite_forms.generators import form_page, error_page
from lite_forms.views import MultiFormView


class AddParty(TemplateView):
    def __init__(self, copy_url, new_url, **kwargs):
        super().__init__(**kwargs)
        self.copy_url = copy_url
        self.new_url = new_url

    def get(self, request, **kwargs):
        return form_page(request, party_create_new_or_copy_existing_form(kwargs["pk"]))

    def post(self, request, **kwargs):
        response = request.POST.get("copy_existing")
        if response:
            if response == "yes":
                return redirect(reverse_lazy(self.copy_url, kwargs=kwargs))
            else:
                return redirect(reverse_lazy(self.new_url, kwargs=kwargs))
        else:
            return form_page(
                request,
                party_create_new_or_copy_existing_form(kwargs["pk"]),
                errors={"copy_existing": [AddPartyForm.ERROR]},
            )


class SetParty(MultiFormView):
    def __init__(
        self, url, form, party_type, back_url, strings, validate_action, post_action, copy_existing=False, **kwargs,
    ):
        super().__init__(**kwargs)
        self.url = url
        self.party_type = party_type
        self.back_url = back_url
        self.strings = strings
        self.form = form
        self.copy_existing = copy_existing
        self.action = None
        self.post_action = post_action
        self.validate_action = validate_action

    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.forms = self.form(application, self.strings, self.back_url)
        self.data = {"type": self.party_type}

    def get_success_url(self):
        return reverse_lazy(
            self.url, kwargs={"pk": self.object_pk, "obj_pk": self.get_validated_data()[self.party_type]["id"]}
        )

    def on_submission(self, request, **kwargs):
        if int(self.request.POST.get("form_pk")) == len(self.forms.forms) - 1:
            self.action = self.post_action
        else:
            self.action = self.validate_action


class DeleteParty(TemplateView):
    def __init__(self, url, action, error, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.action = action
        self.error = error

    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        status_code = self.action(request, application_id, str(kwargs["obj_pk"]))

        if status_code != HTTPStatus.OK:
            return error_page(request, self.error)

        return redirect(reverse_lazy(self.url, kwargs={"pk": application_id}))


class CopyParties(TemplateView):
    def __init__(self, new_party_type, **kwargs):
        super().__init__(**kwargs)
        self.destination_url = f"applications:set_{new_party_type}"
        self.copy_url = f"applications:copy_{new_party_type}"
        self.back_url = f"applications:add_{new_party_type}"
        self.new_party_type = new_party_type

    def get(self, request, **kwargs):
        """
        List of existing parties
        """
        application_id = str(kwargs["pk"])
        parties, _ = get_existing_parties(
            request,
            application_id,
            name=request.GET.get("name"),
            address=request.GET.get("address"),
            country=request.GET.get("country"),
        )

        context = {
            "title": CopyExistingPartyPage.TITLE,
            "back_url": self.back_url,
            "filters": ["Name", "Address", "Country"],
            "draft_id": application_id,
            "data": parties,
            "url": self.copy_url,
            "new_party_type": self.new_party_type,
        }
        return render(request, "applications/parties/preexisting.html", context)


class CopyAndSetParty(SetParty):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.forms = self.form(application, self.strings, self.back_url)
        self.data = copy_party(request=request, pk=self.object_pk, party_pk=kwargs["obj_pk"])
        self.data["type"] = self.party_type
