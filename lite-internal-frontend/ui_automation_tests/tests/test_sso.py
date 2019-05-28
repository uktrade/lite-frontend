from pages.login_page import LoginPage
import unittest
import datetime
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pages.dit_hub_page import DepartmentOfInternationalTradeHub
from pages.exporter_hub import ExporterHub
from pages.login_page import LoginPage
import helpers.helpers as utils
import logging
import random

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)

def test_invalid_user(driver, sign_in_url, internal_url, invalid_username):
    driver.get(sign_in_url)
    login_page = LoginPage(driver)
    login_page.type_into_login_field(invalid_username+str(random.randint(1, 1001)))
    login_page.type_into_password_field("password")
    login_page.click_on_submit_button()
    driver.get(internal_url)
    assert "You need to sign in" in login_page.get_text_of_gov_login_message()

def test_empty_user(driver, sign_in_url, internal_url):
    driver.get(sign_in_url)
    login_page = LoginPage(driver)
    login_page.click_on_submit_button()
    driver.get(internal_url)
    assert "You need to sign in" in login_page.get_text_of_gov_login_message()


def test_teardown(driver):
    driver.quit()
