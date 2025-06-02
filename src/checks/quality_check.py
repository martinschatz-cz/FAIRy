import json
import os
import csv
from typing import Dict, List, Any, Set

def quality_check_tabular_data(data_dir: str, data_dictionary_path: str) -> Dict[str, Any]:
    """
    Checks tabular data files in data_dir against the data dictionary.
    Returns a report dict with file-level and column-level issues.
    """
    report: Dict[str, Any] = {}
    # Load data dictionary
    with open(data_dictionary_path, 'r', encoding='utf-8') as f:
        data_dict = json.load(f)
    for fname, meta in data_dict.items():
        file_path = meta.get('path', '')
        columns_meta = meta.get('columns', [])
        if not file_path or not columns_meta or not os.path.exists(file_path):
            report[fname] = {'error': 'File missing or no columns defined in data dictionary.'}
            continue
        # Read data
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data_rows = list(reader)
        file_issues: List[str] = []
        # Check for missing columns
        data_columns = set(reader.fieldnames or [])
        dict_columns = set(col['Variable Name'] for col in columns_meta)
        missing_in_data = dict_columns - data_columns
        extra_in_data = data_columns - dict_columns
        if missing_in_data:
            file_issues.append(f"Missing columns in data: {sorted(list(missing_in_data))}")
        if extra_in_data:
            file_issues.append(f"Extra columns in data: {sorted(list(extra_in_data))}")
        # Per-column checks
        col_issues: Dict[str, List[str]] = {}
        for col_meta in columns_meta:
            col = col_meta['Variable Name']
            if col not in data_columns:
                continue
            values = [row.get(col, None) for row in data_rows]
            # Data Type check (basic)
            dtype = col_meta.get('Data Type', '').lower()
            if dtype:
                type_errors: List[str] = []
                for v in values:
                    if v in (None, '', col_meta.get('Missing Value Representation', '')):
                        continue
                    if dtype == 'integer':
                        try:
                            int(v)
                        except Exception:
                            type_errors.append(str(v))
                    elif dtype == 'float' or dtype == 'decimal':
                        try:
                            float(v)
                        except Exception:
                            type_errors.append(str(v))
                    elif dtype == 'boolean':
                        if str(v).lower() not in ['true', 'false', '0', '1', 'yes', 'no']:
                            type_errors.append(str(v))
                    elif dtype == 'date':
                        from datetime import datetime
                        try:
                            datetime.fromisoformat(v)
                        except Exception:
                            type_errors.append(str(v))
                if type_errors:
                    col_issues[col] = col_issues.get(col, []) + [f"Type errors: {type_errors}"]
            # Allowed Values / Range check
            allowed = col_meta.get('Allowed Values / Range', '')
            if allowed:
                if dtype in ['integer', 'float', 'decimal'] and '-' in allowed:
                    try:
                        minv, maxv = allowed.split('-')
                        minv, maxv = float(minv.strip()), float(maxv.strip())
                        for v in values:
                            if v in (None, '', col_meta.get('Missing Value Representation', '')):
                                continue
                            try:
                                fv = float(v)
                                if fv < minv or fv > maxv:
                                    col_issues[col] = col_issues.get(col, []) + [f"Out of range: {v}"]
                            except Exception:
                                continue
                    except Exception:
                        pass
                else:
                    allowed_vals = [a.strip() for a in allowed.split(',') if a.strip()]
                    if allowed_vals:
                        for v in values:
                            if v in (None, '', col_meta.get('Missing Value Representation', '')):
                                continue
                            if v not in allowed_vals:
                                col_issues[col] = col_issues.get(col, []) + [f"Invalid value: {v}"]
            # Constraints / Validation Rules (basic: unique, not null)
            constraints = col_meta.get('Constraints / Validation Rules', '').lower()
            if 'unique' in constraints:
                seen: Set[str] = set()
                dups: Set[str] = set()
                for v in values:
                    if v in seen:
                        dups.add(str(v))
                    else:
                        seen.add(str(v))
                if dups:
                    col_issues[col] = col_issues.get(col, []) + [f"Duplicate values: {sorted(list(dups))}"]
            if 'not null' in constraints or 'cannot be null' in constraints:
                nulls = [i for i, v in enumerate(values) if v in (None, '', col_meta.get('Missing Value Representation', ''))]
                if nulls:
                    col_issues[col] = col_issues.get(col, []) + [f"Null/missing values at rows: {nulls}"]
        if file_issues or col_issues:
            report[fname] = {'file_issues': file_issues, 'column_issues': col_issues}
    return report

if __name__ == '__main__':
    # Example usage:
    # report = quality_check_tabular_data('data', 'docs/data_dictionaries/data_dictionary.json')
    # print(json.dumps(report, indent=2))
    pass
