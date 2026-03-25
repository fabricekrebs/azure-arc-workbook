#!/usr/bin/env python3
"""Combine workbook part files into a single Azure Monitor Workbook JSON file.

Usage:
    python combine.py

Reads all JSON files from the parts/ directory (sorted by filename),
concatenates them into the workbook items array, and writes the final
workbook to AzureArc-Comprehensive.workbook.
"""
import json
import os
import glob
import sys


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parts_dir = os.path.join(script_dir, "parts")
    part_files = sorted(glob.glob(os.path.join(parts_dir, "*.json")))

    if not part_files:
        print("ERROR: No part files found in parts/ directory", file=sys.stderr)
        sys.exit(1)

    all_items = []
    for pf in part_files:
        with open(pf, "r", encoding="utf-8") as f:
            try:
                items = json.load(f)
            except json.JSONDecodeError as e:
                print(f"ERROR: Invalid JSON in {os.path.basename(pf)}: {e}", file=sys.stderr)
                sys.exit(1)
        if isinstance(items, list):
            all_items.extend(items)
        else:
            all_items.append(items)

    workbook = {
        "version": "Notebook/1.0",
        "items": all_items,
        "fallbackResourceIds": ["azure monitor"],
        "$schema": "https://github.com/Microsoft/Application-Insights-Workbooks/blob/master/schema/workbook.json"
    }

    output_path = os.path.join(script_dir, "AzureArc-Comprehensive.workbook")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(workbook, f, indent=2, ensure_ascii=False)

    print(f"Workbook generated: {output_path}")
    print(f"  Total items: {len(all_items)}")
    print(f"  Parts combined: {len(part_files)}")
    for pf in part_files:
        print(f"    - {os.path.basename(pf)}")


if __name__ == "__main__":
    main()
