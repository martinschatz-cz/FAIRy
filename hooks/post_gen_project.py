# Post-generation hook for Cookiecutter FAIR RDM Template
import json
import os
from typing import Any

CONFIG_FILE = "{{cookiecutter.project_config_file_name}}"

# Example: build a regex from user choices (expand as needed)
def build_initial_regex():
    # This is a placeholder; in real use, build from cookiecutter context
    return r"^P[0-9]{2}_Exp[A-Z]{1}_[0-9]{4}-[0-9]{2}-[0-9]{2}\\.(csv|json)$"

def main():
    config: dict[str, Any] = {
        "project_name": "My Horizon Europe Data Project",
        "project_slug": "my-horizon-europe-data-project",
        "author_name": "Your Name",
        "email": "your@email.com",
        "github_organization": "your-org",
        "zenodo_community_name": "your-community",
        "include_github_actions": "yes",
        "data_directory_name": "data",
        "code_directory_name": "src",
        "doc_directory_name": "docs",
        "metadata_format": "json",
        "naming_elements_choice": ["project_id", "experiment_name", "date", "version"],
        "date_format_choice": "YYYY-MM-DD",
        "separator_character_choice": "_",
        "allowed_file_extensions_choice": ["csv", "json"],
        "license": "MIT",
        "python_version": "3.10",
        "project_config_file_name": ".project_config.json"
    }
    config["data_naming_convention_regex"] = build_initial_regex()
    config["allowed_file_extensions"] = config.pop("allowed_file_extensions_choice", ["csv", "json"])
    config["data_directory_name"] = config.get("data_directory_name", "data")
    # Write all cookiecutter context and regex to config file
    with open(config["project_config_file_name"], "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    print(f"[INFO] Full project config written to {config['project_config_file_name']}")
    print("[INFO] Next: Run src/utils/regex_builder.py to customize your naming convention.")

if __name__ == "__main__":
    main()
