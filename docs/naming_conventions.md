# Naming Conventions

This document explains the rationale for file naming conventions and how to use the regex builder.

## Why Naming Conventions?
- Improve findability and interoperability
- Enable automated checks and workflows

## Default Convention
- Example: `P01_ExpA_2025-06-02.csv`
- Regex: `^P[0-9]{2}_Exp[A-Z]{1}_[0-9]{4}-[0-9]{2}-[0-9]{2}\.(csv|json)$`

## Customizing
- Use `src/utils/regex_builder.py` to interactively build and test your regex.

## Examples
- `P02_ExpB_2025-06-02.json` (valid)
- `P2_ExpA_2025-06-02.csv` (invalid)
