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


class TestTablesDataSchema:
    """Metadata checks."""

    def test_data_schema(self, test_data, tables_schema):
        """Verify that tables schema is correct."""
        for key, value in tables_schema.items():
            equal(test_data[key], value, f"Actual table schema is not correct for table: {key}")
