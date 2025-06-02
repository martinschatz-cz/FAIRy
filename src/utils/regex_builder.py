import json
import os
import re

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def explain_regex(regex):
    # Placeholder: In production, use a library or custom logic for better explanations
    return f"Current regex: {regex}\n(Explanation: matches files like 'P01_ExpA_2025-06-02.csv')"

def test_regex(regex):
    while True:
        fname = input('Test a filename (or press Enter to finish): ')
        if not fname:
            break
        if re.match(regex, fname):
            print('Valid!')
        else:
            print('Invalid!')

def main():
    config_path = '.project_config.json'
    config = load_config(config_path)
    regex = config['data_naming_convention_regex']
    print('--- Naming Convention Regex Builder ---')
    print(explain_regex(regex))
    print('\nYou can test filenames against the current regex.')
    test_regex(regex)
    # Optionally, add logic to interactively update and save regex
    print('\nTo update the regex, edit .project_config.json or extend this script.')

if __name__ == '__main__':
    main()
