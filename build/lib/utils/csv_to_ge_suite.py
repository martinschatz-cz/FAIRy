import csv
import pandas as pd
import sys
import os
import great_expectations as ge
from great_expectations.data_context import get_context

def build_expectations_from_csv(data_dictionary_csv: str) -> list:
    """
    Reads a data dictionary CSV and returns a list of expectation dicts.
    """
    expectations = []
    df = pd.read_csv(data_dictionary_csv)
    for _, row in df.iterrows():
        col = row['Variable Name']
        dtype = str(row.get('Data Type', '')).lower()
        allowed = str(row.get('Allowed Values / Range', ''))
        constraints = str(row.get('Constraints / Validation Rules', '')).lower()
        # Column exists
        expectations.append({
            "expectation_type": "expect_column_to_exist",
            "kwargs": {"column": col}
        })
        # Data type
        if dtype in ['integer', 'float', 'decimal', 'string', 'boolean', 'date']:
            if dtype == 'integer':
                expectations.append({
                    "expectation_type": "expect_column_values_to_be_of_type",
                    "kwargs": {"column": col, "type_": "int"}
                })
            elif dtype in ['float', 'decimal']:
                expectations.append({
                    "expectation_type": "expect_column_values_to_be_of_type",
                    "kwargs": {"column": col, "type_": "float"}
                })
            elif dtype == 'string':
                expectations.append({
                    "expectation_type": "expect_column_values_to_be_of_type",
                    "kwargs": {"column": col, "type_": "str"}
                })
            elif dtype == 'boolean':
                expectations.append({
                    "expectation_type": "expect_column_values_to_be_in_set",
                    "kwargs": {"column": col, "value_set": ["true", "false", "0", "1", "yes", "no"]}
                })
            elif dtype == 'date':
                pass
        # Allowed values/range
        if allowed and allowed.lower() != 'nan':
            if dtype in ['integer', 'float', 'decimal'] and '-' in allowed:
                try:
                    minv, maxv = allowed.split('-')
                    minv, maxv = float(minv.strip()), float(maxv.strip())
                    expectations.append({
                        "expectation_type": "expect_column_values_to_be_between",
                        "kwargs": {"column": col, "min_value": minv, "max_value": maxv}
                    })
                except Exception:
                    pass
            else:
                allowed_vals = [a.strip() for a in allowed.split(',') if a.strip()]
                if allowed_vals:
                    expectations.append({
                        "expectation_type": "expect_column_values_to_be_in_set",
                        "kwargs": {"column": col, "value_set": allowed_vals}
                    })
        # Constraints
        if 'unique' in constraints:
            expectations.append({
                "expectation_type": "expect_column_values_to_be_unique",
                "kwargs": {"column": col}
            })
        if 'not null' in constraints or 'cannot be null' in constraints:
            expectations.append({
                "expectation_type": "expect_column_values_to_not_be_null",
                "kwargs": {"column": col}
            })
    return expectations

def csv_data_dictionary_to_ge_suite(
    data_dictionary_csv: str,
    data_file: str,
    suite_name: str = "data_dictionary_suite"
) -> None:
    """
    Reads a data dictionary CSV and creates a Great Expectations suite for the given data file.
    """
    # Read the data dictionary CSV
    expectations = build_expectations_from_csv(data_dictionary_csv)
    # Create GE context and suite
    context = get_context()
    from great_expectations.core.batch import RuntimeBatchRequest
    batch_request = RuntimeBatchRequest(
        datasource_name="default_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name=os.path.basename(data_file),
        runtime_parameters={"path": os.path.abspath(data_file)},
        batch_identifiers={"default_identifier_name": "default_identifier"},
    )
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name,
        create_expectation_suite_if_not_exists=True
    )
    for exp in expectations:
        getattr(validator, exp["expectation_type"])(**exp["kwargs"])
    validator.save_expectation_suite(discard_failed_expectations=False)
    print(f"Great Expectations suite '{suite_name}' created for {data_file}.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_ge_suite.py <data_dictionary.csv> <data_file.csv>")
        sys.exit(1)
    csv_data_dictionary_to_ge_suite(sys.argv[1], sys.argv[2])
