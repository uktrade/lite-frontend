from .check_documents import check_documents
from .seed_classes.additional_document import SeedAdditionalDocument
from .seed_classes.case import Case
from .seed_classes.clc import Clc
from .seed_classes.document_template import DocumentTemplate
from .seed_classes.ecju import Ecju
from .seed_classes.good import Good
from .seed_classes.organisation import Organisation
from .seed_classes.party import Party
from .seed_classes.picklist import Picklist
from .seed_classes.queue import Queue
from .seed_classes.user import User
from .make_requests import make_request
from .request_data import create_request_data


class SeedData:
    gov_headers = {"content-type": "application/json"}
    export_headers = {"content-type": "application/json"}
    headers_initialised = False
    context = {}

    def __init__(self, seed_data_config):
        exporter_user = seed_data_config["exporter"]
        gov_user = seed_data_config["gov"]
        self.base_url = seed_data_config["api_url"].rstrip("/")
        self.request_data = create_request_data(
            exporter_user=exporter_user, gov_user=gov_user, base_url=self.base_url
        )

        if not self.headers_initialised:
            self.initialise_headers()
        else:
            self.seed_user = User(
                self.base_url,
                self.gov_headers,
                self.export_headers,
                self.request_data,
                self.context,
            )
            self.seed_org = Organisation(
                self.base_url,
                self.gov_headers,
                self.export_headers,
                self.request_data,
                self.context,
            )

        self.seed_good = Good(
            self.base_url,
            self.gov_headers,
            self.export_headers,
            self.request_data,
            self.context,
        )
        self.seed_clc = Clc(
            self.base_url,
            self.gov_headers,
            self.export_headers,
            self.request_data,
            self.context,
        )
        self.seed_party = Party(
            self.base_url,
            self.gov_headers,
            self.export_headers,
            self.request_data,
            self.context,
        )
        self.seed_ecju = Ecju(
            self.base_url,
            self.gov_headers,
            self.export_headers,
            self.request_data,
            self.context,
        )
        self.seed_picklist = Picklist(
            self.base_url,
            self.gov_headers,
            self.export_headers,
            self.request_data,
            self.context,
        )
        self.seed_case = Case(
            self.base_url,
            self.gov_headers,
            self.export_headers,
            self.request_data,
            self.context,
        )
        self.seed_queue = Queue(
            self.base_url,
            self.gov_headers,
            self.export_headers,
            self.request_data,
            self.context,
        )
        self.seed_additional_doc = SeedAdditionalDocument(
            self.base_url,
            self.gov_headers,
            self.export_headers,
            self.request_data,
            self.context,
        )
        self.seed_document_template = DocumentTemplate(
            self.base_url,
            self.gov_headers,
            self.export_headers,
            self.request_data,
            self.context,
        )

    def initialise_headers(self):
        self.seed_user = User(
            self.base_url,
            self.gov_headers,
            self.export_headers,
            self.request_data,
            self.context,
        )
        self.seed_user.auth_gov_user()
        self.seed_org = Organisation(
            self.base_url,
            self.gov_headers,
            self.export_headers,
            self.request_data,
            self.context,
        )
        self.seed_org.setup_org()
        self.seed_user.auth_export_user()
        self.headers_initialised = True

    def log(self, text):
        print(text)

    def add_to_context(self, name, value):
        self.log(name + ": " + str(value))
        self.context[name] = value

    def add_site(self, draft_id):
        self.log("Adding site: ...")
        make_request(
            "POST",
            base_url=self.base_url,
            url="/applications/" + draft_id + "/sites/",
            headers=self.export_headers,
            body={"sites": [self.context["primary_site_id"]]},
        )

    def create_draft(self, draft):
        self.log("Creating draft: ...")
        data = self.request_data["application"] if draft is None else draft
        response = make_request(
            "POST",
            base_url=self.base_url,
            url="/applications/",
            headers=self.export_headers,
            body=data,
        )
        draft_id = response.json()["application"]["id"]
        self.add_to_context("draft_id", draft_id)
        return draft_id

    def add_countries(self, draft_id):
        self.log("Adding countries: ...")
        make_request(
            "POST",
            base_url=self.base_url,
            url="/applications/" + draft_id + "/countries/",
            headers=self.export_headers,
            body={"countries": ["US"]},
        )
        self.add_to_context("country", {"code": "US", "name": "United States"})

    def add_draft(
        self,
        draft=None,
        good=None,
        end_user=None,
        ultimate_end_user=None,
        consignee=None,
        third_party=None,
        additional_documents=None,
    ):
        draft_id = self.create_draft(draft)
        self.add_site(draft_id)
        self.seed_party.add_end_user(draft_id, end_user)
        self.seed_good.add_good_to_draft(draft_id, good)
        ultimate_end_user_id = self.seed_party.add_ultimate_end_user(
            draft_id, ultimate_end_user
        )
        self.seed_party.add_consignee(draft_id, consignee)
        third_party_id = self.seed_party.add_third_party(draft_id, third_party)
        additional_document_id = self.seed_additional_doc.add_additional_document(
            draft_id, additional_documents
        )
        check_documents(
            base_url=self.base_url,
            export_headers=self.export_headers,
            draft_id=draft_id,
            ultimate_end_user_id=ultimate_end_user_id,
            third_party_id=third_party_id,
            additional_document_id=additional_document_id,
        )

    def add_open_draft(self, draft=None):
        draft_id = self.create_draft(draft)
        self.add_to_context("open_draft_id", draft_id)
        self.add_site(draft_id)
        self.add_countries(draft_id)
        self.seed_good.add_open_draft_good(draft_id)

    def submit_application(self, draft_id):
        self.log("Submitting application: ...")
        draft_id_to_submit = draft_id if None else self.context["draft_id"]  # noqa
        response = make_request(
            "PUT",
            base_url=self.base_url,
            url="/applications/" + draft_id_to_submit + "/submit/",
            headers=self.export_headers,
        )
        return response.json()["application"]

    def submit_standard_application(self, draft_id=None):
        item = self.submit_application(draft_id)
        self.add_to_context("application_id", item["id"])
        self.add_to_context("case_id", item["case_id"])

    def submit_open_application(self, draft_id=None):
        item = self.submit_application(draft_id)
        self.add_to_context("application_id", item["id"])
        self.add_to_context("case_id", item["case_id"])

    def manage_case_status(self, draft_id):
        draft_id_to_change = draft_id if None else self.context["draft_id"]  # noqa
        response = make_request(
            "PUT",
            base_url=self.base_url,
            url="/applications/" + draft_id_to_change + "/status/",
            headers=self.gov_headers,
            body={"status": "withdrawn"},
        )

        return response.status_code
