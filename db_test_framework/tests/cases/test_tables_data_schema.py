from db_test_framework.automation.df import DataFrameFactory
from db_test_framework.automation.tables import TABLES
from pytest_check import equal
import pytest


@pytest.fixture(scope="module", autouse=False)
def test_data():
    """Returns expected tables schema details."""
    return {name: cls.schema_details for name, cls in TABLES.items()}


@pytest.fixture(scope="module", autouse=False)
def tables_schema(db):
    """Returns actual tables schema details."""
    result = {}
    for name, klass in TABLES.items():
        result[name] = db.get_table_schema_details(klass.schema_name, klass.table_name)
    return result


@pytest.fixture(scope="module", autouse=False)
def test_data_df():
    """Pretending that this is some verified schema that can be used as expected result."""
    return DataFrameFactory.schema


@pytest.fixture(scope="module", autouse=False)
def data_schema_df(df):
    return df


class TestTablesDataSchema:
    """Metadata checks."""

    @pytest.mark.skip(reason="DB connection to MS SQL Server not implemented yet.")
    def test_data_schema(self, test_data, tables_schema):
        """Verify that tables schema is correct."""
        for key, value in tables_schema.items():
            equal(test_data[key], value, f"Actual table schema is not correct for table: {key}")

    @pytest.mark.DataFrames
    def test_data_schema_df(self, test_data_df, data_schema_df):
        equal(test_data_df, data_schema_df.schema, msg="Schemas are not equal.")
