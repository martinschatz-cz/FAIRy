import os
import subprocess
import sys
import json

def main():
    import sys
    import argparse
    if '--regex-builder' in sys.argv:
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'utils', 'regex_builder.py')])
        return
    if '--check-naming' in sys.argv:
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'checks', 'check_naming_convention.py')])
        return
    if '--generate-data-dictionary' in sys.argv:
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', type=str, default='.project_config.json', help='Path to config file')
        parser.add_argument('--out', type=str, default='docs/data_dictionaries/data_dictionary.json', help='Output data dictionary path')
        args, _ = parser.parse_known_args()
        env = dict(os.environ)
        env['FAIRY_CONFIG'] = args.config
        env['FAIRY_DD_OUT'] = args.out
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'checks', 'generate_data_dictionary.py')], env=env)
        return
    if '--quality-check' in sys.argv:
        # Verbose: print results and always print a success message if all checks pass
        config_path = os.environ.get('FAIRY_CONFIG', '.project_config.json')
        dict_path = os.environ.get('FAIRY_DD_OUT', 'docs/data_dictionaries/data_dictionary.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        data_dir = config.get('data_directory_name', 'data')
        # Import using relative path so it works as a script or CLI
        import importlib.util
        import pathlib
        qc_path = pathlib.Path(__file__).parent / 'checks' / 'quality_check.py'
        spec = importlib.util.spec_from_file_location('quality_check', qc_path)
        if spec and spec.loader:
            qc = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(qc)
            report = qc.quality_check_tabular_data(data_dir, dict_path)
        else:
            print('Could not load quality_check module.')
            sys.exit(2)
        any_errors = False
        for fname, issues in report.items():
            print(f'File: {fname}')
            if 'error' in issues:
                print('  ERROR:', issues['error'])
                any_errors = True
                continue
            if issues['file_issues']:
                for issue in issues['file_issues']:
                    print('  File issue:', issue)
                    any_errors = True
            if issues['column_issues']:
                for col, col_issues in issues['column_issues'].items():
                    for col_issue in col_issues:
                        print(f'  Column {col}:', col_issue)
                        any_errors = True
            if not issues['file_issues'] and not issues['column_issues'] and 'error' not in issues:
                print('  All checks passed.')
        if not any_errors:
            print('\nAll files passed all quality checks!')
        else:
            print('\nSome files have issues. See above.')
        sys.exit(1 if any_errors else 0)
    if '--zenodo-template' in sys.argv:
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'utils', 'generate_zenodo_json.py'), '--template'])
        return
    if '--zenodo-json' in sys.argv:
        parser = argparse.ArgumentParser()
        parser.add_argument('--csv', type=str, required=True)
        parser.add_argument('--out', type=str, required=True)
        args, _ = parser.parse_known_args()
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'utils', 'generate_zenodo_json.py'), '--csv', args.csv, '--out', args.out])
        return

    cwd = os.getcwd()
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '{{cookiecutter.project_slug}}'))
    # Only copy the contents of the template directory, not unnecessary folders like examples or tests
    for item in os.listdir(template_dir):
        if item in ("examples", "tests"):  # skip unnecessary folders
            continue
        src_path = os.path.join(template_dir, item)
        dest_path = os.path.join(cwd, item)
        if os.path.isdir(src_path):
            if not os.path.exists(dest_path):
                subprocess.run(["cp", "-r", src_path, dest_path])
        else:
            subprocess.run(["cp", src_path, dest_path])
    print("[INFO] FAIRy template files copied to current directory.")

if __name__ == "__main__":
    main()
