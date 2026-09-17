from __future__ import annotations

import base64
import hashlib
import mimetypes
import os
from pathlib import Path

import pytest
from slugify import slugify

from pages.register_page import RegisterPage
from test_data.personal_details import DEFAULT_PERSONAL_DETAILS
from utils.random_data import random_password
from utils.random_data import random_username

MAX_EMBEDDED_BYTES = 3 * 1024 * 1024

@pytest.fixture
def registered_user(page, base_url):
    username = random_username()
    password = random_password()

    user = {
        "username": username,
        "password": password,
    }

    page.goto(base_url)

    register_page = RegisterPage(page)

    register_page.register(
        personal_details=DEFAULT_PERSONAL_DETAILS,
        user=user,
    )

    register_page.expect_registration_success()

    return {
        "page": page,
        "username": username,
        "password": password,
    }


def _truncate_file_name(file_name: str) -> str:
    if len(file_name) < 256:
        return file_name
    return (
        f"{file_name[:100]}"
        f"-{hashlib.sha256(file_name.encode()).hexdigest()[:7]}"
        f"-{file_name[-100:]}"
    )


def _artifact_dir(item: pytest.Item) -> Path:
    output_dir = item.config.getoption("--output", default="test-results")
    return Path(output_dir) / _truncate_file_name(slugify(item.nodeid))


def _build_extras(html_plugin, directory: Path) -> list:
    extras = []

    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue

        mime_type, _ = mimetypes.guess_type(path.name)
        is_image = (mime_type or "").startswith("image/")
        size = path.stat().st_size

        if is_image and size <= MAX_EMBEDDED_BYTES:
            extras.append(
                html_plugin.extras.image(
                    base64.b64encode(path.read_bytes()).decode("ascii"),
                    name=path.name,
                    mime_type=mime_type or "image/png",
                    extension=path.suffix.lstrip(".") or "png",
                )
            )
        else:
            extras.append(html_plugin.extras.url(path.as_posix(), name=path.name))

    return extras


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield

    setattr(item, f"rep_{report.when}", report)

    if report.when != "teardown":
        return report

    html_plugin = item.config.pluginmanager.getplugin("html")
    if html_plugin is None:
        return report

    directory = _artifact_dir(item)
    if not directory.is_dir():
        return report

    try:
        extras = _build_extras(html_plugin, directory)
    except OSError:
        return report

    if extras:
        report.extras = list(getattr(report, "extras", [])) + extras

    return report


def pytest_report_header(config):
    return [
        f"artifacts: output={config.getoption('--output')} "
        f"screenshot={config.getoption('--screenshot')} "
        f"tracing={config.getoption('--tracing')} "
        f"video={config.getoption('--video')}",
        f"CI: {bool(os.getenv('CI'))}",
    ]
