import json
import os
import re

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    config = load_config('.project_config.json')
    regex = config['data_naming_convention_regex']
    data_dir = config['data_directory_name']
    allowed_exts = config['allowed_file_extensions']
    non_compliant = []
    for root, _, files in os.walk(data_dir):
        for fname in files:
            if not re.match(regex, fname):
                non_compliant.append(os.path.join(root, fname))
    if non_compliant:
        print('Non-compliant files:')
        for f in non_compliant:
            print(f)
        exit(1)
    else:
        print('All files are compliant.')

if __name__ == '__main__':
    main()
