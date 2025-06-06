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

## Using the Regex Builder via CLI

You can launch the interactive regex builder at any time with:

```bash
fairy --regex-builder
```

This will run the regex builder script and allow you to customize your naming convention interactively. The changes will be saved to `.project_config.json`.

Alternatively, you can still run it directly with:

```bash
python src/utils/regex_builder.py
```

---

### 3. Generate a Data Dictionary
- Run the data dictionary generator to scan your data files and create a metadata-rich dictionary:
  ```powershell
  python src/checks/generate_data_dictionary.py
  ```
  - This creates/updates `docs/data_dictionaries/data_dictionary.json`.
  - Edit this file to add descriptions, types, allowed values, etc. for each column.

### 4. Check Data Quality
- Run the quality check script to validate your data against the data dictionary:
  ```bash
  python src/checks/quality_check.py
  ```
  - This will report issues such as missing columns, type errors, invalid values, duplicates, and missing data.

### 5. (Advanced) Generate Great Expectations Suite from Data Dictionary
- If you want to generate a Great Expectations suite from your data dictionary CSV, use:
  ```bash
  python src/utils/csv_to_ge_suite.py <data_dictionary.csv> <data_file.csv>
  ```
  - This will create a GE suite for advanced data validation workflows (optional).
  - **Note:** The core FAIRy quality checks do not require Great Expectations and are tested independently for reliability.

### 6. Prepare Zenodo Metadata
- If you need to deposit your data in Zenodo, generate a metadata CSV (or use the template):
  ```bash
  python src/utils/generate_zenodo_json.py input.csv .zenodo.json
  ```
  - If `input.csv` does not exist, a template will be created for you to fill in.
  - Edit the CSV, then rerun the command to generate `.zenodo.json`.

### 7. Automate with GitHub Actions
- The provided workflows in `.github/workflows/` will automatically check naming conventions and data quality on every push or pull request.

---

## Quick Project Scaffolding with Cookiecutter

1. **Clone the FAIRy template repository:**
   ```bash
   git clone https://github.com/martinschatz-cz/FAIRy.git
   cd FAIRy
   ```

2. **Run Cookiecutter from the template root:**
   ```bash
   cookiecutter .
   ```
   - Answer the prompts.
   - Your new project will be created in a new folder.

3. **Change into your new project folder and follow the README instructions.**

---

**Note:**
- Do NOT run `cookiecutter .` from inside a generated project or a non-template folder.
- The `fairy` CLI is for running FAIRy’s Python tools inside your generated project, not for project scaffolding.

---

## Using Cookiecutter to Start a New FAIRy Project

You can use Cookiecutter to quickly scaffold a new FAIR-compliant research data management project using this template:

1. **Install Cookiecutter** (if you haven't already):
   ```bash
   pip install cookiecutter
   ```

2. **Generate a new project** using this template:
   - If you have this repository locally, run:
     ```bash
     cookiecutter .
     ```
     from the root of this repository.
   - Or, use a remote repository (replace URL as needed):
     ```bash
     cookiecutter https://github.com/martinschatz-cz/FAIRy.git
     ```

3. **Answer the prompts** to configure your new project (project name, config file name, etc.).

4. **Your new project** will be created in a new folder, with all the structure and scripts described below.

5. **Follow the steps in the generated README** of your new project to set up naming conventions, generate data dictionaries, check data quality, and automate with GitHub Actions.

---

## FAIRy Command-Line Shortcuts

You can run all major FAIRy functions from the command line using the `fairy` command with the following options:

- `fairy --regex-builder` — Launch the interactive regex builder to customize your naming convention.
- `fairy --check-naming` — Check all files in your data directory for naming convention compliance.
- `fairy --generate-data-dictionary [--config <config.json>] [--out <output.json>]` — Generate or update the data dictionary. You can specify a custom config file and output path.
- `fairy --quality-check` — Run the data quality check using your data dictionary. This command prints a detailed, user-friendly report for each file and column. If all checks pass, it will print `All files passed all quality checks!` so you always know your data is fully compliant.
- `fairy --zenodo-template` — Generate a Zenodo metadata CSV template (`input.csv`).
- `fairy --zenodo-json --csv <input.csv> --out <output.json>` — Convert a metadata CSV to a Zenodo JSON file for upload.

These shortcuts make it easy to use FAIRy features without remembering long script paths. For example:

```bash
fairy --generate-data-dictionary --config myconfig.json --out mydict.json
fairy --zenodo-json --csv input.csv --out .zenodo.json
```

---

## Testing and Development Notes
- All core logic (including data dictionary parsing and quality checks) is tested with unit tests in `tests/`.
- Tests for CSV-to-expectations logic are decoupled from Great Expectations and use pandas for robust, fast validation.
- To run all tests:
  ```bash
  pytest
  ```

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
