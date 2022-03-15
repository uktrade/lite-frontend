import os
import time

from playwright_tests.api.fixtures.application import create, submit, status
from playwright_tests.api.fixtures.auth_user import auth_user
from playwright_tests.api.fixtures.document import document
from playwright_tests.api.fixtures.end_use_details import end_use_details
from playwright_tests.api.fixtures.export_auth_user import export_auth_user
from playwright_tests.api.fixtures.goods import goods
from playwright_tests.api.fixtures.headers import exporter, caseworker
from playwright_tests.api.fixtures.organisation import organisation
from playwright_tests.api.fixtures.parties import end_user, ultimate_end_user, consignee, third_party
from playwright_tests.api.fixtures.route_of_goods import route_of_goods
from playwright_tests.api.fixtures.site import site
from playwright_tests.api.fixtures.user_to_org import user_to_org

from playwright_tests.api.actions.authenticate import gov_auth, export_auth
from playwright_tests.api.actions.organisation import (
    create_organisation,
    update_organisation_status,
    add_user_to_organisation,
    add_site_to_organisation,
)
from playwright_tests.api.actions.application import (
    create_draft_application,
    add_good_to_application,
    add_location_to_application,
    add_end_user_to_application,
    add_document_to_application_end_user,
    add_ultimate_end_user_to_application,
    add_consignee_to_application,
    add_third_party_to_application,
    add_end_use_details_to_application,
    add_route_of_goods_to_application,
    submit_application,
    change_application_status,
)
from playwright_tests.api.actions.goods import create_goods, create_goods_document
from dotenv import load_dotenv

load_dotenv("caseworker.env")

sso_user = os.environ.get("PW_SSO_USER")
sso_export_user = os.environ.get("PW_EXPORT_SSO_USER")


def create_application():
    # Retrieve user token
    auth_response = gov_auth(auth_user(sso_user))
    user_token = auth_response["token"]
    default_queue = auth_response["default_queue"]

    # Retrieve export user token
    export_auth_response = export_auth(export_auth_user(sso_export_user))
    export_user_token = export_auth_response["token"]

    # Create organisation
    organisation_response = create_organisation(organisation(), caseworker(user_token))
    organisation_id = organisation_response["id"]

    # Update organsation status to Active
    update_organisation_status(organisation_id, caseworker(user_token))

    # Add user to organisation caseworker
    add_user_to_organisation(organisation_id, user_to_org(sso_user), caseworker(user_token))

    # Create site for organisation
    site_response = add_site_to_organisation(organisation_id, site(), caseworker(user_token))
    site_id = site_response["site"]["id"]

    # Create an application
    application_response = create_draft_application(create, exporter(export_user_token, organisation_id))
    application_id = application_response["id"]

    # Create goods
    goods_response = create_goods(goods(), exporter(export_user_token, organisation_id))
    good_id = goods_response["good"]["id"]

    # Create good document
    create_goods_document(
        good_id, [document("goods document", "some goods document")], exporter(export_user_token, organisation_id)
    )

    # Add goods to application
    add_good_to_application(
        application_id, {**goods(), "good_id": good_id}, exporter(export_user_token, organisation_id)
    )

    # Add location to application
    add_location_to_application(application_id, {"sites": [site_id]}, exporter(export_user_token, organisation_id))

    # Add end user to application
    add_end_user_to_draft_response = add_end_user_to_application(
        application_id, end_user, exporter(export_user_token, organisation_id)
    )
    end_user_id = add_end_user_to_draft_response["end_user"]["id"]

    # Add document to end user
    add_document_to_application_end_user(
        application_id,
        end_user_id,
        document("party document", "some party document"),
        exporter(export_user_token, organisation_id),
    )

    # Add ultimate end user to application
    add_ultimate_end_user_to_application(
        application_id, ultimate_end_user, exporter(export_user_token, organisation_id)
    )

    # Add consignee to application
    add_consignee_to_application(application_id, consignee, exporter(export_user_token, organisation_id))

    # Add Third Party to application
    add_third_party_to_application(application_id, third_party, exporter(export_user_token, organisation_id))

    # Add end use details to application
    add_end_use_details_to_application(application_id, end_use_details(), exporter(export_user_token, organisation_id))

    # Add route of goods to application
    add_route_of_goods_to_application(application_id, route_of_goods(), exporter(export_user_token, organisation_id))

    # Need to wait for av-scan document task to be completed.
    time.sleep(5)

    # Submit an application
    submitted_application_response = submit_application(
        application_id, submit, exporter(export_user_token, organisation_id)
    )
    submitted_application = submitted_application_response["application"]

    # Change application status
    change_application_status(application_id, status("ogd_advice"), caseworker(user_token))

    return {
        "submitted_application": submitted_application,
        "default_queue": default_queue,
        "application_id": application_id,
    }
