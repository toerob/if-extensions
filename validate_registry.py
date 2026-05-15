#!/usr/bin/env python3
"""Validate registry package.yaml and release yaml files against their schemas."""

import sys
import yaml
import jsonschema
from pathlib import Path

REPO_ROOT = Path(__file__).parent
SCHEMAS_DIR = REPO_ROOT / "schemas"


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_schema(name):
    return load_yaml(SCHEMAS_DIR / name)


def validate(data, schema, label):
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.json_path)
    if errors:
        print(f"  FAIL  {label}")
        for e in errors:
            path = e.json_path if e.json_path != "$" else "(root)"
            print(f"        {path}: {e.message}")
        return False
    return True


def main():
    package_schema = load_schema("package.schema.yaml")
    release_schema = load_schema("release.schema.yaml")

    passed = failed = 0

    registry_root = REPO_ROOT / "registry"
    for package_path in sorted(registry_root.glob("*/*/*/package.yaml")):
        data = load_yaml(package_path)
        label = package_path.relative_to(registry_root)
        if validate(data, package_schema, label):
            passed += 1
        else:
            failed += 1

    for release_path in sorted(registry_root.glob("*/*/*/releases/*.yaml")):
        data = load_yaml(release_path)
        label = release_path.relative_to(registry_root)
        if validate(data, release_schema, label):
            passed += 1
        else:
            failed += 1

    total = passed + failed
    print(f"\n{passed}/{total} passed", end="")
    if failed:
        print(f", {failed} failed")
        sys.exit(1)
    else:
        print()


if __name__ == "__main__":
    main()
