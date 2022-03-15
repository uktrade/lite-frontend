# flake8: noqa
from playwright_tests.api.login import set_sso_cookie
import os

import pytest
from playwright.sync_api import (
    Error,
    Page,
    sync_playwright,
)
from slugify import slugify

import tempfile


artifacts_folder = tempfile.TemporaryDirectory(prefix="playwright-pytest-")


def _build_artifact_test_folder(pytestconfig, request, folder_or_file_name):
    output_dir = pytestconfig.getoption("--output")
    return os.path.join(output_dir, slugify(request.node.nodeid), folder_or_file_name)


@pytest.fixture(scope="session")
def browser_type_launch_args():
    launch_options = {"headless": False}
    return launch_options


@pytest.fixture(scope="session")
def browser_context_args():
    context_args = {
        "base_url": "https://internal.lite.service.devdata.uktrade.digital/",
    }
    return context_args


@pytest.fixture(scope="session")
def playwright():
    pw = sync_playwright().start()
    yield pw
    pw.stop()


@pytest.fixture(scope="session")
def browser_type(playwright, browser_name):
    return getattr(playwright, browser_name)


@pytest.fixture(scope="session")
def launch_browser(browser_type_launch_args, browser_type):
    def launch(**kwargs):
        launch_options = {**browser_type_launch_args, **kwargs}
        browser = browser_type.launch(**launch_options)
        return browser

    return launch


@pytest.fixture(scope="session")
def browser(launch_browser):
    browser = launch_browser()
    yield browser
    browser.close()
    artifacts_folder.cleanup()


@pytest.fixture
def context(browser, browser_context_args, pytestconfig, request):
    pages = []
    context = browser.new_context(**browser_context_args)
    context.on("page", lambda page: pages.append(page))

    tracing_option = pytestconfig.getoption("--tracing")
    capture_trace = tracing_option in ["on", "retain-on-failure"]
    if capture_trace:
        context.tracing.start(
            name=slugify(request.node.nodeid),
            screenshots=True,
            snapshots=True,
            sources=True,
        )

    yield context

    # If requst.node is missing rep_call, then some error happened during execution
    # that prevented teardown, but should still be counted as a failure
    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else True

    if capture_trace:
        retain_trace = tracing_option == "on" or (failed and tracing_option == "retain-on-failure")
        if retain_trace:
            trace_path = _build_artifact_test_folder(pytestconfig, request, "trace.zip")
            context.tracing.stop(path=trace_path)
        else:
            context.tracing.stop()

    screenshot_option = pytestconfig.getoption("--screenshot")
    capture_screenshot = screenshot_option == "on" or (failed and screenshot_option == "only-on-failure")
    if capture_screenshot:
        for index, page in enumerate(pages):
            human_readable_status = "failed" if failed else "finished"
            screenshot_path = _build_artifact_test_folder(
                pytestconfig, request, f"test-{human_readable_status}-{index+1}.png"
            )
            try:
                page.screenshot(timeout=5000, path=screenshot_path)
            except Error:
                pass

    context.close()

    video_option = pytestconfig.getoption("--video")
    preserve_video = video_option == "on" or (failed and video_option == "retain-on-failure")
    if preserve_video:
        for page in pages:
            video = page.video
            if not video:
                continue
            try:
                video_path = video.path()
                file_name = os.path.basename(video_path)
                video.save_as(path=_build_artifact_test_folder(pytestconfig, request, file_name))
            except Error:
                # Silent catch empty videos.
                pass


@pytest.fixture
def page(context):
    page = context.new_page()
    set_sso_cookie(page)
    yield page


@pytest.fixture(scope="session")
def browser_name():
    return "chromium"


def pytest_addoption(parser):
    group = parser.getgroup("playwright", "Playwright")
    group.addoption(
        "--browser",
        action="append",
        default=[],
        help="Browser engine which should be used",
        choices=["chromium", "firefox", "webkit"],
    )
    group.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run tests in headed mode.",
    )
    group.addoption(
        "--browser-channel",
        action="store",
        default=None,
        help="Browser channel to be used.",
    )
    group.addoption(
        "--slowmo",
        default=0,
        type=int,
        help="Run tests with slow mo",
    )
    group.addoption("--device", default=None, action="store", help="Device to be emulated.")
    group.addoption(
        "--output",
        default="test-results",
        help="Directory for artifacts produced by tests, defaults to test-results.",
    )
    group.addoption(
        "--tracing",
        default="off",
        choices=["on", "off", "retain-on-failure"],
        help="Whether to record a trace for each test.",
    )
    group.addoption(
        "--video",
        default="off",
        choices=["on", "off", "retain-on-failure"],
        help="Whether to record video for each test.",
    )
    group.addoption(
        "--screenshot",
        default="off",
        choices=["on", "off", "only-on-failure"],
        help="Whether to automatically capture a screenshot after each test.",
    )
