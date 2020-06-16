from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from compliance.forms import open_licence_return_form_group
from compliance.services import post_open_licence_return, get_open_licence_returns, get_open_licence_return_download
from lite_content.lite_exporter_frontend.compliance import OpenReturnsForm
from lite_forms.generators import success_page
from lite_forms.views import MultiFormView


class AnnualReturnsList(TemplateView):
    def get(self, request, *args, **kwargs):
        data = get_open_licence_returns(request)
        return render(request, "compliance/open-licence-returns/list.html", {"open_licence_returns": data})


class AnnualReturnsDownload(TemplateView):
    def get(self, request, pk):
        return get_open_licence_return_download(request, pk)


class AddAnnualReturn(MultiFormView):
    def init(self, request, **kwargs):
        self.additional_context = {
            "columns": [
                OpenReturnsForm.Upload.ExampleTable.LICENCE_COLUMN,
                OpenReturnsForm.Upload.ExampleTable.DESTINATION_COLUMN,
                OpenReturnsForm.Upload.ExampleTable.END_USER_COLUMN,
                OpenReturnsForm.Upload.ExampleTable.USAGE_COLUMN,
                OpenReturnsForm.Upload.ExampleTable.PERIOD_COLUMN,
            ],
            "rows": [
                [
                    OpenReturnsForm.Upload.ExampleTable.LICENCE_EXAMPLE,
                    OpenReturnsForm.Upload.ExampleTable.DESTINATION_EXAMPLE,
                    OpenReturnsForm.Upload.ExampleTable.END_USER_EXAMPLE_COLUMN,
                    OpenReturnsForm.Upload.ExampleTable.USAGE_EXAMPLE,
                    OpenReturnsForm.Upload.ExampleTable.PERIOD_EXAMPLE,
                ]
            ],
        }
        self.forms = open_licence_return_form_group()
        self.action = post_open_licence_return

    def get_success_url(self):
        return reverse_lazy(
            "compliance:add_open_licence_return_success",
            kwargs={"pk": self.get_validated_data()["open_licence_returns"]},
        )


class AddAnnualReturnSuccess(TemplateView):
    def get(self, request, **kwargs):
        return success_page(
            request=request,
            title=OpenReturnsForm.Success.TITLE,
            secondary_title=OpenReturnsForm.Success.SECONDARY_TITLE,
            description=OpenReturnsForm.Success.DESCRIPTION,
            what_happens_next="",
            links={
                OpenReturnsForm.Success.OPEN_LICENCE_RETURNS_LINK: reverse_lazy("compliance:open_licence_returns_list"),
                OpenReturnsForm.Success.HOME_LINK: reverse_lazy("core:home"),
            },
        )
