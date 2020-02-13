from django.urls import reverse_lazy

from applications.forms.edit import reference_name_form, goods_categories
from applications.helpers.get_application_edit_type import get_application_edit_type, ApplicationEditTypes
from applications.services import get_application, put_application
from lite_content.lite_exporter_frontend import applications
from lite_forms.generators import error_page
from lite_forms.views import SingleFormView


class EditReferenceName(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_application(request, self.object_pk)
        self.form = reference_name_form(self.object_pk)
        self.action = put_application
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})


class EditGoodsCategories(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.data = {"goods_categories": [x["key"] for x in application["goods_categories"]]}
        self.form = goods_categories(self.object_pk)
        self.action = put_application
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})

        if get_application_edit_type(application) == ApplicationEditTypes.MINOR_EDIT:
            return error_page(request, applications.GoodsCategories.ERROR)

    def on_submission(self, request, **kwargs):
        data = request.POST.copy()

        if "goods_categories[]" not in data:
            return {"goods_categories": []}

        return data
