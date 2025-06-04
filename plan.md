# Cookiecutter FAIR RDM Template

This plan outlines the development and execution of a Cookiecutter template for Python research data management projects, emphasizing FAIR principles, automation, and user-friendly naming convention enforcement.

---

## 1. Package Structure Overview

### a. Cookiecutter Template Structure

```
cookiecutter-rdm-template/
│
├── cookiecutter.json
├── hooks/
│   └── post_gen_project.py
└── {{cookiecutter.project_slug}}/
    ├── README.md
    ├── LICENSE
    ├── requirements.txt
    ├── pyproject.toml
    ├── .gitignore
    ├── .zenodo.json
    ├── {{cookiecutter.project_config_file_name}}
    ├── data/
    │   ├── raw/
    │   ├── processed/
    │   ├── metadata/
    │   └── README.md
    ├── src/
    │   ├── __init__.py
    │   ├── checks/
    │   │   ├── check_naming_convention.py
    │   │   ├── generate_data_dictionary.py
    │   │   └── quality_check.py
    │   └── utils/
    │       ├── regex_builder.py
    │       ├── generate_zenodo_json.py
    │       └── csv_to_ge_suite.py
    ├── docs/
    │   ├── README.md
    │   ├── data_dictionaries/
    │   ├── metadata_schema.md
    │   └── naming_conventions.md
    └── .github/
        └── workflows/
            ├── data_checks.yml
            └── zenodo_release.yml
```

---

## 2. Main Functions and Responsibilities

### a. `hooks/post_gen_project.py`
- Reads user choices from `cookiecutter.json`.
- Constructs initial regex for file naming.
- Writes config file (e.g., `.project_config.json`).
- Prints user guidance for next steps.

### b. `src/utils/regex_builder.py`
- Loads regex and settings from config.
- Provides CLI for interactive regex building/refinement.
- Explains regex in human-readable form.
- Allows live testing of regex against filenames.
- Saves updated regex to config.

### c. `src/checks/check_naming_convention.py`
- Loads regex from config.
- Scans data directory for files.
- Validates filenames against regex.
- Outputs report (pass/fail, non-compliant files).

### d. `src/checks/generate_data_dictionary.py`
- Reads data directory and metadata.
- Generates a data dictionary (structure, fields, types).
- Optionally uses config for paths/settings.

### e. `src/checks/quality_check.py`
- Loads data dictionary and data files.
- Performs automated quality checks (type, range, allowed values, uniqueness, missing values) using pandas.
- Outputs a detailed report of issues.
- **Note:** All core quality checks are independent of Great Expectations for reliability and testability.

### f. `src/utils/csv_to_ge_suite.py`
- (Advanced/Optional) Converts a data dictionary CSV to a Great Expectations suite for advanced validation workflows.
- Not required for core FAIRy quality checks or automation.
- Logic for parsing the data dictionary and building expectations is tested independently using pandas.

### g. `.github/workflows/data_checks.yml`
- Runs `check_naming_convention.py` and `quality_check.py` on push/PR.
- Fails workflow if non-compliant files or data issues are found.

### h. `.github/workflows/zenodo_release.yml`
- Handles Zenodo integration for releases (no direct regex or data validation impact).

### i. Documentation
- `README.md`: Project overview, quick start, how to use regex builder, quality checks, and advanced GE suite generation.
- `docs/naming_conventions.md`: Naming convention rationale, regex usage, examples.
- `docs/README.md`: Links to naming conventions and regex builder.

### j. `.zenodo.json`
- Pre-filled metadata for Zenodo, with dynamic fields.

---

## 3. Execution Roadmap

### Phase 1: Template and Structure
- [ ] Scaffold the Cookiecutter template as above.
- [ ] Implement `cookiecutter.json` with all variables, including naming convention options.
- [ ] Write `hooks/post_gen_project.py` to generate config and initial regex.
- [ ] Create templates for all static files (README, LICENSE, requirements, etc.).

### Phase 2: Core Functionality
- [ ] Develop Python scripts:
    - `regex_builder.py` (interactive CLI)
    - `check_naming_convention.py` (validation)
    - `generate_data_dictionary.py` (data dictionary)
    - `quality_check.py` (data quality checks, pandas-based)
    - `csv_to_ge_suite.py` (optional, for GE suite generation)
- [ ] Write documentation:
    - Main README
    - Naming conventions guide
    - Data dictionary guide (if needed)
- [ ] Set up GitHub Actions workflows for data checks and Zenodo release.

### Phase 3: Testing and Refinement
- [ ] Test template generation with various options.
- [ ] Test scripts and workflows with compliant and non-compliant data.
- [ ] Ensure all core logic is covered by unit tests in `tests/`, using pandas for expectation logic validation.
- [ ] Tests for CSV-to-GE suite logic are decoupled from Great Expectations and use pandas for robust, fast validation.
- [ ] Iterate and refine based on feedback and test results.

---

## 4. Checklist for Each Script

- `regex_builder.py`: Loads/saves regex, interactive CLI, human-readable explanations, live testing.
- `check_naming_convention.py`: Loads regex, validates files, outputs report.
- `generate_data_dictionary.py`: Scans data, generates dictionary, uses config.
- `quality_check.py`: Loads data, performs quality checks, outputs report.
- `post_gen_project.py`: Reads variables, generates config, prints guidance.

---

## 5. Next Steps

- Start by creating the template structure and `cookiecutter.json`.
- Implement the post-generation hook and config logic.
- Develop and test the core Python scripts.
- Write and refine documentation.
- Test the full workflow and iterate.

---

This plan is now ready for execution. Each function and file has a clear responsibility, and the structure supports maintainability and FAIR compliance.