import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import tempfile
import shutil
import pytest
from src.checks import generate_data_dictionary

def create_sample_csv(path, columns, rows):
    import csv
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def test_generate_data_dictionary_creates_file_and_preserves_metadata(tmp_path):
    # Setup: create data dir and sample csv
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    csv_path = data_dir / "sample.csv"
    columns = ["id", "value"]
    rows = [
        {"id": "1", "value": "A"},
        {"id": "2", "value": "B"}
    ]
    create_sample_csv(csv_path, columns, rows)
    # Setup: create docs/data_dictionaries dir
    docs_dir = tmp_path / "docs" / "data_dictionaries"
    docs_dir.mkdir(parents=True)
    dict_path = docs_dir / "data_dictionary.json"
    # Setup: create .project_config.json
    config = {"data_directory_name": str(data_dir)}
    config_path = tmp_path / ".project_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f)
    # Setup: pre-existing metadata
    pre_existing = {
        "sample.csv": {
            "path": str(csv_path),
            "columns": [
                {"Variable Name": "id", "Description": "Identifier", "Data Type": "integer"},
                {"Variable Name": "value", "Description": "Old desc", "Data Type": "string"}
            ]
        }
    }
    with open(dict_path, 'w', encoding='utf-8') as f:
        json.dump(pre_existing, f)
    # Patch paths in module
    orig_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        generate_data_dictionary.main()
        # Check output
        with open(dict_path, 'r', encoding='utf-8') as f:
            result = json.load(f)
        assert "sample.csv" in result
        col_meta = result["sample.csv"]["columns"]
        assert any(col["Variable Name"] == "id" and col["Description"] == "Identifier" for col in col_meta)
        assert any(col["Variable Name"] == "value" and col["Description"] == "Old desc" for col in col_meta)
    finally:
        os.chdir(orig_cwd)

def test_generate_data_dictionary_adds_new_columns(tmp_path):
    # Setup: create data dir and sample csv with new column
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    csv_path = data_dir / "sample.csv"
    columns = ["id", "value", "extra"]
    rows = [
        {"id": "1", "value": "A", "extra": "foo"},
        {"id": "2", "value": "B", "extra": "bar"}
    ]
    create_sample_csv(csv_path, columns, rows)
    docs_dir = tmp_path / "docs" / "data_dictionaries"
    docs_dir.mkdir(parents=True)
    dict_path = docs_dir / "data_dictionary.json"
    config = {"data_directory_name": str(data_dir)}
    config_path = tmp_path / ".project_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f)
    # Pre-existing metadata with only two columns
    pre_existing = {
        "sample.csv": {
            "path": str(csv_path),
            "columns": [
                {"Variable Name": "id", "Description": "Identifier", "Data Type": "integer"},
                {"Variable Name": "value", "Description": "Old desc", "Data Type": "string"}
            ]
        }
    }
    with open(dict_path, 'w', encoding='utf-8') as f:
        json.dump(pre_existing, f)
    orig_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        generate_data_dictionary.main()
        with open(dict_path, 'r', encoding='utf-8') as f:
            result = json.load(f)
        col_meta = result["sample.csv"]["columns"]
        # Existing columns preserved
        assert any(col["Variable Name"] == "id" and col["Description"] == "Identifier" for col in col_meta)
        # New column added with empty metadata
        assert any(col["Variable Name"] == "extra" and col["Description"] == "" for col in col_meta)
    finally:
        os.chdir(orig_cwd)

def test_generate_data_dictionary_handles_non_csv(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    txt_path = data_dir / "file.txt"
    txt_path.write_text("hello world")
    docs_dir = tmp_path / "docs" / "data_dictionaries"
    docs_dir.mkdir(parents=True)
    dict_path = docs_dir / "data_dictionary.json"
    config = {"data_directory_name": str(data_dir)}
    config_path = tmp_path / ".project_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f)
    orig_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        generate_data_dictionary.main()
        with open(dict_path, 'r', encoding='utf-8') as f:
            result = json.load(f)
        assert "file.txt" in result
        assert result["file.txt"]["columns"] == []
    finally:
        os.chdir(orig_cwd)
