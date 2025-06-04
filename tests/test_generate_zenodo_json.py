import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
import json
import tempfile
import pytest
from src.utils import generate_zenodo_json

def test_template_csv_creation(tmp_path, monkeypatch):
    import pathlib
    csv_path = tmp_path / "input.csv"
    output_path = tmp_path / "out.json"
    # Remove file if exists
    if os.path.exists(csv_path):
        os.remove(csv_path)
    monkeypatch.chdir(tmp_path)
    # Use absolute path to the script
    script_path = str(pathlib.Path(__file__).parent.parent / "src" / "utils" / "generate_zenodo_json.py")
    import subprocess
    result = subprocess.run([sys.executable, script_path, '--template'], capture_output=True)
    assert result.returncode == 0
    assert os.path.exists(csv_path)
    with open(csv_path, 'r', encoding='utf-8') as f:
        header = f.readline()
        assert 'field' in header and 'value' in header

def test_json_generation_from_csv(tmp_path):
    csv_path = tmp_path / "input.csv"
    output_path = tmp_path / "out.json"
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("field,value\n")
        f.write("title,Test Project\n")
        f.write("keywords,FAIR;RDM\n")
        f.write("communities,community1;community2\n")
        f.write("creators,Name1|Aff1;Name2|Aff2\n")
    generate_zenodo_json.csv_to_zenodo_json(str(csv_path), str(output_path))
    with open(output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data['title'] == 'Test Project'
    assert data['keywords'] == ['FAIR', 'RDM']
    assert data['communities'] == [{"identifier": "community1"}, {"identifier": "community2"}]
    assert data['creators'] == [
        {"name": "Name1", "affiliation": "Aff1"},
        {"name": "Name2", "affiliation": "Aff2"}
    ]
