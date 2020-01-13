from http import HTTPStatus

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.parties import party_create_new_or_copy_existing_form
from applications.services import get_application, get_existing_parties
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
    def __init__(self, url, form, name, back_url, action, strings, multiple_allowed, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.name = name
        self.back_url = back_url
        self.action = action
        self.strings = strings
        self.form = form
        self.multiple_allowed = multiple_allowed

    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.forms = self.form(application, self.strings, self.back_url)
        if self.multiple_allowed:
            self.data = None
        else:
            self.data = application[self.name]

    def get_success_url(self):
        if self.multiple_allowed:
            return reverse_lazy(
                self.url, kwargs={"pk": self.object_pk, "obj_pk": self.get_validated_data()[self.name]["id"]}
            )
        else:
            return reverse_lazy(self.url, kwargs={"pk": self.object_pk})


class DeleteParty(TemplateView):
    def __init__(self, url, action, error, multiple_allowed, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.action = action
        self.error = error
        self.multiple_allowed = multiple_allowed

    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        if self.multiple_allowed:
            status_code = self.action(request, application_id, str(kwargs["obj_pk"]))
        else:
            status_code = self.action(request, application_id)

        if status_code != HTTPStatus.NO_CONTENT:
            return error_page(request, self.error)

        return redirect(reverse_lazy(self.url, kwargs={"pk": application_id}))


class ExistingPartiesList(TemplateView):
    def __init__(self, destination_url, back_url, **kwargs):
        super().__init__(**kwargs)
        self.destination_url = destination_url
        self.back_url = back_url

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
            "url": self.destination_url,
        }
        return render(request, "applications/parties/preexisting.html", context)
