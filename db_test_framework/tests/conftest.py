from db_test_framework.automation.df import DataFrameFactory
from db_test_framework.automation.db import DB
import pytest


@pytest.fixture(scope="session", autouse=False)
def db(request):
    return DB()


@pytest.fixture(scope="session", autouse=False)
def df_factory():
    return DataFrameFactory()


@pytest.fixture(scope="session", autouse=False)
def df(df_factory):
    return df_factory.get_df()
