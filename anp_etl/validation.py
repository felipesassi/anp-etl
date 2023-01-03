from ruamel import yaml
import great_expectations as gx
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import DataContextConfig, FilesystemStoreBackendDefaults
from anp_etl.expectations import *


spark = gx.core.util.get_or_create_spark_application()


def configure_great_expectations_sources(run_test=False):

    data_source_config = {
        "name": "anp_bronze_data_validation",
        "class_name": "Datasource",
        "execution_engine": {"class_name": "SparkDFExecutionEngine"},
        "data_connectors": {
            "default_runtime_data_connector_name": {
                "class_name": "RuntimeDataConnector",
                "batch_identifiers": ["batch_id"],
            }
        },
    }

    store_backend_defaults = FilesystemStoreBackendDefaults(root_directory="$PWD/validation/")

    data_docs_config={
        "ANP": {
            "class_name": "SiteBuilder",
            "show_how_to_buttons": "false",
            "store_backend": {
                "class_name": "TupleFilesystemStoreBackend",
                "base_directory": "$PWD/validation/data_docs/local_site/"
                }
            }
        }

    data_context_config = DataContextConfig(
        store_backend_defaults=store_backend_defaults,
        checkpoint_store_name=store_backend_defaults.checkpoint_store_name,
        data_docs_sites=data_docs_config
    )

    context = BaseDataContext(project_config=data_context_config)

    if run_test:

        context.test_yaml_config(yaml.dump(data_source_config))

    context.add_datasource(**data_source_config)

    return context


def get_expectation_suite(context):

    return context.create_expectation_suite(expectation_suite_name="anp_bronze_data_suite", overwrite_existing=True)


def add_expectations_to_context(context):

    suite = get_expectation_suite(context)

    expectation_to_check_categorical_cols_values(suite)

    expectation_to_check_null_values(suite)

    expectation_to_check_table_rows(suite)

    expectation_to_check_columns_order(suite)

    context.save_expectation_suite(suite, "anp_bronze_data_suite", overwrite_existing=True)


def add_checkpoint_to_context(context):

    checkpoint_config = {
        "name": "anp_bronze_data_checkpoint",
        "config_version": 1,
        "class_name": "SimpleCheckpoint",
        "expectation_suite_name": "anp_bronze_data_suite",
    }

    context.add_checkpoint(**checkpoint_config)

    return context


def configure_great_expectations():

    context = configure_great_expectations_sources()

    add_expectations_to_context(context)

    return add_checkpoint_to_context(context)


def get_batch_request(df, data_asset_name):

    return RuntimeBatchRequest(
        datasource_name="anp_bronze_data_validation",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name=data_asset_name,  
        batch_identifiers={"batch_id": "default_identifier"},
        runtime_parameters={"batch_data": df}, 
    )


def run_great_expectations_checkpoint(context, batch_request):

    return context.run_checkpoint(
        checkpoint_name="anp_bronze_data_checkpoint",
        validations=[
            {"batch_request": batch_request},
        ],
    )