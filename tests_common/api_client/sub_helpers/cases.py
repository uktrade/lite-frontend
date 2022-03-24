from django.utils import timezone


class Cases:
    def __init__(self, api_client, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data

    def assign_case_to_queue(self, case_id=None, queue_id=None):
        queue_id = queue_id or self.api_client.context["queue_id"]
        case_id = case_id or self.api_client.context["case_id"]
        self.api_client.make_request(
            method="PUT",
            url="/cases/" + case_id + "/queues/",
            headers=self.api_client.gov_headers,
            body={"queues": [queue_id]},
        )

    def assign_case_to_user(self, case_id=None, queue_id=None, gov_user_id=None):
        queue_id = queue_id or self.api_client.context["queue_id"]
        case_id = case_id or self.api_client.context["case_id"]
        gov_user_id = gov_user_id or self.api_client.context["gov_user_id"]
        case_assignments = {"case_assignments": [{"case_id": case_id, "users": [gov_user_id]}]}
        self.api_client.make_request(
            method="PUT",
            url="/queues/" + queue_id + "/case-assignments/",
            headers=self.api_client.gov_headers,
            body=case_assignments,
        )

    def assign_test_cases_to_bin(self, bin_queue_id, new_cases_queue_id):
        cases = self.api_client.make_request(
            method="GET",
            url="/queues/" + new_cases_queue_id + "/",
            headers=self.api_client.gov_headers,
        ).json()["queue"]["cases"]
        for case in cases:
            self.api_client.make_request(
                method="PUT",
                url="/cases/" + case["id"] + "/",
                headers=self.api_client.gov_headers,
                body={"queues": [bin_queue_id]},
            )

    def add_case_note(self, context, case_id, note=None):
        data = self.request_data["case_note"]
        if note is not None:
            data["text"] = note
        context.case_note_text = self.request_data["case_note"]["text"]
        self.api_client.make_request(
            method="POST",
            url="/cases/" + case_id + "/case-notes/",
            headers=self.api_client.gov_headers,
            body=data,
        )

    def edit_case(self, app_id):
        data = self.request_data["edit_case_app"]
        self.api_client.context["edit_case_app"] = self.request_data["edit_case_app"]
        self.api_client.make_request(
            method="PUT",
            url="/applications/" + app_id + "/",
            headers=self.api_client.exporter_headers,
            body=data,
        )

    def add_generated_document(self, case_id, template_id, advice_type=None):
        generated_document = self.api_client.make_request(
            method="POST",
            url="/cases/" + case_id + "/generated-documents/",
            headers=self.api_client.gov_headers,
            body={
                "template": template_id,
                "text": "random text",
                "visible_to_exporter": True,
                "advice_type": advice_type,
            },
        ).json()["generated_document"]
        self.api_client.add_to_context("generated_document", generated_document)

    def finalise_licence(self, case_id, save_licence=True):
        response = self.api_client.make_request(
            method="PUT",
            url="/cases/" + case_id + "/finalise/",
            headers=self.api_client.gov_headers,
        ).json()
        if save_licence:
            self.api_client.add_to_context("licence", response["licence"])

    def manage_case_status(self, draft_id, status="withdrawn"):
        draft_id_to_change = draft_id or self.api_client.context["draft_id"]
        response = self.api_client.make_request(
            method="PUT",
            url="/applications/" + draft_id_to_change + "/status/",
            headers=self.api_client.gov_headers,
            body={"status": status},
        )

        return response.status_code

    def finalise_case(self, draft_id, action, additional_data=None):
        date = timezone.localtime()
        data = {"action": action, "day": date.day, "month": date.month, "year": date.year}
        if additional_data:
            data.update(additional_data)

        self.api_client.make_request(
            method="PUT",
            url="/applications/" + draft_id + "/final-decision/",
            headers=self.api_client.gov_headers,
            body=data,
        )

    def create_user_advice(self, case_id, data):
        self.api_client.make_request(
            method="POST",
            url="/cases/" + case_id + "/user-advice/",
            headers=self.api_client.gov_headers,
            body=data,
        )

    def add_good_country_decisions(self, case_id, data):
        self.api_client.make_request(
            method="POST",
            url="/cases/" + case_id + "/goods-countries-decisions/",
            headers=self.api_client.gov_headers,
            body=data,
        )

    def create_team_advice(self, case_id, data):
        self.api_client.make_request(
            method="POST",
            url="/cases/" + case_id + "/team-advice/",
            headers=self.api_client.gov_headers,
            body=data,
        )

    def create_final_advice(self, case_id, data):
        self.api_client.make_request(
            method="POST",
            url="/cases/" + case_id + "/final-advice/",
            headers=self.api_client.gov_headers,
            body=data,
        )

    def get_compliance_id_for_case(self, case_id):
        case = self.api_client.make_request(
            method="GET", url="/compliance/case/" + case_id, headers=self.api_client.gov_headers
        ).json()
        return case["ids"]

    def create_compliance_visit_case(self, complaince_site_case_id):
        case = self.api_client.make_request(
            method="POST",
            url=f"/compliance/site/{complaince_site_case_id}/visit/",
            headers=self.api_client.gov_headers,
        ).json()["data"]
        return case["id"]

    def get_case_info(self, case_id):
        return self.api_client.make_request(
            method="GET", url="/cases/" + case_id + "/", headers=self.api_client.gov_headers
        ).json()["case"]
