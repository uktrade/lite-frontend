import copy
from abc import ABC
from typing import List

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from lite_forms.components import FormGroup, Form
from lite_forms.generators import form_page
from lite_forms.helpers import (
    handle_lists,
    get_next_form,
    nest_data,
    flatten_data,
    remove_unused_errors,
    convert_form_to_summary_list_instance,
    insert_hidden_fields,
    get_all_form_components,
    validate_data_unknown,
)
from lite_forms.submitters import submit_paged_form

ACTION = "_action"
VALIDATE_ONLY = "validate_only"


class Actions:
    SUBMIT = "submit"
    RETURN = "return"
    CHANGE = "change"
    FINISH = "finish"


class FormView(TemplateView, ABC):
    """
    Base class with properties necessary to support getting and posting to forms within subclasses of this
    class, using supplied data and actions.

    Will call validate() if it exists with parsed data (not validated yet)
    """

    data: dict = None
    action: callable = None
    object_pk = None
    success_url: str = ""
    success_message: str = ""

    def get_data(self):
        data = getattr(self, "data", {})
        return data

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
        data = getattr(self, "_validated_data", {}).copy()
        return data

    def init(self, request, **kwargs):
        raise NotImplementedError("init function not implemented")


class SingleFormView(FormView):
    """
    Takes a single Form as a parameter and handles getting and posting to it using supplied values.
    """

    form: Form = None
    redirect: bool = True
    context: dict = {}

    def get_form(self):
        if not self.form:
            raise AttributeError("form has not been set")

        return self.form

    def init(self, request, **kwargs):
        super().init(request, **kwargs)

    def on_submission(self, request, **kwargs):
        return request.POST.copy()

    def clean_data(self, data):
        return data

    def post_success_step(self):
        if self.success_message:
            messages.success(self.request, self.success_message)

    def get(self, request, **kwargs):
        override_return = self.init(request, **kwargs)  # noqa
        if override_return:
            if isinstance(override_return, str):
                return redirect(override_return)
            return override_return
        return form_page(request, self.get_form(), data=self.get_data(), extra_data=self.context)

    def post(self, request, **kwargs):
        self.init(request, **kwargs)
        data = self.on_submission(request, **kwargs)

        # Handle lists (such as checkboxes)
        data = handle_lists(data)

        self._validated_data = data

        if self.get_object_pk():
            validated_data, _ = self.get_action()(request, self.get_object_pk(), self.clean_data(data.copy()))  # noqa
        else:
            validated_data, _ = self.get_action()(request, self.clean_data(data.copy()))  # noqa

        if "errors" in validated_data:
            return form_page(
                request, self.get_form(), data=data, errors=validated_data.get("errors"), extra_data=self.context
            )

        self._validated_data = validated_data

        self.post_success_step()

        if self.redirect:
            return redirect(self.get_success_url())
        else:
            return form_page(request, self.get_form(), data=data)


class MultiFormView(FormView):
    """
    Takes a FormGroup as a parameter and handles getting and posting to forms in the group using supplied values.

    Interface:
        init(): Called on every GET and POST request prior to post() and get()
    """

    forms: FormGroup = None
    additional_context: dict = {}
    hide_unused_errors = True

    def get_forms(self):
        if not self.forms:
            raise AttributeError("form has not been set")

        return self.forms

    def init(self, request, **kwargs):
        super().init(request, **kwargs)

    def get_form(self, form_pk):
        forms = self.forms.get_forms()
        if len(forms) < (form_pk + 1):
            raise AttributeError("Form index exceeds the number of forms in the form group")
        return forms[form_pk]

    def on_submission(self, request, **kwargs):
        return

    def post_success_step(self):
        if self.success_message:
            messages.success(self.request, self.success_message)

    def get(self, request, **kwargs):
        self.init(request, **kwargs)
        form = self.get_forms().forms[0]
        return form_page(
            request, form, data=self.get_data(), extra_data={"form_pk": form.pk, **self.additional_context}
        )

    def post(self, request, **kwargs):
        self.init(request, **kwargs)
        submission = self.on_submission(request, **kwargs)  # noqa

        if submission:
            return redirect(submission)

        response, data = submit_paged_form(
            request,
            self.get_forms(),
            self.get_action(),
            object_pk=self.get_object_pk(),
            inject_data=self.get_data(),
            additional_context=self.additional_context,
            hide_unused_errors=self.hide_unused_errors,
        )
        # If there are more forms to go through, continue
        if response:
            return response

        self._validated_data = data

        self.post_success_step()

        return redirect(self.get_success_url())


