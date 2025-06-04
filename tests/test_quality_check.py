import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import tempfile
import pytest
from src.checks import quality_check

def create_data_and_dictionary(tmp_path, csv_columns, csv_rows, dict_columns):
    import csv
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    csv_path = data_dir / "sample.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        writer.writeheader()
        for row in csv_rows:
            writer.writerow(row)
    docs_dir = tmp_path / "docs" / "data_dictionaries"
    docs_dir.mkdir(parents=True)
    dict_path = docs_dir / "data_dictionary.json"
    dictionary = {
        "sample.csv": {
            "path": str(csv_path),
            "columns": dict_columns
        }
    }
    with open(dict_path, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f)
    return data_dir, dict_path

def test_missing_and_extra_columns(tmp_path):
    csv_columns = ["id", "value"]
    csv_rows = [{"id": "1", "value": "A"}]
    dict_columns = [
        {"Variable Name": "id", "Data Type": "integer"},
        {"Variable Name": "value", "Data Type": "string"},
        {"Variable Name": "extra", "Data Type": "string"}
    ]
    data_dir, dict_path = create_data_and_dictionary(tmp_path, csv_columns, csv_rows, dict_columns)
    report = quality_check.quality_check_tabular_data(str(data_dir), str(dict_path))
    assert "sample.csv" in report
    # Now, missing_in_data should be true (dict has 'extra', CSV does not)
    assert any("Missing columns" in issue for issue in report["sample.csv"].get("file_issues", []))
    # No extra columns in data, so this should be False
    assert not any("Extra columns" in issue for issue in report["sample.csv"].get("file_issues", []))

def test_type_validation(tmp_path):
    csv_columns = ["id", "value"]
    csv_rows = [{"id": "foo", "value": "A"}]
    dict_columns = [
        {"Variable Name": "id", "Data Type": "integer"},
        {"Variable Name": "value", "Data Type": "string"}
    ]
    data_dir, dict_path = create_data_and_dictionary(tmp_path, csv_columns, csv_rows, dict_columns)
    report = quality_check.quality_check_tabular_data(str(data_dir), str(dict_path))
    col_issues = report["sample.csv"]["column_issues"]
    assert "id" in col_issues
    assert any("Type errors" in msg for msg in col_issues["id"])

def test_allowed_values(tmp_path):
    csv_columns = ["id"]
    # First, test with an invalid value
    csv_rows = [{"id": "A"}, {"id": "C"}]  # 'C' is not allowed
    dict_columns = [
        {"Variable Name": "id", "Allowed Values / Range": "A,B"}
    ]
    data_dir, dict_path = create_data_and_dictionary(tmp_path, csv_columns, csv_rows, dict_columns)
    report = quality_check.quality_check_tabular_data(str(data_dir), str(dict_path))
    assert "sample.csv" in report
    col_issues = report["sample.csv"].get("column_issues", {})
    assert "id" in col_issues
    assert any("Invalid value" in issue for issue in col_issues["id"])

def test_allowed_values_valid(tmp_path):
    csv_columns = ["id"]
    csv_rows = [{"id": "A"}, {"id": "B"}]
    dict_columns = [
        {"Variable Name": "id", "Allowed Values / Range": "A,B"}
    ]
    data_dir, dict_path = create_data_and_dictionary(tmp_path, csv_columns, csv_rows, dict_columns)
    report = quality_check.quality_check_tabular_data(str(data_dir), str(dict_path))
    col_issues = report["sample.csv"].get("column_issues", {})
    assert "id" not in col_issues or not col_issues["id"]

def test_uniqueness_and_not_null(tmp_path):
    csv_columns = ["id"]
    csv_rows = [{"id": "1"}, {"id": "1"}, {"id": ""}]
    dict_columns = [
        {"Variable Name": "id", "Constraints / Validation Rules": "unique, not null"}
    ]
    data_dir, dict_path = create_data_and_dictionary(tmp_path, csv_columns, csv_rows, dict_columns)
    report = quality_check.quality_check_tabular_data(str(data_dir), str(dict_path))
    col_issues = report["sample.csv"]["column_issues"]
    assert "id" in col_issues
    assert any("Duplicate values" in msg for msg in col_issues["id"])
    assert any("Null/missing values" in msg for msg in col_issues["id"])
