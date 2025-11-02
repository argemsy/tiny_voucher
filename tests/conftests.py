# Standard Libraries
import contextlib
import tracemalloc

# Third-party Libraries
import pytest


@pytest.fixture(autouse=True, scope="session")
def __make_unmanaged_managed():
    # Third Party Libraries
    # Third-party Libraries
    from django.apps import apps

    get_models = apps.get_models
    for m in [m for m in get_models() if not m._meta.managed]:
        m._meta.managed = True


def pytest_sessionfinish(session, exitstatus):
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    with contextlib.suppress(Exception):
        failed = reporter.stats.get("failed")
        with open("/src/reports/config.txt", "a") as f:
            f.write(str(len(failed)))


def pytest_configure(config):
    """Configure pytest with tracemalloc enabled."""
    tracemalloc.start()


pytest_plugins: list[str] = [
    # This ensures that all fixtures declared under fixtures/ will be found by
    # pytest, As a note that the respective directories referred to in
    # fixtures.conftest" need to have __init__.py files for the plugins to be
    # loaded by pytest
]
