import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import tempfile
import pytest
from src.utils.csv_to_ge_suite import build_expectations_from_csv

def test_build_expectations_from_csv(tmp_path):
    """Test that build_expectations_from_csv parses the CSV and produces the correct expectations."""
    csv_path = tmp_path / "data_dictionary.csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("Variable Name,Data Type,Allowed Values / Range,Constraints / Validation Rules\n")
        f.write("id,integer,,unique\n")
        f.write("value,string,\"A,B\",\n")

    expectations = build_expectations_from_csv(str(csv_path))
    expected = [
        {'expectation_type': 'expect_column_to_exist', 'kwargs': {'column': 'id'}},
        {'expectation_type': 'expect_column_values_to_be_of_type', 'kwargs': {'column': 'id', 'type_': 'int'}},
        {'expectation_type': 'expect_column_values_to_be_unique', 'kwargs': {'column': 'id'}},
        {'expectation_type': 'expect_column_to_exist', 'kwargs': {'column': 'value'}},
        {'expectation_type': 'expect_column_values_to_be_of_type', 'kwargs': {'column': 'value', 'type_': 'str'}},
        {'expectation_type': 'expect_column_values_to_be_in_set', 'kwargs': {'column': 'value', 'value_set': ['A', 'B']}}
    ]
    # The order of expectations may differ, so compare as sets
    def norm(e):
        def make_hashable(val):
            if isinstance(val, list):
                return tuple(val)
            return val
        return (
            e['expectation_type'],
            tuple(sorted((k, make_hashable(v)) for k, v in e['kwargs'].items()))
        )
    assert set(map(norm, expectations)) == set(map(norm, expected))
