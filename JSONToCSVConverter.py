"""JSON to CSV converter with key-based filtering and transformation."""

import json
import csv
import pandas as pd
from pathlib import Path
from typing import Any, Dict, List, Union, Optional
from datetime import datetime
import logging


class JSONToCSVConverter:
    """Convert JSON files to CSV with flexible key-based filtering."""
    
    def __init__(self, output_directory: str = "csv_output"):
        """Initialize the converter."""
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(exist_ok=True)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def convert_json_to_csv(self, json_file_path: str, 
                          output_csv_path: str = None,
                          target_keys: List[str] = None,
                          nested_key_path: str = None,
                          flatten_nested: bool = True) -> str:
        """
        Convert JSON file to CSV based on specified keys.
        
        Args:
            json_file_path: Path to input JSON file
            output_csv_path: Path to output CSV file (auto-generated if None)
            target_keys: List of keys to extract (None = all keys)
            nested_key_path: Path to nested data (e.g., 'data.items')
            flatten_nested: Whether to flatten nested objects
        
        Returns:
            Path to created CSV file
        """
        # Load JSON data
        json_data = self._load_json_file(json_file_path)
        
        # Extract data based on nested key path if specified
        if nested_key_path:
            json_data = self._extract_nested_data(json_data, nested_key_path)
        
        # Convert to list of dictionaries if not already
        data_list = self._normalize_to_list(json_data)
        
        # Filter by target keys if specified
        if target_keys:
            data_list = self._filter_by_keys(data_list, target_keys)
        
        # Flatten nested objects if requested
        if flatten_nested:
            data_list = self._flatten_nested_objects(data_list)
        
        # Generate output path if not provided
        if output_csv_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_filename = Path(json_file_path).stem
            output_csv_path = self.output_directory / f"{json_filename}_{timestamp}.csv"
        else:
            output_csv_path = Path(output_csv_path)
        
        # Write to CSV
        self._write_to_csv(data_list, output_csv_path)
        
        self.logger.info(f"Successfully converted {json_file_path} to {output_csv_path}")
        return str(output_csv_path)
    
    def convert_with_key_mapping(self, json_file_path: str,
                               key_mapping: Dict[str, str],
                               output_csv_path: str = None) -> str:
        """
        Convert JSON to CSV with key renaming.
        
        Args:
            json_file_path: Path to input JSON file
            key_mapping: Dictionary mapping old keys to new keys
            output_csv_path: Path to output CSV file
        
        Returns:
            Path to created CSV file
        """
        json_data = self._load_json_file(json_file_path)
        data_list = self._normalize_to_list(json_data)
        
        # Apply key mapping
        mapped_data = []
        for item in data_list:
            mapped_item = {}
            for old_key, new_key in key_mapping.items():
                if old_key in item:
                    mapped_item[new_key] = item[old_key]
            mapped_data.append(mapped_item)
        
        if output_csv_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_filename = Path(json_file_path).stem
            output_csv_path = self.output_directory / f"{json_filename}_mapped_{timestamp}.csv"
        
        self._write_to_csv(mapped_data, output_csv_path)
        return str(output_csv_path)
    
    def convert_multiple_files(self, json_files: List[str],
                             target_keys: List[str] = None,
                             combine_files: bool = False) -> List[str]:
        """
        Convert multiple JSON files to CSV.
        
        Args:
            json_files: List of JSON file paths
            target_keys: Keys to extract from each file
            combine_files: Whether to combine all files into one CSV
        
        Returns:
            List of created CSV file paths
        """
        if combine_files:
            return [self._combine_multiple_files(json_files, target_keys)]
        else:
            csv_files = []
            for json_file in json_files:
                csv_file = self.convert_json_to_csv(json_file, target_keys=target_keys)
                csv_files.append(csv_file)
            return csv_files
    
    def _load_json_file(self, file_path: str) -> Union[Dict, List]:
        """Load JSON data from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file {file_path}: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {file_path}")
    
    def _extract_nested_data(self, data: Union[Dict, List], key_path: str) -> Any:
        """Extract data from nested structure using dot notation."""
        keys = key_path.split('.')
        current_data = data
        
        for key in keys:
            if isinstance(current_data, dict) and key in current_data:
                current_data = current_data[key]
            elif isinstance(current_data, list) and key.isdigit():
                index = int(key)
                if 0 <= index < len(current_data):
                    current_data = current_data[index]
                else:
                    raise IndexError(f"Index {index} out of range")
            else:
                raise KeyError(f"Key path '{key_path}' not found in data")
        
        return current_data
    
    def _normalize_to_list(self, data: Union[Dict, List]) -> List[Dict]:
        """Convert data to list of dictionaries."""
        if isinstance(data, list):
            # If it's already a list, ensure all items are dictionaries
            result = []
            for item in data:
                if isinstance(item, dict):
                    result.append(item)
                else:
                    result.append({"value": item})
            return result
        elif isinstance(data, dict):
            # If it's a single dictionary, wrap it in a list
            return [data]
        else:
            # If it's a primitive value, create a dictionary
            return [{"value": data}]
    
    def _filter_by_keys(self, data_list: List[Dict], target_keys: List[str]) -> List[Dict]:
        """Filter dictionaries to only include specified keys."""
        filtered_data = []
        for item in data_list:
            filtered_item = {}
            for key in target_keys:
                if key in item:
                    filtered_item[key] = item[key]
                else:
                    # Handle nested key paths
                    if '.' in key:
                        try:
                            nested_value = self._get_nested_value(item, key)
                            filtered_item[key] = nested_value
                        except (KeyError, TypeError):
                            filtered_item[key] = None
                    else:
                        filtered_item[key] = None
            filtered_data.append(filtered_item)
        return filtered_data
    
    def _get_nested_value(self, data: Dict, key_path: str) -> Any:
        """Get value from nested dictionary using dot notation."""
        keys = key_path.split('.')
        current_data = data
        
        for key in keys:
            if isinstance(current_data, dict) and key in current_data:
                current_data = current_data[key]
            else:
                raise KeyError(f"Key '{key}' not found")
        
        return current_data
    
    def _flatten_nested_objects(self, data_list: List[Dict], 
                              separator: str = '_') -> List[Dict]:
        """Flatten nested dictionaries and lists."""
        flattened_data = []
        
        for item in data_list:
            flattened_item = self._flatten_dict(item, separator)
            flattened_data.append(flattened_item)
        
        return flattened_data
    
    def _flatten_dict(self, data: Dict, separator: str = '_', 
                     parent_key: str = '') -> Dict:
        """Recursively flatten a nested dictionary."""
        items = []
        
        for key, value in data.items():
            new_key = f"{parent_key}{separator}{key}" if parent_key else key
            
            if isinstance(value, dict):
                items.extend(self._flatten_dict(value, separator, new_key).items())
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        items.extend(self._flatten_dict(
                            item, separator, f"{new_key}{separator}{i}"
                        ).items())
                    else:
                        items.append((f"{new_key}{separator}{i}", item))
            else:
                items.append((new_key, value))
        
        return dict(items)
    
    def _write_to_csv(self, data_list: List[Dict], output_path: Path):
        """Write data to CSV file."""
        if not data_list:
            self.logger.warning("No data to write to CSV")
            return
        
        # Get all unique keys from all dictionaries
        all_keys = set()
        for item in data_list:
            all_keys.update(item.keys())
        
        fieldnames = sorted(list(all_keys))
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_list)
    
    def _combine_multiple_files(self, json_files: List[str], 
                              target_keys: List[str] = None) -> str:
        """Combine multiple JSON files into one CSV."""
        combined_data = []
        
        for json_file in json_files:
            json_data = self._load_json_file(json_file)
            data_list = self._normalize_to_list(json_data)
            
            if target_keys:
                data_list = self._filter_by_keys(data_list, target_keys)
            
            # Add source file information
            for item in data_list:
                item['_source_file'] = Path(json_file).name
            
            combined_data.extend(data_list)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_directory / f"combined_{timestamp}.csv"
        
        self._write_to_csv(combined_data, output_path)
        return str(output_path)