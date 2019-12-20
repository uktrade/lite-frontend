from faker import Faker

from fixtures.env import env
from shared.api.client import post
from shared.tools.helpers import strip_special_characters, get_current_date_time

fake = Faker()


def add_site(organisation_id, headers):
    data = {
        "name": strip_special_characters(fake.company()) + get_current_date_time(),
        "address": {
            "address_line_1": fake.street_address(),
            "city": fake.city(),
            "postcode": fake.postcode(),
            "region": fake.state(),
            "country": "GB",
        },
    }
    return post(f"/organisations/{organisation_id}/sites/", json=data, headers=headers).json()["site"]
