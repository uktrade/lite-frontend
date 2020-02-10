from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView

from lite_content.lite_exporter_frontend import strings
from lite_forms.components import HiddenField
from lite_forms.generators import form_page, error_page
from lite_forms.submitters import submit_paged_form

from applications.services import (
    get_case_notes,
    get_application_ecju_queries,
    post_application_case_notes,
    get_ecju_query,
    put_ecju_query,
)
from end_users.forms import (
    apply_for_an_end_user_advisory_form,
    copy_end_user_advisory_form,
    end_user_advisory_success_page,
    respond_to_query_form,
    ecju_query_respond_confirmation_form,
)
from end_users.services import get_end_user_advisories, post_end_user_advisories, get_end_user_advisory


class EndUsersList(TemplateView):
    def get(self, request, **kwargs):
        end_users = get_end_user_advisories(request)

        context = {
            "end_users": end_users,
        }
        return render(request, "end-users/end-users.html", context)


class CopyAdvisory(TemplateView):

    forms = None
    data = None

    def dispatch(self, request, *args, **kwargs):
        query, _ = get_end_user_advisory(request, str(kwargs["pk"]))

        self.data = {
            "end_user.name": query["end_user"]["name"],
            "end_user.website": query["end_user"]["website"],
            "end_user.address": query["end_user"]["address"],
            "end_user.country": query["end_user"]["country"]["id"],
            "end_user.type": query["end_user"]["type"],
            "reasoning": query.get("reasoning", ""),
            "note": query.get("note", ""),
            "copy_of": query["id"],
            "contact_email": query["contact_email"],
            "contact_telephone": query["contact_telephone"],
        }

        individual, commercial = False, False

        sub_type = query["end_user"]["sub_type"]["key"]
        if sub_type != "individual":
            self.data["contact_name"] = query["contact_name"]
            self.data["contact_job_title"] = query["contact_job_title"]
        else:
            individual = True

        if sub_type == "commercial":
            commercial = True
            self.data["nature_of_business"] = query["nature_of_business"]

        self.forms = copy_end_user_advisory_form(individual, commercial)

        # Add the existing end user type as a hidden field to preserve its data
        self.forms.forms[0].questions.append(HiddenField("end_user.sub_type", query["end_user"]["sub_type"]["key"]))

        return super(CopyAdvisory, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0], data=self.data)

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.forms, post_end_user_advisories, inject_data=self.data)

        if response:
            return response

        return end_user_advisory_success_page(request, str(data["end_user_advisory"]["reference_code"]))


class ApplyForAnAdvisory(TemplateView):

    forms = None

    def dispatch(self, request, *args, **kwargs):
        individual = request.POST.get("end_user.sub_type") == "individual"
        commercial = request.POST.get("end_user.sub_type") == "commercial"
        self.forms = apply_for_an_end_user_advisory_form(individual, commercial)

        return super(ApplyForAnAdvisory, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0])

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.forms, post_end_user_advisories)
        if response:
            return response

        return end_user_advisory_success_page(request, str(data["end_user_advisory"]["reference_code"]))


