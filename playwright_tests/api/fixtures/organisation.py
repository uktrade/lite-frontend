import random


def organisation():
    return {
        "name": f"Org-2022{random.randrange(10000000000000)}",  # nosec
        "type": "commercial",
        "eori_number": "GB123456789000",
        "phone_number": "+441234567890",
        "website": "http://somewebsite.com",
        "sic_number": "12345",
        "vat_number": "GB123456789",
        "registration_number": "09876543",
        "user": {"first_name": "Automated", "last_name": "Test", "email": "test@ci.uktrade.io"},
        "site": {
            "name": "Headquarters",
            "address": {
                "address_line_1": "42 Question Road",
                "postcode": "BC1 2DE",
                "city": "London",
                "region": "London",
                "country": "GB",
            },
        },
    }
