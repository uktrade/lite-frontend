from faker import Faker  # noqa

fake = Faker()


class Ogel:
    def __init__(self, api_client, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data

    def add_ogel(self, context):
        context.ogel_name = fake.bs()
        return self.api_client.make_request(
            method="POST",
            url="/open-general-licences/",
            headers=self.api_client.gov_headers,
            body={
                "name": context.ogel_name,
                "control_list_entries": ["ML1a"],
                "countries": ["GB"],
                "url": "https://www.gov.uk/government/publications/open-general-export-licence-military-goods-government-or-nato-end-use--6",
                "description": fake.paragraph(),
                "registration_required": True,
                "case_type": "00000000-0000-0000-0000-000000000002",
            },
        ).json()["id"]

    def add_ogel_application(self, ogel_id):
        return self.api_client.make_request(
            method="POST",
            url="/licences/open-general-licences/",
            headers=self.api_client.exporter_headers,
            body={"open_general_licence": ogel_id,},
        ).json()