class SummaryListFormView(FormView):
    """
    Multi form group with a summary list at the end of the flow.
    """

    forms: FormGroup = None
    summary_list_title = "Check your answers before sending your application"
    summary_list_button = "Accept and send"
    summary_list_notice_title = "Now send your application"
    summary_list_notice_text = (
        "By submitting this notification you are confirming that, "
        "to the best of your knowledge, the details you are providing are correct."
    )
    hide_titles = False
    _validated_data = {}
    hide_components: List = None
    validate_only_until_final_submission = True
    additional_context: dict = {}
    cancel_link_prefix = "or "
    cancel_link_text = ""
    cancel_link_url = ""

    def get_forms(self):
        if not self.forms:
            raise AttributeError("forms have not been set")

        return self.forms

    def init(self, request, **kwargs):
        super().init(request, **kwargs)

    def clean_data(self, data):
        data = data.copy()
        while "csrfmiddlewaretoken" in data:
            del data["csrfmiddlewaretoken"]
        while "form_pk" in data:
            del data["form_pk"]
        while ACTION in data:
            del data[ACTION]
        return data

    def prettify_data(self, data):
        """
        Takes the data to be presented on the summary list and manipulates it
        to be human readable
        """
        for key in data.keys():
            if data[key] is True:
                data[key] = "Yes"
            elif data[key] is False:
                data[key] = "No"
            elif isinstance(data[key], dict):
                if "key" in data[key] and "value" in data[key]:
                    data[key] = data[key]["value"]
        return data

    def generate_summary_list(self):
        self.init(self.request, **self.kwargs)
        data = self.clean_data(self.get_validated_data())
        context = {
            "forms": self.get_forms(),
            "data": data,
            "pretty_data": self.prettify_data(data.copy()),
            "title": self.summary_list_title,
            "button": self.summary_list_button,
            "notice_title": self.summary_list_notice_title,
            "notice": self.summary_list_notice_text,
            "hide_components": self.hide_components if self.hide_components else {},
            "cancel_link_prefix": self.cancel_link_prefix,
            "cancel_link_text": self.cancel_link_text,
            "cancel_link_url": self.cancel_link_url,
            "hide_titles": self.hide_titles,
            **self.additional_context,
        }
        return render(self.request, "summary-list.html", context)

    def get(self, request, **kwargs):
        self.init(request, **kwargs)

        if self.data:
            self._validated_data = self.data.copy()
            return self.generate_summary_list()

        form = self.get_forms().forms[0]
        return form_page(
            request, form, data=self.get_data(), extra_data={"form_pk": form.pk, **self.additional_context}
        )

    def _post(self, request, **kwargs):
        self.init(request, **kwargs)
        self._validated_data = request.POST.copy()
        self._validated_data = handle_lists(self._validated_data)

        action = self.get_validated_data()[ACTION]
        form_pk = str(self.get_validated_data().get("form_pk", ""))
        post_errors = None

        post_function = getattr(self, f"post_form_{form_pk}", None)
        if post_function:
            post_errors = post_function(request, **kwargs)

        if self.validate_only_until_final_submission:
            self._validated_data[VALIDATE_ONLY] = True

        if form_pk:
            return self.get_next_form_page(form_pk, action, request, post_errors)
        elif action == Actions.FINISH:
            self._validated_data = nest_data(self.get_validated_data())
            self._validated_data[VALIDATE_ONLY] = False

            validated_data = validate_data_unknown(
                self.get_object_pk(), self.get_action(), request, self.get_validated_data()
            )

            if "errors" not in validated_data:
                if self.success_message:
                    messages.success(self.request, self.success_message)

                return redirect(self.get_success_url())

        if self.validate_only_until_final_submission:
            return self.generate_summary_list()

        return redirect(request.path)

    def post(self, request, **kwargs):
        return self._post(request, **kwargs)

    def get_next_form_page(self, form_pk, action, request, post_errors):
        form = copy.deepcopy(next(form for form in self.get_forms().forms if str(form.pk) == form_pk))

        # Add form fields to validated_data if they dont exist
        for component in get_all_form_components(form):
            if component.name not in self._validated_data and component.name[:-2] not in self._validated_data:
                self._validated_data[component.name] = ""

        if action == Actions.SUBMIT or action == Actions.RETURN:
            validated_data = validate_data_unknown(
                self.get_object_pk(), self.get_action(), request, nest_data(self.get_validated_data())
            )
            validated_data["errors"] = validated_data.get("errors", {})
            errors = validated_data["errors"]
            if post_errors:
                errors.update(post_errors)

            if errors:
                errors = flatten_data(validated_data["errors"])
                errors = remove_unused_errors(errors, form)
            if errors:
                insert_hidden_fields(self.get_validated_data(), form)

                if action == Actions.RETURN:
                    form = convert_form_to_summary_list_instance(form)

                return form_page(
                    request,
                    form,
                    data=self.get_validated_data(),
                    errors=errors,
                    extra_data={"form_pk": form.pk, **self.additional_context},
                )

            if action != Actions.RETURN:
                next_form = get_next_form(form.pk, self.get_forms())

                if next_form:
                    insert_hidden_fields(self.get_validated_data(), next_form)

                    return form_page(
                        request,
                        next_form,
                        data=self.get_validated_data(),
                        extra_data={"form_pk": next_form.pk, **self.additional_context},
                    )
        elif action == Actions.CHANGE:
            insert_hidden_fields(self.get_validated_data(), form)
            return form_page(
                request,
                convert_form_to_summary_list_instance(form),
                data=self.get_validated_data(),
                extra_data={"form_pk": form.pk, **self.additional_context},
            )

        if self.validate_only_until_final_submission:
            return self.generate_summary_list()

        return redirect(request.path)

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            if request.method.lower() == "post":
                return self.post(request, **kwargs)
            else:
                return self.get(request, **kwargs)

        handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
