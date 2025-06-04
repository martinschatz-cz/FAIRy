import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import tempfile
import pytest
from src.utils import regex_builder

def test_load_regex_from_config(tmp_path):
    config = {"data_naming_convention_regex": r"^test_.*\\.csv$"}
    config_path = tmp_path / ".project_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f)
    orig_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        loaded = regex_builder.load_config(str(config_path))
        assert loaded["data_naming_convention_regex"] == r"^test_.*\\.csv$"
    finally:
        os.chdir(orig_cwd)

def test_regex_valid_filename():
    regex = r"^test_.*\.csv$"
    assert regex_builder.re.match(regex, "test_file.csv")
    assert not regex_builder.re.match(regex, "other_file.csv")

def test_explain_regex():
    regex = r"^test_.*\\.csv$"
    explanation = regex_builder.explain_regex(regex)
    assert "test_" in explanation
    assert ".csv" in explanation

# Saving updated regex would require a refactor to make regex_builder.py more testable (e.g., inject config path)
# This is a placeholder for future extension.
