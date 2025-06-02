# FAIRy

![FAIRy Logo](FAIRy_logo.jpg)

FAIRy is a toolkit for FAIRification and quality control of data management, especially for tabular data. It helps you enforce naming conventions, generate data dictionaries, check data quality, and prepare metadata for repositories like Zenodo.

## What does FAIRy do?
- **Enforces file naming conventions** using regex (customizable via an interactive builder)
- **Generates data dictionaries** for your tabular datasets, including all standard metadata fields
- **Performs automated quality checks** on tabular data based on your data dictionary (e.g., type, range, allowed values, uniqueness, missing values)
- **Helps you prepare Zenodo metadata** from a CSV template
- **Supports automation** via GitHub Actions for continuous data quality and FAIR compliance

---

## How to Use FAIRy: Step by Step

### 1. Set Up Your Project
- Clone or generate your project using the Cookiecutter FAIR RDM template (or set up the folder structure as shown in `plan.md`).
- Place your data files in the `data/` directory (e.g., `data/raw/`).

### 2. Enforce and Customize Naming Conventions
- Edit `.project_config.json` to set your initial naming convention regex.
- Run the interactive regex builder to refine your rules:
  ```powershell
  python src/utils/regex_builder.py
  ```
  - Test filenames and update the regex as needed.

### 3. Generate a Data Dictionary
- Run the data dictionary generator to scan your data files and create a metadata-rich dictionary:
  ```powershell
  python src/checks/generate_data_dictionary.py
  ```
  - This creates/updates `docs/data_dictionaries/data_dictionary.json`.
  - Edit this file to add descriptions, types, allowed values, etc. for each column.

### 4. Check Data Quality
- Run the quality check script to validate your data against the data dictionary:
  ```powershell
  python src/checks/quality_check.py
  ```
  - This will report issues such as missing columns, type errors, invalid values, duplicates, and missing data.

### 5. Prepare Zenodo Metadata
- If you need to deposit your data in Zenodo, generate a metadata CSV (or use the template):
  ```powershell
  python src/utils/generate_zenodo_json.py input.csv .zenodo.json
  ```
  - If `input.csv` does not exist, a template will be created for you to fill in.
  - Edit the CSV, then rerun the command to generate `.zenodo.json`.

### 6. Automate with GitHub Actions
- The provided workflows in `.github/workflows/` will automatically check naming conventions and data quality on every push or pull request.

---

## Example Workflow
1. Add a new CSV file to `data/raw/`.
2. Run the data dictionary generator:
   ```powershell
   python src/checks/generate_data_dictionary.py
   ```
3. Edit `docs/data_dictionaries/data_dictionary.json` to fill in metadata for each column.
4. Run the quality check:
   ```powershell
   python src/checks/quality_check.py
   ```
5. Fix any reported issues in your data.
6. Prepare Zenodo metadata as needed.

---

For more details, see the documentation in the `docs/` folder.
