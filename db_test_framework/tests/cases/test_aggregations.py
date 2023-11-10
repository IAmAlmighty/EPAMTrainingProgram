from db_test_framework.automation.tables import *
from pytest_check import equal
import pytest


@pytest.fixture(scope="function", autouse=False)
def test_data(request):
    """
    Expected aggregations values. Pretending that it was fetched from source DB.
    These values from actual result right now.
    """
    data = {
        PersonAddress.schema_name: {
            PersonAddress.table_name: {
                "AddressID": (382792340, 19516, 32521, 1, 19614),
                "StateProvinceID": (966669, 49, 181, 1, 74)
            }},
        ProductionDocument.schema_name: {
            ProductionDocument.table_name: {
                "Owner": (2844, 218, 220, 217, 3),
                "ChangeNumber": (462, 35, 288, 0, 9)
            },
            ProductionUnitMeasure.table_name: {}
        },
    }
    schema_name, table_name = request.param[0], request.param[1]

    return data[schema_name][table_name]


@pytest.fixture(scope="function", autouse=False)
def aggregations_data(request, db):
    """Actual aggregations values."""
    schema_name, table_name = request.param[0], request.param[1]

    result = db.get_aggregations_of_numeric(schema_name, table_name)

    return {r[0]: r[1:] for r in result}


class TestAggregations:
    """Different types of aggregations checks."""

    @pytest.mark.parametrize("aggregations_data, test_data",
                             [[table, table] for table in AGG_SCHEMAS_TABLES_NAMES],
                             indirect=True)
    def test_aggregations(self, test_data, aggregations_data):
        """Verify that aggregations values from source DB equals target DB."""
        for column, aggregations in test_data.items():
            equal(aggregations, aggregations_data[column], f"Aggregations data not equals at column: {column}")
