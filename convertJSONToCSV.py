import json
import csv
import os
from datetime import datetime
from pathlib import Path

def flatten_json(nested_json, parent_key='', sep='.'):
    """
    Flatten a nested json file into a dictionary with key paths.
    Example:
    {"a":{"b":1,"c":2}} -> {"a.b":1,"a.c":2}
    """
    items = {}
    for k, v in nested_json.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_json(v, new_key, sep=sep))
        elif isinstance(v, list):
            # Convert list to string or flatten further if dicts inside
            if all(isinstance(i, dict) for i in v):
                for idx, i in enumerate(v):
                    items.update(flatten_json(i, f"{new_key}[{idx}]", sep=sep))
            else:
                items[new_key] = ','.join(map(str, v))
        else:
            items[new_key] = v
    return items

def json_to_csv(json_file, csv_file):
    """
    Convert JSON file to CSV file with flattened keys.
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Ensure data is a list of records
    if isinstance(data, dict):
        data = [data]

    flattened_data = [flatten_json(record) for record in data]

    # Collect all unique keys for CSV header
    fieldnames = set()
    for record in flattened_data:
        fieldnames.update(record.keys())
    fieldnames = sorted(fieldnames)

    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in flattened_data:
            writer.writerow(record)

if __name__ == "__main__":
    # Example usage
    input_json = "policy_rsty6ny9q8a7ZbdqB697_20251211_173643.json"
    #output_csv = "output.csv"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = Path(input_json).stem
    output_csv = f"./csv_outputs/{json_filename}_transformed_{timestamp}.csv"

    if os.path.exists(input_json):
        json_to_csv(input_json, output_csv)
        print(f"Converted {input_json} to {output_csv}")
    else:
        print(f"File {input_json} not found.")