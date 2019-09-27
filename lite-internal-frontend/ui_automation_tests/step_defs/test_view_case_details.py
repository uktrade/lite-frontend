from pytest_bdd import then, scenarios
from pages.application_page import ApplicationPage


def assert_party_data(table, headings, values):
    for heading in headings:
        assert heading.lower() in table.lower()
    for value in values:
        assert value in table


class ViewCaseDetails:
    scenarios('../features/case_view_details.feature', strict_gherkin=False)

    import logging
    log = logging.getLogger()
    console = logging.StreamHandler()
    log.addHandler(console)

    @then("I see an end user")
    def i_see_end_user_on_page(driver, context):
        destinations_table = ApplicationPage(driver).get_text_of_eu_table()
        headings = ["NAME", "TYPE", "WEBSITE", "ADDRESS", "DOCUMENT"]
        values = [
            # For whatever reason end user subtype is a dict rather than a string
            context.end_user['sub_type']['value'],
            context.end_user['name'],
            context.end_user['website'],
            context.end_user['address'],
            context.end_user['country']['name']
        ]
        assert_party_data(destinations_table, headings, values)

    @then('I see an ultimate end user')
    def i_see_ultimate_end_user_on_page(driver, context):
        destinations_table = ApplicationPage(driver).get_text_of_ueu_table()
        headings = ["NAME", "TYPE", "WEBSITE", "ADDRESS", "DOCUMENT"]
        values = [
            # context.ultimate_end_user['sub_type'],
            context.ultimate_end_user['name'],
            context.ultimate_end_user['website'],
            context.ultimate_end_user['address'],
            context.ultimate_end_user['country']['name']
        ]
        assert_party_data(destinations_table, headings, values)

    @then('I see a consignee')
    def i_see_consignee_on_page(driver, context):
        destinations_table = ApplicationPage(driver).get_text_of_consignee_table()
        headings = ["NAME", "TYPE", "WEBSITE", "ADDRESS", "DOCUMENT"]
        values = [
            # context.consignee['sub_type'],
            context.consignee['name'],
            context.consignee['website'],
            context.consignee['address'],
            context.consignee['country']['name']
        ]
        assert_party_data(destinations_table, headings, values)

    @then('I see a third party')
    def i_see_third_party_on_page(driver, context):
        destinations_table = ApplicationPage(driver).get_text_of_third_parties_table()
        headings = ["NAME", "TYPE", "WEBSITE", "ADDRESS", "DOCUMENT"]
        values = [
            # context.third_party['sub_type'],
            context.third_party['name'],
            context.third_party['website'],
            context.third_party['address'],
            context.third_party['country']['name']
        ]
        assert_party_data(destinations_table, headings, values)
