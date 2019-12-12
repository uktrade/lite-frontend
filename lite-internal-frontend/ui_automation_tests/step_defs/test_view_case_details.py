from pytest_bdd import then, scenarios, when
from pages.application_page import ApplicationPage
from shared.tools.utils import get_lite_client


def assert_party_data(table, headings, values):
    for heading in headings:
        assert heading.lower() in table.lower()
    for value in values:
        assert value in table


class ViewCaseDetails:
    scenarios("../features/view_case_details.feature", strict_gherkin=False)

    import logging

    log = logging.getLogger()
    console = logging.StreamHandler()
    log.addHandler(console)

    @when("the exporter user has edited the case")
    def exporter_user_has_edited_case(driver, context, seed_data_config):
        lite_client = get_lite_client(context, seed_data_config)
        lite_client.seed_case.edit_case(context.app_id)

    @then("I see that changes have been made to the case")
    def changes_have_been_made_to_case(driver, context, exporter_info, seed_data_config):
        app_page = ApplicationPage(driver)
        case_notification_anchor = app_page.get_case_notification_anchor()

        lite_client = get_lite_client(context, seed_data_config)

        audit_text = (
            ' updated the application name from "'
            + context.app_name
            + '" to "'
            + lite_client.context["edit_case_app"]["name"]
            + '".'
        )

        last_exporter_case_activity_id = app_page.get_case_activity_id_by_audit_text(audit_text)
        expected_anchor_href = driver.current_url + "#" + last_exporter_case_activity_id

        assert case_notification_anchor.get_attribute("href") == expected_anchor_href

    @then("I see an end user")
    def i_see_end_user_on_page(driver, context):
        destinations_table = ApplicationPage(driver).get_text_of_eu_table()
        headings = ["NAME", "TYPE", "WEBSITE", "ADDRESS", "DOCUMENT"]
        values = [
            # For whatever reason end user subtype is a dict rather than a string
            context.end_user["sub_type"]["value"],
            context.end_user["name"],
            context.end_user["website"],
            context.end_user["address"],
            context.end_user["country"]["name"],
        ]
        assert_party_data(destinations_table, headings, values)

    @then("I see an ultimate end user")
    def i_see_ultimate_end_user_on_page(driver, context):
        destinations_table = ApplicationPage(driver).get_text_of_ueu_table()
        headings = ["NAME", "TYPE", "WEBSITE", "ADDRESS", "DOCUMENT"]
        values = [
            # context.ultimate_end_user['sub_type'],
            context.ultimate_end_user["name"],
            context.ultimate_end_user["website"],
            context.ultimate_end_user["address"],
            context.ultimate_end_user["country"]["name"],
        ]
        assert_party_data(destinations_table, headings, values)

    @then("I see a consignee")
    def i_see_consignee_on_page(driver, context):
        destinations_table = ApplicationPage(driver).get_text_of_consignee_table()
        headings = ["NAME", "TYPE", "WEBSITE", "ADDRESS", "DOCUMENT"]
        values = [
            # context.consignee['sub_type'],
            context.consignee["name"],
            context.consignee["website"],
            context.consignee["address"],
            context.consignee["country"]["name"],
        ]
        assert_party_data(destinations_table, headings, values)

    @then("I see a third party")
    def i_see_third_party_on_page(driver, context):
        destinations_table = ApplicationPage(driver).get_text_of_third_parties_table()
        headings = ["NAME", "TYPE", "WEBSITE", "ADDRESS", "DOCUMENT"]
        values = [
            # context.third_party['sub_type'],
            context.third_party["name"],
            context.third_party["website"],
            context.third_party["address"],
            context.third_party["country"]["name"],
        ]
        assert_party_data(destinations_table, headings, values)
