from db_test_framework.automation.db import DB
import pytest


@pytest.fixture(scope="session", autouse=False)
def db(request):
    yield DB()
