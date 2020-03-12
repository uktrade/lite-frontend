from pytest_bdd import when, then, parsers, scenarios, given
from pages.case_list_page import CaseListPage
from pages.shared import Shared

from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.shared import functions

from ui_automation_tests.pages.assign_user_page import AssignUserPage
from ui_automation_tests.shared.tools.helpers import get_formatted_date_time_m_d_h_s
from ui_automation_tests.shared.tools.utils import get_lite_client

scenarios("../features/assign_users_to_queue.feature", strict_gherkin=False)


@when("I select the checkbox for previously created case to be assigned")
def click_checkbox_for_application(driver, internal_url, context):
    CaseListPage(driver).click_on_case_checkbox(context.case_id)
    CaseListPage(driver).click_on_assign_users_button()


@when("I select user to assign SSO users name")
def assign_user_to_case(driver, internal_info, context):
    driver.find_element_by_id(internal_info["name"]).click()
    context.user_name = internal_info["name"]
    Shared(driver).click_submit()


@then("user is assignee on case list")
def user_is_on_case_list(driver, context):
    assert context.user_name in CaseListPage(driver).get_text_of_assignees(driver, context.case_id), (
        "user name " + context.user_name + " is not an assignee on case list"
    )


@then("user is not an assignee on case list")
def user_is_not_on_case_list(driver, context):
    assert context.user_name in CaseListPage(driver).get_text_of_assignees(driver, context.case_id), (
        "user name " + context.user_name + " is an assignee on case list"
    )


@when("I filter assigned user by Not Assigned")
def i_filter_case_officer_by_not_assigned(driver):
    CaseListPage(driver).click_show_filters_link()
    CaseListPage(driver).enter_assigned_user_filter_text("Not assigned")
    CaseListPage(driver).click_apply_filters_button()


@when("I filter assigned user by SSO users name")
def i_filter_case_officer_by_not_assigned(driver, context):
    CaseListPage(driver).click_show_filters_link()
    CaseListPage(driver).enter_assigned_user_filter_text(context.user_name)
    CaseListPage(driver).click_apply_filters_button()


@then("only SSO users name is displayed in user list for assign cases")
def user_is_on_case_list(driver, internal_info):
    elements = CaseListPage(driver).get_text_checkbox_elements()
    for element in elements:
        assert internal_info["name"] in element.text, internal_info["name"] + "is not displayed in user list"


@then("user is not assignee on case list")
def user_is_not_on_case_list(driver, context):
    assert "No users assigned" in CaseListPage(driver).get_text_of_assignees(
        driver, context.case_id
    ), "No users assigned text is not displayed"


@when("I click select all cases checkbox")
def select_all_cases(driver):
    CaseListPage(driver).click_select_all_checkbox()


@when("I search for SSO users name to assign")
def filter_search_for_assign_users(driver, internal_info):
    CaseListPage(driver).enter_name_to_filter_search_box(internal_info["name"])


@then(parsers.parse('assign users button is "{enabled_disabled}"'))
def assign_user_to_case(driver, enabled_disabled):
    if enabled_disabled == "enabled":
        assert (
            "disabled" not in CaseListPage(driver).get_class_name_of_assign_users_button()
        ), "assign users button is not enabled"
    elif enabled_disabled == "disabled":
        assert (
            "disabled" in CaseListPage(driver).get_class_name_of_assign_users_button()
        ), "assign users button is not disabled"


@when("I click on the added queue in dropdown")  # noqa
def system_queue_shown_in_dropdown(driver, context):
    CaseListPage(driver).click_on_queue_name(context.queue_name)


@when("filter by test user email to assign a user")
def filter_gov_users_found(driver, internal_info):
    assign_user_page = AssignUserPage(driver)
    assign_user_page.search(internal_info["email"])


@when("filter by queue name")
def filter_gov_users_found(driver, internal_info):
    assign_user_page = AssignUserPage(driver)
    assign_user_page.search("queue")


@then("I should see one user with the test user name")
def one_user_found(driver, internal_info):
    assign_user_page = AssignUserPage(driver)
    emails = assign_user_page.get_users_email()
    assert len(emails) > 0
    for email in emails:
        assert internal_info["email"] in email.text


@when("I click the user and click continue")
def click_user_and_assign(driver):
    assign_user_page = AssignUserPage(driver)
    assign_user_page.select_first_radio_button()
    functions.click_submit(driver)


@when("I click the queue and click continue")
def click_user_and_assign(driver):
    assign_user_page = AssignUserPage(driver)
    assign_user_page.select_first_radio_button()
    functions.click_submit(driver)


@given("a new queue has been created")
def create_queue(context, api_client_config):
    lite_client = get_lite_client(context, api_client_config)
    lite_client.queues.add_queue("queue" + get_formatted_date_time_m_d_h_s())
    context.queue_name = lite_client.context["queue_name"]


@then("I see a user is assigned")
def case_officer_is_set(driver, internal_info):
    assert internal_info["name"] in AssignUserPage(driver).get_assigned_user()


@when("I click assign user Button")  # noqa
def i_click_assign_user_button(driver):
    application_page = ApplicationPage(driver)
    application_page.click_assign_user_button()
