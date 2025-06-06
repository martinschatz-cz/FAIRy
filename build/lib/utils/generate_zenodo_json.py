import csv
import json
import sys
import os
from typing import Any

def write_template_csv(csv_path: str) -> None:
    template = [
        {'field': 'title', 'value': 'My Horizon Europe Data Project'},
        {'field': 'upload_type', 'value': 'dataset'},
        {'field': 'description', 'value': 'A FAIR-compliant research data management project.'},
        {'field': 'creators', 'value': 'Your Name|Your Institution'},
        {'field': 'communities', 'value': 'your-community'},
        {'field': 'keywords', 'value': 'FAIR;RDM;Cookiecutter;Python'},
        {'field': 'license', 'value': 'MIT'}
    ]
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['field', 'value'])
        writer.writeheader()
        for row in template:
            writer.writerow(row)
    print(f"Template CSV written to {csv_path}. Please fill in your metadata and rerun the script.")

def csv_to_zenodo_json(csv_path: str, output_path: str) -> None:
    """
    Reads a CSV file with Zenodo metadata fields and generates a zenodo.json file.
    The CSV should have two columns: 'field' and 'value'.
    For list fields (e.g., keywords), use semicolon-separated values.
    """
    zenodo_dict: dict[str, Any] = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            field = row['field'].strip()
            value = row['value'].strip()
            # Handle list fields
            if field in ['keywords', 'communities', 'creators']:
                if field == 'keywords':
                    zenodo_dict[field] = [k.strip() for k in value.split(';') if k.strip()]
                elif field == 'communities':
                    zenodo_dict[field] = [{"identifier": v.strip()} for v in value.split(';') if v.strip()]
                elif field == 'creators':
                    zenodo_dict[field] = []
                    for creator in value.split(';'):
                        parts = creator.split('|')
                        if len(parts) == 2:
                            zenodo_dict[field].append({"name": parts[0].strip(), "affiliation": parts[1].strip()})
                        else:
                            zenodo_dict[field].append({"name": creator.strip()})
            else:
                zenodo_dict[field] = value
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(zenodo_dict, f, indent=2)
    print(f"Zenodo JSON written to {output_path}")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', action='store_true', help='Write template CSV and exit')
    parser.add_argument('--csv', type=str, help='CSV file to convert to zenodo.json')
    parser.add_argument('--out', type=str, help='Output zenodo.json path')
    args = parser.parse_args()
    if args.template:
        write_template_csv('input.csv')
        print('Template CSV created.')
        sys.exit(0)
    if args.csv and args.out:
        csv_to_zenodo_json(args.csv, args.out)
        print(f'zenodo.json written to {args.out}')
        sys.exit(0)
    print('No action taken. Use --template or --csv/--out.')
    sys.exit(1)

if __name__ == "__main__":
    main()
