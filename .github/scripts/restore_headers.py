#!/usr/bin/env python3
import argparse
import json
import os
import sys


def update_po_file(filepath, translation_id):
    """
    Opens the file at filepath, checks for the header "X-WagtailLocalize-TranslationID:".
    If not present, adds it immediately after the line containing "Generated-By:".
    Returns True if the file was updated, False otherwise.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return False

    # Check if header already exists.
    if any("X-WagtailLocalize-TranslationID:" in line for line in lines):
        return False

    # Find the index of the line containing "Generated-By:".
    index = None
    for i, line in enumerate(lines):
        if "Generated-By:" in line:
            index = i
            break

    if index is None:
        print(
            f"Warning: 'Generated-By:' header not found in {filepath}. Skipping.",
            file=sys.stderr,
        )
        return False

    # Create the header line to be inserted.
    new_header = rf'"X-WagtailLocalize-TranslationID: {translation_id}\n"' + "\n"
    # Insert the new header after the "Generated-By:" line.
    lines.insert(index - 1, new_header)

    # Write the updated lines back to the file.
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"Updated {filepath} with new translation header.")
        return True
    except Exception as e:
        print(f"Error writing to {filepath}: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="For each file specified in the JSON mapping, check and insert the X-WagtailLocalize-TranslationID header if missing."
    )
    parser.add_argument(
        "--path", required=True, help="Path to the locales folder in the repository."
    )
    parser.add_argument(
        "--json", required=True, help="Path to the JSON file containing file mappings."
    )

    args = parser.parse_args()

    # Load the JSON file.
    try:
        with open(args.json, "r", encoding="utf-8") as jf:
            translations = json.load(jf)
    except Exception as e:
        print(f"Error reading JSON file {args.json}: {e}", file=sys.stderr)
        sys.exit(1)

    # Process each relative file path and translation id.
    for rel_path, trans_id in translations.items():
        file_path = os.path.join(args.path, rel_path)
        if not os.path.isfile(file_path):
            print(f"Warning: File {rel_path} does not exist.", file=sys.stderr)
            continue
        if trans_id != "":
            update_po_file(file_path, trans_id)
        else:
            print(f"Warning: Missing header info for file {rel_path}.", file=sys.stderr)


if __name__ == "__main__":
    main()
