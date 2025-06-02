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
    │   │   └── generate_data_dictionary.py
    │   └── utils/
    │       └── regex_builder.py
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

### e. `.github/workflows/data_checks.yml`
- Runs `check_naming_convention.py` on push/PR.
- Fails workflow if non-compliant files are found.

### f. `.github/workflows/zenodo_release.yml`
- Handles Zenodo integration for releases (no direct regex impact).

### g. Documentation
- `README.md`: Project overview, quick start, how to use regex builder.
- `docs/naming_conventions.md`: Naming convention rationale, regex usage, examples.
- `docs/README.md`: Links to naming conventions and regex builder.

### h. `.zenodo.json`
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
- [ ] Write documentation:
    - Main README
    - Naming conventions guide
    - Data dictionary guide (if needed)
- [ ] Set up GitHub Actions workflows for data checks and Zenodo release.

### Phase 3: Testing and Refinement
- [ ] Test template generation with various options.
- [ ] Test scripts and workflows with compliant and non-compliant data.
- [ ] Iterate and refine based on feedback and test results.

---

## 4. Checklist for Each Script

- `regex_builder.py`: Loads/saves regex, interactive CLI, human-readable explanations, live testing.
- `check_naming_convention.py`: Loads regex, validates files, outputs report.
- `generate_data_dictionary.py`: Scans data, generates dictionary, uses config.
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