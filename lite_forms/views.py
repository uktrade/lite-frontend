from abc import ABC

from django.shortcuts import redirect
from django.views.generic import TemplateView

from lite_forms.components import FormGroup, Form
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form


class FormView(TemplateView, ABC):
    """
    Base class with properties necessary to support getting and posting to forms within subclasses of this
    class, using supplied data and actions.
    """

    data: dict = None
    action: callable = None
    object_pk = None
    success_url: str = ""

    def get_data(self):
        return self.data

    def get_action(self):
        if not self.action:
            raise AttributeError("action has not been set")

        return self.action

    def get_object_pk(self):
        return self.object_pk

    def get_success_url(self):
        if not self.success_url:
            raise AttributeError("success_url has not been set")

        return self.success_url

    def get_validated_data(self):
        return self._validated_data

    def init(self, request, **kwargs):
        raise NotImplementedError("init function not implemented")


class SingleFormView(FormView):
    """
    Takes a single Form as a parameter and handles getting and posting to it using supplied values.
    """

    form: Form = None

    def get_form(self):
        if not self.form:
            raise AttributeError("form has not been set")

        return self.form

    def init(self, request, **kwargs):
        super().init(request, **kwargs)

    def get(self, request, **kwargs):
        self.init(request, **kwargs)
        return form_page(request, self.get_form(), data=self.get_data())

    def post(self, request, **kwargs):
        self.init(request, **kwargs)
        data = request.POST.copy()

        if self.get_object_pk():
            validated_data, _ = self.get_action()(  # noqa
                request, self.get_object_pk(), data
            )
        else:
            validated_data, _ = self.get_action()(request, data)  # noqa

        if "errors" in validated_data:
            return form_page(
                request, self.get_form(), data=data, errors=validated_data.get("errors")
            )

        self._validated_data = validated_data

        return redirect(self.get_success_url())


class MultiFormView(FormView):
    """
    Takes a FormGroup as a parameter and handles getting and posting to forms in the group using supplied values.
    """

    forms: FormGroup = None

    def get_forms(self):
        if not self.forms:
            raise AttributeError("form has not been set")

        return self.forms

    def init(self, request, **kwargs):
        super().init(request, **kwargs)

    def on_submission(self, request, **kwargs):
        pass

    def get(self, request, **kwargs):
        self.init(request, **kwargs)
        form = self.get_forms().forms[0]
        return form_page(
            request, form, data=self.get_data(), extra_data={"form_pk": form.pk}
        )

    def post(self, request, **kwargs):
        self.init(request, **kwargs)
        self.on_submission(request, **kwargs)

        response, data = submit_paged_form(
            request, self.get_forms(), self.get_action(), object_pk=self.get_object_pk()
        )

        # If there are more forms to go through, continue
        if response:
            return response

        self._validated_data = data

        return redirect(self.get_success_url())
