from django.urls import reverse_lazy

from applications.forms.route_of_goods import route_of_goods_form
from applications.services import get_application, put_application_route_of_goods
from lite_forms.helpers import get_all_form_components
from lite_forms.views import SingleFormView


class RouteOfGoods(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = self.get_form_data(request)
        self.form = route_of_goods_form()
        self.action = put_application_route_of_goods
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})

    def get_form_data(self, request):
        application = get_application(request, self.object_pk)
        data = {}
        if application["is_shipped_waybill_or_lading"] is not None:
            data["is_shipped_waybill_or_lading"] = application["is_shipped_waybill_or_lading"]

        if application["non_waybill_or_lading_route_details"]:
            data["non_waybill_or_lading_route_details"] = application["non_waybill_or_lading_route_details"]

        return data

    def on_submission(self, request, **kwargs):
        data = request.POST.copy()
        # Add form fields to data if they dont exist (checkboxes/radio buttons will be missing if they're not selected)
        for component in get_all_form_components(self.form):
            if component.name not in data:
                data[component.name] = None
        return data
