import pytest
from django.apps import apps
from django.db import connections


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem):
    cleanup_databases()


def cleanup_databases():
    for connection in connections.all():
        for model in apps.get_models():
            model.objects.using(connection.alias).delete()