class EndUserDetailEmpty(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("end_users:end_user_detail", kwargs={"pk": self.kwargs["pk"], "type": "case-notes"})


class EndUserDetail(TemplateView):
    end_user_advisory_id = None
    end_user_advisory = None
    view_type = None
    case_id = None

    def dispatch(self, request, *args, **kwargs):
        self.end_user_advisory_id = str(kwargs["pk"])
        self.end_user_advisory, self.case_id = get_end_user_advisory(request, self.end_user_advisory_id)
        self.view_type = kwargs["type"]

        if self.view_type != "case-notes" and self.view_type != "ecju-queries":
            return Http404

        return super(EndUserDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        context = {
            "case_id": self.case_id,
            "end_user_advisory": self.end_user_advisory,
            "type": self.view_type,
        }

        if self.view_type == "case-notes":
            case_notes = get_case_notes(request, self.case_id)["case_notes"]
            context["notes"] = case_notes

        if self.view_type == "ecju-queries":
            context["open_queries"], context["closed_queries"] = get_application_ecju_queries(request, self.case_id)

        return render(request, "end-users/end-user.html", context)

    def post(self, request, **kwargs):
        if self.view_type != "case-notes":
            return Http404

        response, _ = post_application_case_notes(request, self.case_id, request.POST)

        if "errors" in response:
            errors = response.get("errors")
            if errors.get("text"):
                error = errors.get("text")[0]
                error = error.replace("This field", "Case note")
                error = error.replace("this field", "the case note")  # TODO: Move to API

            else:
                error_list = []
                for key in errors:
                    error_list.append("{field}: {error}".format(field=key, error=errors[key][0]))
                error = "\n".join(error_list)
            return error_page(request, error)

        return redirect(
            reverse_lazy("end_users:end_user_detail", kwargs={"pk": self.end_user_advisory_id, "type": "case-notes"})
        )


class RespondToQuery(TemplateView):
    end_user_advisory_id = None
    end_user_advisory = None
    view_type = None
    case_id = None
    ecju_query_id = None
    ecju_query = None

    def dispatch(self, request, *args, **kwargs):
        self.end_user_advisory_id = str(kwargs["pk"])
        self.end_user_advisory, self.case_id = get_end_user_advisory(request, self.end_user_advisory_id)

        self.ecju_query_id = str(kwargs["query_pk"])
        self.ecju_query = get_ecju_query(request, self.case_id, self.ecju_query_id)

        # If an ecju query is already responded to, return user to end_user_advisory_page
        if self.ecju_query["response"]:
            return redirect(
                reverse_lazy(
                    "end_users:end_user_detail", kwargs={"pk": self.end_user_advisory_id, "type": "ecju-queries"}
                )
            )

        return super(RespondToQuery, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Will get a text area form for the user to respond to the ecju_query
        """
        return form_page(request, respond_to_query_form(self.end_user_advisory_id, self.ecju_query))

    def post(self, request, **kwargs):
        """
        will determine what form the user is on:
        if the user is on the input form will then will determine if data is valid, and move user to confirmation form
        else will allow the user to confirm they wish to respond and post data if accepted.
        """
        form_name = request.POST.get("form_name")

        if form_name == "respond_to_query":
            # Post the form data to API for validation only
            data = {"response": request.POST.get("response"), "validate_only": True}
            response, status_code = put_ecju_query(request, self.case_id, self.ecju_query_id, data)

            if status_code != 200:
                errors = response.get("errors")
                errors = {error: message for error, message in errors.items()}
                form = respond_to_query_form(self.end_user_advisory_id, self.ecju_query)
                data = {"response": request.POST.get("response")}
                return form_page(request, form, data=data, errors=errors)
            else:
                form = ecju_query_respond_confirmation_form(
                    reverse_lazy(
                        "end_users:respond_to_query",
                        kwargs={"pk": self.end_user_advisory_id, "query_pk": self.ecju_query_id},
                    )
                )
                form.questions.append(HiddenField("response", request.POST.get("response")))
                return form_page(request, form)
        elif form_name == "ecju_query_response_confirmation":
            if request.POST.get("confirm_response") == "yes":
                data, status_code = put_ecju_query(request, self.case_id, self.ecju_query_id, request.POST)
                if "errors" in data:
                    return form_page(
                        request,
                        respond_to_query_form(self.end_user_advisory_id, self.ecju_query),
                        data=request.POST,
                        errors=data["errors"],
                    )

                return redirect(
                    reverse_lazy(
                        "end_users:end_user_detail", kwargs={"pk": self.end_user_advisory_id, "type": "ecju-queries"}
                    )
                )

            elif request.POST.get("confirm_response") == "no":
                return form_page(
                    request, respond_to_query_form(self.end_user_advisory_id, self.ecju_query), data=request.POST
                )
            else:
                error = {"required": ["This field is required"]}
                form = ecju_query_respond_confirmation_form(
                    reverse_lazy(
                        "end_users:respond_to_query",
                        kwargs={"pk": self.end_user_advisory_id, "query_pk": self.ecju_query_id},
                    )
                )
                form.questions.append(HiddenField("response", request.POST.get("response")))
                return form_page(request, form, errors=error)
        else:
            # Submitted data does not contain an expected form field - return an error
            return error_page(request, strings.end_users.AttachDocumentPage.UPLOAD_GENERIC_ERROR)
