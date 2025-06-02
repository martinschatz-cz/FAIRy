import json
import os

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    config = load_config('.project_config.json')
    data_dir: str = config['data_directory_name']
    dictionary: dict[str, dict[str, object]] = {}
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
            if columns:
                col_list = dictionary[fname]["columns"]
                if not isinstance(col_list, list):
                    col_list = []
                    dictionary[fname]["columns"] = col_list
                for col in columns:
                    col_list.append({
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
            else:
                # Fallback for non-CSV or unreadable files
                dictionary[fname]["columns"] = []
    with open('docs/data_dictionaries/data_dictionary.json', 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, indent=2)
    print('Data dictionary generated at docs/data_dictionaries/data_dictionary.json')

# quality_check_tabular_data has been moved to src/checks/quality_check.py

if __name__ == '__main__':
    main()
    # Example usage:
    # report = quality_check_tabular_data('data', 'docs/data_dictionaries/data_dictionary.json')
    # print(json.dumps(report, indent=2))
