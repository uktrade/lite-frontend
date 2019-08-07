from pytest_bdd import scenarios, given, when, then, parsers
from pages.add_goods_page import AddGoodPage
from pages.case_list_page import CaseListPage
import helpers.helpers as utils

scenarios('../features/add_goods.feature', strict_gherkin=False)


@when('I click add a good button')
def click_add_from_organisation_button(driver):
    add_goods_page = AddGoodPage(driver)
    add_goods_page.click_add_a_good()
