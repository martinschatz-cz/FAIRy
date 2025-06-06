import json
import os

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    config = load_config(os.environ.get('FAIRY_CONFIG', '.project_config.json'))
    data_dir: str = config['data_directory_name']
    dictionary: dict[str, dict[str, object]] = {}
    # Load existing data dictionary if it exists
    dict_path = os.environ.get('FAIRY_DD_OUT', 'docs/data_dictionaries/data_dictionary.json')
    if os.path.exists(dict_path) and dict_path.endswith('.json'):
        with open(dict_path, 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
    for root, _, files in os.walk(data_dir):
        for fname in files:
            file_path: str = os.path.join(root, fname)
            columns: list[str] = []
            if fname.lower().endswith('.csv'):
                try:
                    import csv
                    with open(file_path, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile)
                        columns = list(reader.fieldnames) if reader.fieldnames else []
                except Exception as e:
                    print(f"Warning: Could not read columns from {fname}: {e}")
            if fname not in dictionary:
                dictionary[fname] = {"path": file_path, "columns": []}
            # Ensure columns is a list
            col_list = dictionary[fname]["columns"]
            if not isinstance(col_list, list):
                col_list = []
            # Build a lookup for existing columns by Variable Name
            existing_cols = {}
            for col in col_list:
                if isinstance(col, dict) and 'Variable Name' in col:
                    existing_cols[col['Variable Name']] = col
            new_col_list = []
            for col in columns:
                if col in existing_cols:
                    new_col_list.append(existing_cols[col])
                else:
                    new_col_list.append({
                        "Variable Name": str(col),
                        "Description": "",
                        "Data Type": "",
                        "Units": "",
                        "Allowed Values / Range": "",
                        "Missing Value Representation": "",
                        "Source": "",
                        "Constraints / Validation Rules": "",
                        "Notes / Comments": "",
                        "Example Value": ""
                    })
            dictionary[fname]["columns"] = new_col_list
            if not columns:
                # Fallback for non-CSV or unreadable files
                dictionary[fname]["columns"] = []
    # Auto-detect output format
    if dict_path.endswith('.csv'):
        # Write as CSV (one row per variable)
        import csv
        rows = []
        for fname, meta in dictionary.items():
            for col in meta["columns"]:
                row = {"Filename": fname, **col}
                rows.append(row)
        if rows:
            fieldnames = list(rows[0].keys())
        else:
            fieldnames = ["Filename", "Variable Name", "Description", "Data Type", "Units", "Allowed Values / Range", "Missing Value Representation", "Source", "Constraints / Validation Rules", "Notes / Comments", "Example Value"]
        with open(dict_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        print(f'Data dictionary generated at {dict_path} (CSV)')
    else:
        with open(dict_path, 'w', encoding='utf-8') as f:
            json.dump(dictionary, f, indent=2)
        print(f'Data dictionary generated at {dict_path} (JSON)')

# quality_check_tabular_data has been moved to src/checks/quality_check.py

if __name__ == '__main__':
    main()
    # Example usage:
    # report = quality_check_tabular_data('data', 'docs/data_dictionaries/data_dictionary.json')
    # print(json.dumps(report, indent=2))
