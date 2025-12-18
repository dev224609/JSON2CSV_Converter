import json
import os
from pathlib import Path

def merge_json_files_from_folder(folder_path, output_file):
    """
    Merge multiple JSON files from a folder into one JSON file.
    - If files contain JSON objects (dicts), they are merged into a single dict.
    - If files contain JSON arrays (lists), they are concatenated into a single list.
    
    :param folder_path: Path to the folder containing JSON files
    :param output_file: Path to the output merged JSON file
    """
    folder = Path(folder_path)
    json_files = list(folder.glob("*.json"))

    if not json_files:
        raise FileNotFoundError("No JSON files found in the folder.")

    merged_data = None

    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Initialize merged_data based on first file type
            if merged_data is None:
                if isinstance(data, dict):
                    merged_data = {}
                elif isinstance(data, list):
                    merged_data = []
                else:
                    raise ValueError(f"{file_path} contains unsupported JSON type")

            # Merge depending on type
            if isinstance(merged_data, dict) and isinstance(data, dict):
                merged_data.update(data)  # later files overwrite earlier keys
            elif isinstance(merged_data, list) and isinstance(data, list):
                merged_data.extend(data)
            else:
                raise ValueError(f"Inconsistent JSON types across files. Found {type(data)} in {file_path}")

    # Write merged output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=4)

    print(f"Merged {len(json_files)} files into {output_file}")


if __name__ == "__main__":
    # Example usage
    folder_path = "json_folder"   # Replace with your folder path
    output_file = "merged.json"   # Output file name
    merge_json_files_from_folder(folder_path, output_file)