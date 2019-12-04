# Generic views

In order to display a form/series of forms you should extend your template view from one of LITE-Form's generic views. There are currently two available:

## SingleFormView

```
class ApplicationEditReferenceName(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_application(request, self.object_pk)
        self.form = reference_name_form(self.object_pk)
        self.action = put_application
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
```

object_pk: Refers to the object that the form is referencing. (Optional)
data: Refers to initial data to be displayed on the form. (Optional)
form: Refers to the form to be used.
action: Refers to the function that should be called on submission.
success_url: Refers to what page should be displayed on a successful submission.

## MultiFormView
