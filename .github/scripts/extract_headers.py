#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys


def parse_po_file(filepath):
    """
    Reads a .po file and returns the value of the header
    'X-WagtailLocalize-TranslationID' if found, otherwise None.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return None

    # Look for the header line in the content.
    # This regex will capture the value after the header name.
    match = re.search(r"X-WagtailLocalize-TranslationID:\s*(\S+)", content)
    if match:
        return match.group(1).rstrip(r'\n"')
    else:
        return ""


def main():
    parser = argparse.ArgumentParser(
        description="Search a directory for .po files, extract the X-WagtailLocalize-TranslationID header, and build a dictionary mapping relative paths to the header value."
    )
    parser.add_argument(
        "--path", help="The directory path to search for .po files", required=True
    )
    args = parser.parse_args()

    translation_dict = {}

    for root, _, files in os.walk(args.path):
        for filename in files:
            if filename.endswith(".po"):
                full_path = os.path.join(root, filename)
                # Calculate the path relative to the argument path.
                rel_path = os.path.relpath(full_path, args.path)
                translation_id = parse_po_file(full_path)
                translation_dict[rel_path] = translation_id
                if translation_id == "":
                    print(
                        f"Warning: {rel_path} is missing header 'X-WagtailLocalize-TranslationID'",
                        file=sys.stderr,
                    )

    # Store the resulting
    with open(".github/scripts/ids.json", "w") as f:
        json.dump(translation_dict, f, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
