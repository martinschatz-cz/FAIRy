import os
import subprocess
import sys

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
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'checks', 'quality_check.py')])
        return
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
