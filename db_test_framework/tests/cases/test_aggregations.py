from pyspark.sql.functions import sum, avg, max, min, countDistinct
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


@pytest.fixture(scope="function", autouse=False)
def test_data_df(request):
    """
    Expected aggregations values. Pretending that it was fetched from source DB.
    These values from actual result right now.
    """
    return {
        "Age": {
            "sum": 6686758,
            "avg": 25.556898357297374,
            "max": 97,
            "min": 10,
            "distinct_count": 74,
        },
        "Height": {
            "sum": 36986879,
            "avg": 175.33896987366376,
            "max": 226,
            "min": 127,
            "distinct_count": 95,
        },
        "Weight": {
            "sum": 14644004,
            "avg": 70.68149413803256,
            "max": 214,
            "min": 25,
            "distinct_count": 142,
        },
    }


@pytest.fixture(scope="function", autouse=False)
def aggregations_data_df(df_factory, df):
    """Actual aggregations values."""
    result = {}
    for column in df_factory.numeric_columns:
        result[column] = df.agg(
            sum(column).alias("sum"),
            avg(column).alias("avg"),
            max(column).alias("max"),
            min(column).alias("min"),
            countDistinct(column).alias(f"distinct_count")
        ).collect()
    return result


class TestAggregations:
    """Different types of aggregations checks."""

    @pytest.mark.parametrize("aggregations_data, test_data",
                             [[table, table] for table in AGG_SCHEMAS_TABLES_NAMES],
                             indirect=True)
    @pytest.mark.skip(reason="DB connection to MS SQL Server not implemented yet.")
    def test_aggregations(self, test_data, aggregations_data):
        """Verify that aggregations values from source DB equals target DB."""
        for column, aggregations in test_data.items():
            equal(aggregations, aggregations_data[column], f"Aggregations data not equals at column: {column}")

    @pytest.mark.DataFrames
    def test_aggregations_df(self, test_data_df, aggregations_data_df):
        for column, aggregations in test_data_df.items():
            actual_aggregations = dict(aggregations_data_df[column][0].asDict())

            for agg_type, value in aggregations.items():
                equal(value, actual_aggregations[agg_type], msg="Discrepancy between aggregation values.")
