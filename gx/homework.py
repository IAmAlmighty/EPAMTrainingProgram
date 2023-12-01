from great_expectations.data_context.types.resource_identifiers import ExpectationSuiteIdentifier
from great_expectations.checkpoint import Checkpoint
import great_expectations as gx

asset_name = "my_asset"
expectation_suite_name = "my_suite"
checkpoint_name = "my_sql_checkpoint"
context = gx.get_context()
datasource = context.get_datasource("my_datasource")


def init_datasource():
    user_name = "Sobaqa"
    password = "12345"
    address = "localhost"
    port = "1433"
    connection_string = f"mssql+pyodbc://{user_name}:{password}@{address}:{port}/AdventureWorks2012?driver=SQL Server&charset=utf&autocommit=true"
    context.sources.add_sql(
        name="my_datasource", connection_string=connection_string
    )


def init_default_suite():
    suite = context.add_expectation_suite(expectation_suite_name=expectation_suite_name)
    context.add_or_update_expectation_suite(expectation_suite=suite)

    suite_identifier = ExpectationSuiteIdentifier(expectation_suite_name=expectation_suite_name)
    context.build_data_docs(resource_identifiers=[suite_identifier])
    context.open_data_docs(resource_identifier=suite_identifier)


def init_default_asset():
    datasource.add_table_asset(name="my_asset", schema_name="Production", table_name="Product")


def init_default_expectations():
    batch_request = datasource.get_asset(asset_name).build_batch_request()

    context.add_or_update_expectation_suite(expectation_suite_name=expectation_suite_name)
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=expectation_suite_name,
    )
    validator.expect_column_values_to_not_be_null(column="Name")
    validator.expect_column_values_to_not_be_null(column="SafetyStockLevel")
    validator.expect_column_values_to_not_be_null(column="ProductNumber")
    validator.expect_column_values_to_not_be_null(column="ReorderPoint")
    validator.expect_column_values_to_be_between(
        column="SafetyStockLevel", min_value=4, max_value=1000
    )
    validator.expect_column_value_lengths_to_be_between(
        column="ProductNumber", min_value=7, max_value=10
    )
    validator.expect_column_values_to_match_like_pattern(
        column="ProductNumber", like_pattern="%-%"
    )
    validator.expect_column_distinct_values_to_equal_set(
        column="MakeFlag", value_set={0, 1}
    )
    validator.expect_table_row_count_to_equal(value=504)
    validator.save_expectation_suite(discard_failed_expectations=False)


def init_default_checkpoint():
    batch_request = datasource.get_asset(asset_name).build_batch_request()

    checkpoint = Checkpoint(
        name=checkpoint_name,
        run_name_template="%Y%m%d-%H%M%S-my-run-name-template",
        data_context=context,
        batch_request=batch_request,
        expectation_suite_name=expectation_suite_name,
        action_list=[
            {
                "name": "store_validation_result",
                "action": {"class_name": "StoreValidationResultAction"},
            },
            {"name": "update_data_docs", "action": {"class_name": "UpdateDataDocsAction"}},
        ],
    )
    context.add_or_update_checkpoint(checkpoint=checkpoint)


if __name__ == "__main__":
    checkpoint = context.get_checkpoint(checkpoint_name)
    checkpoint_result = checkpoint.run()

    context.open_data_docs()
