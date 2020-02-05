from .api_client import ApiClient


class Cases(ApiClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def assign_case_to_queue(self, case_id=None, queue_id=None):
        queue_id = queue_id or self.context["queue_id"]
        case_id = case_id or self.context["case_id"]
        self.make_request(
            method="PUT", url="/cases/" + case_id + "/", headers=ApiClient.gov_headers, body={"queues": [queue_id]},
        )

    def assign_case_to_user(self, case_id=None, queue_id=None, gov_user_id=None):
        queue_id = queue_id or self.context["queue_id"]
        case_id = case_id or self.context["case_id"]
        gov_user_id = gov_user_id or self.context["gov_user_id"]
        case_assignments = {"case_assignments": [{"case_id": case_id, "users": [gov_user_id]}]}
        self.make_request(
            method="PUT",
            url="/queues/" + queue_id + "/case-assignments/",
            headers=ApiClient.gov_headers,
            body=case_assignments,
        )

    def assign_test_cases_to_bin(self, bin_queue_id, new_cases_queue_id):
        cases = self.make_request(
            method="GET", url="/queues/" + new_cases_queue_id + "/", headers=ApiClient.gov_headers,
        ).json()["queue"]["cases"]
        for case in cases:
            self.make_request(
                method="PUT",
                url="/cases/" + case["id"] + "/",
                headers=ApiClient.gov_headers,
                body={"queues": [bin_queue_id]},
            )

    def add_case_note(self, context, case_id):
        data = self.request_data["case_note"]
        context.case_note_text = self.request_data["case_note"]["text"]
        self.make_request(
            method="POST", url="/cases/" + case_id + "/case-notes/", headers=ApiClient.gov_headers, body=data,
        )

    def edit_case(self, app_id):
        data = self.request_data["edit_case_app"]
        self.context["edit_case_app"] = self.request_data["edit_case_app"]
        self.make_request(
            method="PUT", url="/applications/" + app_id + "/", headers=ApiClient.exporter_headers, body=data,
        )

    def add_generated_document(self, case_id, template_id):
        generated_document = self.make_request(
            method="POST",
            url="/cases/" + case_id + "/generated-documents/",
            headers=ApiClient.gov_headers,
            body={"template": template_id, "text": "random text"},
        ).json()["generated_document"]
        self.add_to_context("generated_document", generated_document)

    def manage_case_status(self, draft_id):
        draft_id_to_change = draft_id or self.context["draft_id"]
        response = self.make_request(
            method="PUT",
            url="/applications/" + draft_id_to_change + "/status/",
            headers=ApiClient.gov_headers,
            body={"status": "withdrawn"},
        )

        return response.status_code
