import os
from pathlib import Path
import pytest

import tests_common.tools.helpers as utils

from environ import Env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_FILE = os.path.join(BASE_DIR, ".env")
if os.path.exists(ENV_FILE):
    Env.read_env(ENV_FILE)

environ = Env()

STEP_THROUGH = False  # Gives a prompt for every step in the terminal
STEP_VERBOSE = STEP_THROUGH  # Shows info as a banner for every step


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    step.name = f"[FAILED] {step.name}"


def pytest_bdd_before_step_call(request, feature, scenario, step, step_func, step_func_args):
    """
    Runs before each step
    """
    if STEP_VERBOSE:
        print("*******************************************")
        print(f"SCENARIO: {scenario.feature.description}")
        print(f"STEP: .. {step.keyword} {step.name}")
        print("*******************************************")
    if STEP_THROUGH:
        import IPython

        IPython.embed(using=False)


def pytest_configure(config):
    if config.option.step_through:
        global STEP_THROUGH  # pylint: disable=global-statement
        STEP_THROUGH = config.option.step_through
    if config.option.step_verbose:
        global STEP_VERBOSE  # pylint: disable=global-statement
        STEP_VERBOSE = config.option.step_verbose


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False)
    parser.addoption(
        "--chrome-binary-location", action="store", default="", help="Custom chrome binary path for selenium to use"
    )
    parser.addoption(
        "--step-through", action="store_true", default=STEP_THROUGH, help="Allow stepping through each scenario step"
    )
    parser.addoption(
        "--step-verbose", action="store_true", default=STEP_VERBOSE, help="Gives extra info for every step"
    )
    parser.addoption("--exporter_url", action="store", default=f"http://exporter:8300/", help="url")
    parser.addoption("--internal_url", action="store", default="http://caseworker:8200/", help="url")
    lite_api_url = os.environ.get(
        "LOCAL_LITE_API_URL",
        os.environ.get("LITE_API_URL"),
    )
    parser.addoption(
        "--lite_api_url",
        action="store",
        default=lite_api_url,
        help="url",
    )
    parser.addoption("--sso_sign_in_url", action="store", default="https://sso.trade.uat.uktrade.io/login/", help="url")


def pytest_exception_interact(node, report):
    if node and report.failed and hasattr(node, "funcargs"):
        driver = node.funcargs.get("driver")
        if driver:
            utils.save_screenshot(driver=driver, name=node.name)


@pytest.fixture()
def tmp_download_path():
    download_path = Path("/tmp/downloads/")
    download_path.mkdir(exist_ok=True)
    return download_path
