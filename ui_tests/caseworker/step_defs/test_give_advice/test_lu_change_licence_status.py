from pytest_bdd import scenarios
from pytest_bdd import scenarios, when


from ui_tests.caseworker.pages.users_page import UsersPage

scenarios("../../features/give_advice/lu_licence_change_status.feature", strict_gherkin=False)


@when("I go to edit user role")
def edit_user(driver, context):
    import pdb

    pdb.set_trace()
    user_page = UsersPage(driver)
    user_page.go_to_user_page(context)
    user_page.click_change_email_link()


# @when("I edit my role LU")
# def edit_existing_role(driver, context):
#     # This code needs to edit the user role not edit the details of the role
#     return
