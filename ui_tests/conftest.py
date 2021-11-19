import os
from collections import OrderedDict

import tests_common.tools.helpers as utils


STEP_THROUGH = False  # Gives a prompt for every step in the terminal
STEP_VERBOSE = False  # Print steps as they happen
SCENARIO_HISTORY = OrderedDict()
FEATURE_DIVIDER_LEN = 70


def print_scenario_history(entry):
    scenario = entry["scenario"]
    steps = entry["steps"]
    print("*******************************************\n")
    print(f"FEATURE:  {scenario.feature.description}\n")
    print(f"SCENARIO: {scenario.name}\n")
    for step in steps:
        print(f"\t{step.keyword.upper()} {step.name}")
    print("\n*******************************************")


def print_scenario_history_last_entry():
    print_scenario_history(list(SCENARIO_HISTORY.values())[-1])


def pytest_bdd_before_step_call(request, feature, scenario, step, step_func, step_func_args):
    """
    Runs before each step
    """
    if feature not in SCENARIO_HISTORY:
        if STEP_VERBOSE or STEP_THROUGH:
            print()
            print("*"*FEATURE_DIVIDER_LEN)
            print()
            print(f"FEATURE: {scenario.feature.description}")
        SCENARIO_HISTORY[feature] = {}

    if scenario not in SCENARIO_HISTORY[feature]:
        if STEP_VERBOSE or STEP_THROUGH:
            print()
            print(f"SCENARIO: {scenario.name}")
            print(f"STEPS:\n")
        SCENARIO_HISTORY[feature][scenario] = {}

    if STEP_VERBOSE or STEP_THROUGH:
        print(f"\t {step.keyword.upper()} {step.name}")

    try:
        # TODO: Add feature, scenario, steps
        SCENARIO_HISTORY[feature][scenario]["steps"].append(step)
    except KeyError:
        SCENARIO_HISTORY[feature][scenario] = {
            "steps": [step],
            "scenario": scenario,
            "feature": feature,
        }

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
    env = str(os.environ.get("ENVIRONMENT"))
    if env == "None":
        env = "dev"
    parser.addoption("--headless", action="store_true", default=False)
    parser.addoption(
        "--step-through", action="store_true", default=STEP_THROUGH, help="Allow stepping through each scenario step"
    )
    parser.addoption(
        "--step-verbose", action="store_true", default=STEP_VERBOSE, help="Print each step before executing it"
    )
    if env == "local":
        parser.addoption(
            "--exporter_url", action="store", default=f"http://localhost:{str(os.environ.get('PORT'))}/", help="url"
        )
        parser.addoption(
            "--internal_url", action="store", default="http://localhost:" + str(os.environ.get("PORT")), help="url"
        )
        lite_api_url = os.environ.get("LOCAL_LITE_API_URL", os.environ.get("LITE_API_URL"),)
        parser.addoption(
            "--lite_api_url", action="store", default=lite_api_url, help="url",
        )
    else:
        parser.addoption(
            "--exporter_url",
            action="store",
            default=f"https://exporter.lite.service.{env}.uktrade.digital/",
            help="url",
        )
        parser.addoption(
            "--internal_url",
            action="store",
            default="https://internal.lite.service." + env + ".uktrade.digital/",
            help="url",
        )
        parser.addoption(
            "--lite_api_url", action="store", default=f"https://lite-api-{env}.london.cloudapps.digital/", help="url",
        )
    parser.addoption("--sso_sign_in_url", action="store", default="https://sso.trade.uat.uktrade.io/login/", help="url")


def pytest_exception_interact(node, report):
    if node and report.failed and hasattr(node, "funcargs"):
        driver = node.funcargs.get("driver")
        if driver:
            utils.save_screenshot(driver=driver, name=node.name)
